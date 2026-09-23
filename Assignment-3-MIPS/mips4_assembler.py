#!/usr/bin/env python3
"""
4-bit MIPS assembler for the CSE 210 custom ISA.

Supports:
- All 16 group-specific instructions
- Labels
- Logisim Evolution v2.0 raw ROM output
- Dedicated stack operation code in the base-register field ($sp code = 0110)
- push/pop pseudo-instructions
- Automatic far conditional-branch expansion

Stack behavior:
    push/pop use base field 0110.
    Normal lw/sw with $sp are intentionally rejected by the assembler.
    The MEMORY_UNIT interprets base code 0110 as the special stack path
    and updates the 8-bit SP automatically.

Far branches:
    A beq/bneq whose label is outside the signed 4-bit branch range (-8..+7)
    is automatically expanded to the inverse branch + absolute jump.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

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

GPR_REGISTERS = {
    "$zero": 0x0,
    "$t0":   0x1,
    "$t1":   0x2,
    "$t2":   0x3,
    "$t3":   0x4,
    "$t4":   0x5,
}

SP_CODE = 0x6

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
        try:
            return int(token, 10)
        except ValueError as exc:
            raise AssemblerError(f"invalid number '{token}'") from exc


def reg(token: str) -> int:
    name = token.strip().lower()
    if name == "$sp":
        raise AssemblerError(
            "$sp is a dedicated 8-bit stack pointer; use it only as a memory base or via push/pop"
        )
    if name not in GPR_REGISTERS:
        valid = ", ".join(GPR_REGISTERS)
        raise AssemblerError(f"unknown register '{token}' (valid: {valid})")
    return GPR_REGISTERS[name]


def base_reg(token: str) -> int:
    name = token.strip().lower()
    if name == "$sp":
        raise AssemblerError(
            "$sp cannot be used with normal lw/sw; use push or pop instead"
        )
    return reg(token)


def signed4(value: int, what: str) -> int:
    if not -8 <= value <= 7:
        raise AssemblerError(f"{what} {value} does not fit signed 4-bit range -8..7")
    return value & 0xF


def bits4(value: int, what: str) -> int:
    if not -8 <= value <= 15:
        raise AssemblerError(
            f"{what} {value} does not fit a 4-bit field "
            f"(use -8..7 signed or 0..15 as a bit pattern)"
        )
    return value & 0xF


def split_operands(text: str) -> list[str]:
    return [x.strip() for x in text.split(",") if x.strip()]


def encode_r(op: int, operands: list[str]) -> int:
    if len(operands) != 3:
        raise AssemblerError("expected: $dst, $src1, $src2")
    dst, src1, src2 = map(reg, operands)
    return (op << 12) | (src1 << 8) | (src2 << 4) | dst


def encode_i_arith(op: int, operands: list[str]) -> int:
    if len(operands) != 3:
        raise AssemblerError("expected: $dst, $src1, immediate")
    dst = reg(operands[0])
    src1 = reg(operands[1])
    imm = signed4(parse_number(operands[2]), "immediate")
    return (op << 12) | (src1 << 8) | (dst << 4) | imm


def encode_i_logic(op: int, operands: list[str]) -> int:
    if len(operands) != 3:
        raise AssemblerError("expected: $dst, $src1, immediate")
    dst = reg(operands[0])
    src1 = reg(operands[1])
    imm = bits4(parse_number(operands[2]), "immediate")
    return (op << 12) | (src1 << 8) | (dst << 4) | imm


def encode_shift(op: int, operands: list[str]) -> int:
    if len(operands) != 3:
        raise AssemblerError("expected: $dst, $src1, shamt")
    dst = reg(operands[0])
    src1 = reg(operands[1])
    shamt = parse_number(operands[2])
    if not 0 <= shamt <= 3:
        raise AssemblerError("shift amount must be 0..3 for a 4-bit datapath")
    return (op << 12) | (src1 << 8) | (dst << 4) | shamt


def encode_memory(op: int, mnemonic: str, operands: list[str]) -> int:
    if len(operands) != 2:
        if mnemonic == "lw":
            raise AssemblerError("expected: $dst, offset($base)")
        raise AssemblerError("expected: $src, offset($base)")

    data_reg = reg(operands[0])

    match = MEM_RE.match(operands[1].replace(" ", ""))
    if not match:
        raise AssemblerError("memory operand must look like offset($base), e.g. 3($t1)")

    offset_text, base_text = match.groups()
    base = base_reg(base_text)
    offset = signed4(parse_number(offset_text), "memory offset")

    return (op << 12) | (base << 8) | (data_reg << 4) | offset


def encode_push_pop(mnemonic: str, operands: list[str]) -> int:
    if len(operands) != 1:
        raise AssemblerError(f"expected: {mnemonic} $register")

    data_reg = reg(operands[0])
    op = OPCODES["sw"] if mnemonic == "push" else OPCODES["lw"]

    # offset = 0, base field = 0110.
    # MEMORY_UNIT interprets 0110 as the automatic stack path.
    return (op << 12) | (SP_CODE << 8) | (data_reg << 4)


def encode_branch(op: int, operands: list[str], labels: dict[str, int], pc: int) -> int:
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
    if len(operands) != 1:
        raise AssemblerError("expected: label_or_address")

    target_text = operands[0]
    target = labels[target_text] if target_text in labels else parse_number(target_text)

    if not 0 <= target <= 0xFF:
        raise AssemblerError(f"jump target {target} does not fit 8 bits (0..255)")

    return (op << 12) | (target << 4)


def _layout_source(
    lines: list[str],
    expanded_lines: set[int],
) -> tuple[dict[str, int], list[SourceLine]]:
    """
    Assign physical ROM addresses.

    A source branch listed in expanded_lines occupies two ROM words:
        inverse-branch + jump
    Everything else occupies one word.
    """
    labels: dict[str, int] = {}
    source: list[SourceLine] = []
    pc = 0

    for line_no, raw in enumerate(lines, start=1):
        text = clean_line(raw)
        if not text:
            continue

        # Supports:
        #   label:
        #   label: instruction
        # and even multiple labels on the same source line.
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

        size = 2 if line_no in expanded_lines else 1

        if pc + size > 0x100:
            raise AssemblerError("program exceeds 256-word instruction memory")

        source.append(SourceLine(line_no, pc, raw.rstrip("\\n"), text))
        pc += size

    return labels, source


def _branch_parts(statement: str) -> tuple[str, list[str]] | None:
    """Return (mnemonic, operands) for beq/bneq, otherwise None."""
    parts = statement.strip().split(None, 1)
    if not parts:
        return None

    mnemonic = parts[0].lower()
    if mnemonic not in BRANCH:
        return None

    operand_text = parts[1] if len(parts) == 2 else ""
    operands = split_operands(operand_text)
    return mnemonic, operands


def first_pass(
    lines: list[str],
) -> tuple[dict[str, int], list[SourceLine], set[int]]:
    """
    Compute final addresses and determine which label-based conditional
    branches must be expanded.

    Expansion is monotonic: adding an extra word can only keep or increase
    label distances, so the loop converges quickly.
    """
    expanded_lines: set[int] = set()

    while True:
        labels, source = _layout_source(lines, expanded_lines)
        newly_far: set[int] = set()

        for item in source:
            parsed = _branch_parts(item.statement)
            if parsed is None:
                continue

            mnemonic, operands = parsed

            # Let the normal encoder report malformed branch syntax later.
            if len(operands) != 3:
                continue

            target = operands[2]

            # Numeric branch operands are explicit offsets, not labels.
            # Keep the original signed-4-bit validation for those.
            if target not in labels:
                continue

            offset = labels[target] - (item.address + 1)

            if not -8 <= offset <= 7:
                newly_far.add(item.line_no)

        if newly_far.issubset(expanded_lines):
            return labels, source, expanded_lines

        expanded_lines |= newly_far

def encode_statement(stmt: str, labels: dict[str, int], pc: int) -> int:
    parts = stmt.strip().split(None, 1)
    mnemonic = parts[0].lower()
    operand_text = parts[1] if len(parts) == 2 else ""
    operands = split_operands(operand_text)

    if mnemonic == "nop":
        if operands:
            raise AssemblerError("nop takes no operands")
        return OPCODES["addi"] << 12  # 0x9000

    if mnemonic == ".word":
        if len(operands) != 1:
            raise AssemblerError("expected: .word <16-bit value>")
        value = parse_number(operands[0])
        if not 0 <= value <= 0xFFFF:
            raise AssemblerError(".word value must fit 16 bits (0..65535)")
        return value

    if mnemonic in {"push", "pop"}:
        return encode_push_pop(mnemonic, operands)

    if mnemonic not in OPCODES:
        valid = ", ".join(list(OPCODES) + ["push", "pop", "nop"])
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



def _has_terminal_label_only(lines: list[str]) -> bool:
    """
    True when the last meaningful source line contains only one or more labels
    and no instruction, e.g.:
        end:
    """
    for raw in reversed(lines):
        text = clean_line(raw)
        if not text:
            continue

        saw_label = False
        while ":" in text:
            label_part, rest = text.split(":", 1)
            label = label_part.strip()

            if not LABEL_RE.match(label):
                return False

            saw_label = True
            text = rest.strip()

            if not text:
                return saw_label

        return False

    return False


def assemble(text: str) -> tuple[list[int], list[SourceLine]]:
    lines = text.splitlines()
    labels, source, expanded_lines = first_pass(lines)

    words: list[int] = []
    listing_source: list[SourceLine] = []

    for item in source:
        try:
            if item.line_no in expanded_lines:
                parsed = _branch_parts(item.statement)
                if parsed is None:
                    raise AssemblerError("internal error: non-branch marked for far expansion")

                mnemonic, operands = parsed
                if len(operands) != 3:
                    raise AssemblerError("expected: $src1, $src2, label")

                target = operands[2]
                if target not in labels:
                    raise AssemblerError(
                        "far-branch expansion requires a label target"
                    )

                # Invert the condition so the taken inverse branch skips
                # over the inserted jump:
                #
                #   original: bneq r1,r2,target
                #
                #   becomes:  beq  r1,r2,+1
                #             j    target
                #
                # With PC+1-relative branches, +1 lands at PC+2.
                inverse = "bneq" if mnemonic == "beq" else "beq"

                branch_word = encode_branch(
                    OPCODES[inverse],
                    [operands[0], operands[1], "1"],
                    labels,
                    item.address,
                )
                jump_word = encode_jump(
                    OPCODES["j"],
                    [target],
                    labels,
                )

                words.extend([branch_word, jump_word])

                listing_source.append(
                    SourceLine(
                        item.line_no,
                        item.address,
                        item.text + "    [far branch expanded]",
                        item.statement,
                    )
                )
                listing_source.append(
                    SourceLine(
                        item.line_no,
                        item.address + 1,
                        f"    [assembler] j {target}",
                        f"j {target}",
                    )
                )
            else:
                word = encode_statement(item.statement, labels, item.address)
                words.append(word)
                listing_source.append(item)

        except AssemblerError as exc:
            raise AssemblerError(
                f"line {item.line_no}, address 0x{item.address:02X}: {exc}\\n"
                f"    {item.text}"
            ) from exc

    # If the program ends with a bare label such as:
    #
    #     end:
    #
    # that label points to the next ROM address. Put an explicit self-loop
    # there so execution stops visibly instead of falling through into
    # unused ROM (which contains 0000 = beq $zero,$zero,0).
    #
    # With PC+1-relative branches:
    #     beq $zero,$zero,-1
    # loops to its own address.
    if _has_terminal_label_only(lines):
        halt_pc = len(words)

        if halt_pc > 0xFF:
            raise AssemblerError("program exceeds 256-word instruction memory")

        halt_word = (
            (OPCODES["beq"] << 12)
            | (GPR_REGISTERS["$zero"] << 8)
            | (GPR_REGISTERS["$zero"] << 4)
            | 0xF
        )

        words.append(halt_word)
        listing_source.append(
            SourceLine(
                0,
                halt_pc,
                "    [assembler] terminal self-loop",
                "beq $zero, $zero, -1",
            )
        )

    return words, listing_source

def write_logisim_image(path: Path, words: list[int]) -> None:
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
