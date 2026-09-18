#!/usr/bin/env python3
"""
4-bit MIPS assembler for the CSE 210 custom ISA.

Output format:
    Logisim Evolution "v2.0 raw" memory image for a 256 x 16 instruction ROM.

Usage:
    python mips4_assembler.py program.asm
    python mips4_assembler.py program.asm -o program.hex
    python mips4_assembler.py program.asm -o program.hex --listing program.lst
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# Group-specific ISA
# Sequence fixed earlier from the assignment: NHDIAJEMKBOCFLPG
# ---------------------------------------------------------------------------

OPCODES = {
    "beq":  0x0,
    "ori":  0x1,
    "subi": 0x2,
    "sll":  0x3,
    "add":  0x4,
    "srl":  0x5,
    "and":  0x6,
    "sw":   0x7,
    "nor":  0x8,
    "addi": 0x9,
    "bneq": 0xA,
    "sub":  0xB,
    "andi": 0xC,
    "lw":   0xD,
    "j":    0xE,
    "or":   0xF,
}

REGISTERS = {
    "$zero": 0x0,
    "$t0":   0x1,
    "$t1":   0x2,
    "$t2":   0x3,
    "$t3":   0x4,
    "$t4":   0x5,
}

R_TYPE = {"add", "sub", "and", "or", "nor"}
I_ARITH = {"addi", "subi"}
I_LOGIC = {"andi", "ori"}
SHIFT = {"sll", "srl"}
BRANCH = {"beq", "bneq"}
MEMORY = {"lw", "sw"}

COMMENT_RE = re.compile(r"(#|//|;).*$")
LABEL_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
MEM_RE = re.compile(r"^(.+)\((\$[A-Za-z0-9_]+)\)$")


@dataclass
class SourceLine:
    line_no: int
    address: int
    text: str
    statement: str


class AssemblerError(Exception):
    pass


def clean_line(line: str) -> str:
    return COMMENT_RE.sub("", line).strip()


def parse_number(token: str) -> int:
    token = token.strip().replace("_", "")
    try:
        return int(token, 0)
    except ValueError:
        # Plain decimal without prefix.
        try:
            return int(token, 10)
        except ValueError as exc:
            raise AssemblerError(f"invalid number '{token}'") from exc


def reg(token: str) -> int:
    name = token.strip().lower()
    if name not in REGISTERS:
        valid = ", ".join(REGISTERS)
        raise AssemblerError(f"unknown register '{token}' (valid: {valid})")
    return REGISTERS[name]


def signed4(value: int, what: str) -> int:
    if not -8 <= value <= 7:
        raise AssemblerError(f"{what} {value} does not fit signed 4-bit range -8..7")
    return value & 0xF


def bits4(value: int, what: str) -> int:
    # Allows either signed notation (-8..-1) or unsigned bit-pattern notation (0..15).
    if not -8 <= value <= 15:
        raise AssemblerError(
            f"{what} {value} does not fit a 4-bit field "
            f"(use -8..7 signed or 0..15 as a bit pattern)"
        )
    return value & 0xF


def split_operands(text: str) -> list[str]:
    return [x.strip() for x in text.split(",") if x.strip()]


def encode_r(op: int, operands: list[str]) -> int:
    # Assembly: op $dst, $src1, $src2
    if len(operands) != 3:
        raise AssemblerError("expected: $dst, $src1, $src2")
    dst, src1, src2 = map(reg, operands)
    return (op << 12) | (src1 << 8) | (src2 << 4) | dst


def encode_i_arith(op: int, operands: list[str]) -> int:
    # Assembly: op $dst, $src1, imm
    if len(operands) != 3:
        raise AssemblerError("expected: $dst, $src1, immediate")
    dst = reg(operands[0])
    src1 = reg(operands[1])
    imm = signed4(parse_number(operands[2]), "immediate")
    return (op << 12) | (src1 << 8) | (dst << 4) | imm


def encode_i_logic(op: int, operands: list[str]) -> int:
    # Assembly: op $dst, $src1, imm
    if len(operands) != 3:
        raise AssemblerError("expected: $dst, $src1, immediate")
    dst = reg(operands[0])
    src1 = reg(operands[1])
    imm = bits4(parse_number(operands[2]), "immediate")
    return (op << 12) | (src1 << 8) | (dst << 4) | imm


def encode_shift(op: int, operands: list[str]) -> int:
    # Assembly: sll/srl $dst, $src1, shamt
    # Custom S format: Opcode | Src1 | Dst | Shamt
    if len(operands) != 3:
        raise AssemblerError("expected: $dst, $src1, shamt")
    dst = reg(operands[0])
    src1 = reg(operands[1])
    shamt = parse_number(operands[2])
    if not 0 <= shamt <= 3:
        raise AssemblerError("shift amount must be 0..3 for a 4-bit datapath")
    return (op << 12) | (src1 << 8) | (dst << 4) | shamt


def encode_memory(op: int, mnemonic: str, operands: list[str]) -> int:
    # Assembly:
    #   lw $dst, offset($base)
    #   sw $src, offset($base)
    #
    # Custom I format:
    #   Opcode | Src1(base) | Src2/Dst | signed offset
    if len(operands) != 2:
        if mnemonic == "lw":
            raise AssemblerError("expected: $dst, offset($base)")
        raise AssemblerError("expected: $src, offset($base)")

    data_reg = reg(operands[0])
    match = MEM_RE.match(operands[1].replace(" ", ""))
    if not match:
        raise AssemblerError("memory operand must look like offset($base), e.g. 3($t1)")

    offset_text, base_text = match.groups()
    base = reg(base_text)
    offset = signed4(parse_number(offset_text), "memory offset")
    return (op << 12) | (base << 8) | (data_reg << 4) | offset


def encode_branch(
    op: int,
    operands: list[str],
    labels: dict[str, int],
    pc: int,
) -> int:
    # Assembly: beq/bneq $src1, $src2, label_or_signed_offset
    #
    # CPU rule:
    #   BranchTarget = PC + 1 + sign_extend(offset)
    if len(operands) != 3:
        raise AssemblerError("expected: $src1, $src2, label_or_offset")

    src1 = reg(operands[0])
    src2 = reg(operands[1])
    target = operands[2]

    if target in labels:
        offset_value = labels[target] - (pc + 1)
    else:
        offset_value = parse_number(target)

    offset = signed4(offset_value, "branch offset")
    return (op << 12) | (src1 << 8) | (src2 << 4) | offset


def encode_jump(op: int, operands: list[str], labels: dict[str, int]) -> int:
    # Custom J format:
    #   Opcode | absolute 8-bit target | 0000
    if len(operands) != 1:
        raise AssemblerError("expected: label_or_address")

    target_text = operands[0]
    if target_text in labels:
        target = labels[target_text]
    else:
        target = parse_number(target_text)

    if not 0 <= target <= 0xFF:
        raise AssemblerError(f"jump target {target} does not fit 8 bits (0..255)")

    return (op << 12) | (target << 4)


def first_pass(lines: list[str]) -> tuple[dict[str, int], list[SourceLine]]:
    labels: dict[str, int] = {}
    source: list[SourceLine] = []
    pc = 0

    for line_no, raw in enumerate(lines, start=1):
        text = clean_line(raw)
        if not text:
            continue

        # Permit "label:" and "label: instruction" forms.
        while ":" in text:
            label_part, rest = text.split(":", 1)
            label = label_part.strip()
            if not LABEL_RE.match(label):
                raise AssemblerError(f"line {line_no}: invalid label '{label}'")
            if label in labels:
                raise AssemblerError(f"line {line_no}: duplicate label '{label}'")
            labels[label] = pc
            text = rest.strip()
            if not text:
                break

        if not text:
            continue

        if pc > 0xFF:
            raise AssemblerError("program exceeds 256-word instruction memory")

        source.append(SourceLine(line_no, pc, raw.rstrip("\n"), text))
        pc += 1

    return labels, source


def encode_statement(stmt: str, labels: dict[str, int], pc: int) -> int:
    parts = stmt.strip().split(None, 1)
    mnemonic = parts[0].lower()
    operand_text = parts[1] if len(parts) == 2 else ""
    operands = split_operands(operand_text)

    # Convenience pseudo-instruction.
    if mnemonic == "nop":
        if operands:
            raise AssemblerError("nop takes no operands")
        # addi $zero, $zero, 0
        return (OPCODES["addi"] << 12)

    if mnemonic == ".word":
        if len(operands) != 1:
            raise AssemblerError("expected: .word <16-bit value>")
        value = parse_number(operands[0])
        if not 0 <= value <= 0xFFFF:
            raise AssemblerError(".word value must fit 16 bits (0..65535)")
        return value

    if mnemonic not in OPCODES:
        valid = ", ".join(OPCODES)
        raise AssemblerError(f"unknown instruction '{mnemonic}' (valid: {valid})")

    op = OPCODES[mnemonic]

    if mnemonic in R_TYPE:
        return encode_r(op, operands)
    if mnemonic in I_ARITH:
        return encode_i_arith(op, operands)
    if mnemonic in I_LOGIC:
        return encode_i_logic(op, operands)
    if mnemonic in SHIFT:
        return encode_shift(op, operands)
    if mnemonic in MEMORY:
        return encode_memory(op, mnemonic, operands)
    if mnemonic in BRANCH:
        return encode_branch(op, operands, labels, pc)
    if mnemonic == "j":
        return encode_jump(op, operands, labels)

    raise AssemblerError(f"internal error: no encoder for '{mnemonic}'")


def assemble(text: str) -> tuple[list[int], list[SourceLine]]:
    lines = text.splitlines()
    labels, source = first_pass(lines)
    words: list[int] = []

    for item in source:
        try:
            word = encode_statement(item.statement, labels, item.address)
        except AssemblerError as exc:
            raise AssemblerError(
                f"line {item.line_no}, address 0x{item.address:02X}: {exc}\n"
                f"    {item.text}"
            ) from exc
        words.append(word)

    return words, source


def write_logisim_image(path: Path, words: list[int]) -> None:
    # Logisim accepts whitespace-separated words after the header.
    rows = []
    for i in range(0, len(words), 8):
        rows.append(" ".join(f"{w:04x}" for w in words[i:i + 8]))
    body = "\n".join(rows)
    path.write_text("v2.0 raw\n" + body + ("\n" if body else ""), encoding="utf-8")


def write_listing(path: Path, words: list[int], source: list[SourceLine]) -> None:
    lines = [
        "ADDR  MACHINE              SOURCE",
        "----  -------------------  ----------------------------------------",
    ]
    for word, item in zip(words, source):
        binary = f"{word:016b}"
        grouped = " ".join(binary[i:i + 4] for i in range(0, 16, 4))
        lines.append(f"{item.address:02X}    {word:04X}  {grouped}  {item.text}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Assemble the custom 4-bit MIPS ISA into a Logisim ROM image."
    )
    parser.add_argument("source", type=Path, help="assembly source file (.asm)")
    parser.add_argument(
        "-o", "--output", type=Path,
        help="Logisim ROM image output (default: <source>.hex)"
    )
    parser.add_argument(
        "--listing", type=Path,
        help="optional human-readable listing file"
    )
    args = parser.parse_args()

    source_path: Path = args.source
    output_path: Path = args.output or source_path.with_suffix(".hex")

    try:
        text = source_path.read_text(encoding="utf-8")
        words, source = assemble(text)
        write_logisim_image(output_path, words)

        if args.listing:
            write_listing(args.listing, words, source)

    except (OSError, AssemblerError) as exc:
        print(f"Assembler error: {exc}", file=sys.stderr)
        return 1

    print(f"Assembled {len(words)} instruction(s).")
    print(f"Logisim ROM image: {output_path}")
    if args.listing:
        print(f"Listing:           {args.listing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
