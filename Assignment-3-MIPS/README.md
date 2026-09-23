# Assignment 3: 4-Bit Custom MIPS Processor

This directory contains the circuit implementation, custom assembler tools, test programs, and official specifications for the **4-bit Custom MIPS Processor** designed for the CSE 210 Computer Architecture Sessional course at BUET.

---

## 📑 Table of Contents

- [Overview & Architecture](#overview--architecture)
- [Instruction Set Architecture (ISA)](#instruction-set-architecture-isa)
  - [Opcode Table](#opcode-table)
  - [Instruction Formats](#instruction-formats)
  - [Registers](#registers)
- [Special Hardware & Assembler Features](#special-hardware--assembler-features)
  - [Dedicated Stack Support (`push` / `pop`)](#dedicated-stack-support-push--pop)
  - [Automatic Far-Branch Expansion](#automatic-far-branch-expansion)
- [Assembler Tooling](#assembler-tooling)
  - [Command-Line Assembler (`mips4_assembler.py`)](#command-line-assembler-mips4_assemblerpy)
  - [Graphical Assembler (`mips4_assembler_gui.py`)](#graphical-assembler-mips4_assembler_guipy)
- [Simulating in Logisim](#simulating-in-logisim)
- [File Manifest](#file-manifest)

---

## 🔍 Overview & Architecture

The custom processor is an 8-bit addressable, 4-bit word microprogrammed processor implementing a subset of the MIPS architecture tailored with custom opcodes and specialized instructions.

### Hardware Specifications:
- **Data Bus Width:** 4 bits
- **Address Bus Width:** 8 bits (addresses 256 memory locations: `0x00` - `0xFF`)
- **Instruction Width:** 16 bits (stored in Instruction ROM)
- **ALU Operations:** 4-bit Arithmetic Logic Unit supporting addition, subtraction, AND, OR, NOR, and shifts
- **Control Unit:** Microprogrammed Control Unit using Control ROM to issue control signals
- **Memory Subsystems:**
  - **Instruction Memory (ROM):** 8-bit addressing for fetching 16-bit instructions.
  - **Data Memory (RAM):** 8-bit addressing for 4-bit data storage (`0x00` - `0xEF`).
  - **Stack Memory:** Hardware managed via dedicated 8-bit Stack Pointer (`$sp`), initialized to `0xFF` and growing downwards.

---

## 📐 Instruction Set Architecture (ISA)

The processor supports 16 core instructions formatted into 16-bit words.

### Opcode Table

| Mnemonic | Opcode (Hex) | Opcode (Binary) | Format | Description |
| :--- | :---: | :---: | :---: | :--- |
| `beq`  | `0x0` | `0000` | I-type | Branch if equal: `if (R[rs] == R[rt]) PC = PC + 1 + offset` |
| `ori`  | `0x1` | `0001` | I-type | Bitwise OR immediate: `R[rt] = R[rs] \| imm` |
| `subi` | `0x2` | `0010` | I-type | Subtract immediate: `R[rt] = R[rs] - imm` |
| `sll`  | `0x3` | `0011` | S-type | Shift left logical: `R[rd] = R[rs] << shamt` |
| `add`  | `0x4` | `0100` | R-type | Add: `R[rd] = R[rs] + R[rt]` |
| `srl`  | `0x5` | `0101` | S-type | Shift right logical: `R[rd] = R[rs] >> shamt` |
| `and`  | `0x6` | `0110` | R-type | Bitwise AND: `R[rd] = R[rs] & R[rt]` |
| `sw`   | `0x7` | `0111` | I-type | Store word: `Mem[R[rs] + offset] = R[rt]` |
| `nor`  | `0x8` | `1000` | R-type | Bitwise NOR: `R[rd] = ~(R[rs] \| R[rt])` |
| `addi` | `0x9` | `1001` | I-type | Add immediate: `R[rt] = R[rs] + imm` |
| `bneq` | `0xA` | `1010` | I-type | Branch if not equal: `if (R[rs] != R[rt]) PC = PC + 1 + offset` |
| `sub`  | `0xB` | `1011` | R-type | Subtract: `R[rd] = R[rs] - R[rt]` |
| `andi` | `0xC` | `1100` | I-type | Bitwise AND immediate: `R[rt] = R[rs] & imm` |
| `lw`   | `0xD` | `1101` | I-type | Load word: `R[rt] = Mem[R[rs] + offset]` |
| `j`    | `0xE` | `1110` | J-type | Unconditional jump: `PC = target` |
| `or`   | `0xF` | `1111` | R-type | Bitwise OR: `R[rd] = R[rs] \| R[rt]` |

---

### Instruction Formats

All instructions are fixed 16 bits wide:

#### 1. R-Type (Register)
```text
 15        12 11        8 7         4 3         0
+------------+-----------+-----------+-----------+
|   Opcode   |    rs     |    rt     |    rd     |
|   (4 bits) |  (4 bits) |  (4 bits) |  (4 bits) |
+------------+-----------+-----------+-----------+
```
Used by: `add`, `sub`, `and`, `or`, `nor`

#### 2. S-Type (Shift)
```text
 15        12 11        8 7         4 3         0
+------------+-----------+-----------+-----------+
|   Opcode   |    rs     |    rd     |   shamt   |
|   (4 bits) |  (4 bits) |  (4 bits) |  (4 bits) |
+------------+-----------+-----------+-----------+
```
Used by: `sll`, `srl`

#### 3. I-Type (Immediate / Memory / Branch)
```text
 15        12 11        8 7         4 3         0
+------------+-----------+-----------+-----------+
|   Opcode   |    rs     |    rt     | Immediate |
|   (4 bits) |  (4 bits) |  (4 bits) |  (4 bits) |
+------------+-----------+-----------+-----------+
```
- Arithmetic/Logic (`addi`, `subi`, `andi`, `ori`): `rt` = destination, `rs` = source, `Immediate` = 4-bit constant.
- Memory (`lw`, `sw`): `rs` = base register, `rt` = target/source register, `Immediate` = 4-bit offset.
- Branch (`beq`, `bneq`): `rs` & `rt` = compared registers, `Immediate` = signed 4-bit PC-relative offset (range: `[-8, +7]`).

#### 4. J-Type (Jump)
```text
 15        12 11                     4 3         0
+------------+------------------------+-----------+
|   Opcode   |  Target Jump Address   |  Unused   |
|   (4 bits) |        (8 bits)        |  (4 bits) |
+------------+------------------------+-----------+
```
Used by: `j` (Target address is an 8-bit absolute address).

---

### Registers

The processor defines 6 General Purpose Registers (GPRs) and 1 special hardware register code:

| Register Name | Binary Code | Hex | Purpose |
| :--- | :---: | :---: | :--- |
| `$zero` | `0000` | `0x0` | Constant 0 (hardwired) |
| `$t0`   | `0001` | `0x1` | Temporary Register 0 |
| `$t1`   | `0010` | `0x2` | Temporary Register 1 |
| `$t2`   | `0011` | `0x3` | Temporary Register 2 |
| `$t3`   | `0100` | `0x4` | Temporary Register 3 |
| `$t4`   | `0101` | `0x5` | Temporary Register 4 |
| `$sp`   | `0110` | `0x6` | *Stack Pointer hardware code (used for stack operations)* |

---

## ⚙️ Special Hardware & Assembler Features

### Dedicated Stack Support (`push` / `pop`)
Instead of software-managed pointer increments and decrements, this processor features dedicated hardware stack paths:
- **`push $reg`**: Assembled into `sw` with base register code `0110` (`$sp`). The hardware pushes the value of `$reg` to `Mem[SP]` and decrements `SP` automatically.
- **`pop $reg`**: Assembled into `lw` with base register code `0110` (`$sp`). The hardware increments `SP` and loads the value from `Mem[SP]` into `$reg`.
- **Note:** Standard `lw`/`sw` operations using `$sp` with an offset are disallowed; stack operations are performed via `push` and `pop`.

### Automatic Far-Branch Expansion
In 4-bit MIPS, conditional branch offsets are limited to 4-bit signed integers ($-8 \dots +7$).
When a branch target is out of this range:
- The assembler automatically **inverts the branch condition** to jump over an unconditional `j` instruction.
- *Example:*
  ```asm
  beq $t0, $t1, far_label
  ```
  Expands to:
  ```asm
  bneq $t0, $t1, skip_jump
  j far_label
  skip_jump:
  ```

---

## 🛠️ Assembler Tooling

This repository includes both a Python CLI assembler and an intuitive Tkinter GUI.

### Command-Line Assembler (`mips4_assembler.py`)

Run the assembler directly from the terminal:

```bash
# Basic usage (outputs <file>.hex)
python3 Assignment-3-MIPS/mips4_assembler.py Assignment-3-MIPS/code.asm

# Specify output hex file and machine-code listing file
python3 Assignment-3-MIPS/mips4_assembler.py Assignment-3-MIPS/code.asm \
  -o Assignment-3-MIPS/code.hex \
  --listing Assignment-3-MIPS/code.lst
```

#### Output formats:
1. **`.hex`**: Logisim Evolution v2.0 raw ROM image format (`v2.0 raw` header followed by 16-bit hex values).
2. **`.lst`**: Formatted listing detailing addresses, machine code, bit breakdown, and source statements.

---

### Graphical Assembler (`mips4_assembler_gui.py`)

A graphical interface for writing, assembling, and inspecting machine code:

```bash
python3 Assignment-3-MIPS/mips4_assembler_gui.py
```

**Features:**
- Split-pane interface displaying assembly source code and machine code listings side by side.
- Real-time syntax validation and clear error highlighting with line numbers.
- One-click ROM image generation and export for Logisim.

---

## 💻 Simulating in Logisim

1. **Launch Logisim:**
   Open `MIPS.circ` in [Logisim or Logisim-Evolution](https://github.com/logisim-evolution/logisim-evolution):
   ```bash
   logisim Assignment-3-MIPS/MIPS.circ
   ```
2. **Load Program into Instruction ROM:**
   - Locate the **Instruction Memory / ROM** component in the circuit.
   - Right-click the ROM $\rightarrow$ Select **Load Image...**
   - Choose `code.hex` or your newly assembled `.hex` file.
3. **Execute:**
   - Ensure the Clock is enabled (`Simulate` $\rightarrow$ `Ticks Enabled` or press `Ctrl+K` / `Cmd+K`).
   - Observe register values in the Register File and verify memory updates.

---

## 📂 File Manifest

- [`MIPS.circ`](./MIPS.circ): Complete Logisim circuit file for the 4-bit MIPS processor.
- [`mips4_assembler.py`](./mips4_assembler.py): Python CLI assembler translating custom assembly to Logisim ROM hex format.
- [`mips4_assembler_gui.py`](./mips4_assembler_gui.py): GUI front-end for the assembler.
- [`code.asm`](./code.asm) / [`code.hex`](./code.hex) / [`code.lst`](./code.lst): Comprehensive test assembly suite covering arithmetic, logic, memory, branching, and stack operations.
- [`program.asm`](./program.asm) / [`program.hex`](./program.hex) / [`program.lst`](./program.lst): Quick-start demo program.
- [`Jan_2026_CSE_210_MIPS.pdf`](./Jan_2026_CSE_210_MIPS.pdf): Official Assignment 3 specification sheet from BUET CSE.
- [`MIPS-code.pdf`](./MIPS-code.pdf): Reference document with sample programs and test configurations.
