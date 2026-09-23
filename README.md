# CSE 210: Computer Architecture Sessional

This repository contains the digital logic designs, circuit simulation files, custom assemblers, specifications, and documentation for the **CSE 210: Computer Architecture Sessional** course offered by the Department of Computer Science and Engineering (CSE), **Bangladesh University of Engineering and Technology (BUET)**.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Assignments Summary](#assignments-summary)
  - [Assignment 1: IC-Level ALU Design](#assignment-1-ic-level-alu-design)
  - [Assignment 2: 16-Bit Floating Point Adder (FPA)](#assignment-2-16-bit-floating-point-adder-fpa)
  - [Assignment 3: 4-Bit Custom MIPS Processor](#assignment-3-4-bit-custom-mips-processor)
  - [MIPS Online Evaluation](#mips-online-evaluation)
- [Tools & Requirements](#tools--requirements)
- [How to Run Simulations](#how-to-run-simulations)
- [Course Details](#course-details)

---

## 🔍 Overview

The experiments in this repository explore digital hardware architecture from low-level SSI/MSI gate and IC design up to a full microprogrammed processor and software assembler:
1. **ALU Design:** Combinational arithmetic and logic circuit design at the IC level with status flags ($C, S, V, Z$).
2. **Floating-Point Arithmetic:** Implementation of a 16-bit IEEE-754 style floating-point adder featuring alignment, normalization, rounding, and flag detection.
3. **MIPS Processor & Assembler:** Software/hardware specification, Logisim circuit implementation of a microprogrammed 4-bit custom MIPS processor, accompanied by a custom Python CLI and GUI assembler.
4. **MIPS Assembly Programming:** Recursive procedures and stack frame handling for MIPS online examination preparation.

---

## 📁 Repository Structure

```text
cse210-comparch/
├── Assignment-1-ALU/
│   ├── ALU.circ                                # Logisim circuit file for the ALU design
│   └── January_2026_CSE_210_Assignment_1_V0.pdf# Assignment 1 specification document
│   ├── January_2026_CSE_210_Assignment_1_V0.pdf# Assignment 1 specification document
│   └── README.md                               # Detailed Assignment 1 technical documentation
├── Assignment-2-FPA/
│   ├── FPA3.circ                               # Logisim circuit file for 16-bit Floating-Point Adder
│   ├── CSE210_Assignment2.pdf                  # Assignment 2 problem specification
│   ├── CSE210_Assignment2testcases.pdf         # Sample test cases and walkthrough
│   └── FPA_BlockDiagram.pdf                    # Hardware block diagram for FPA design
│   ├── FPA_BlockDiagram.pdf                    # Hardware block diagram for FPA design
│   └── README.md                               # Detailed Assignment 2 technical documentation
├── Assignment-3-MIPS/
│   ├── MIPS.circ                               # Full Logisim circuit for 4-bit MIPS processor
│   ├── mips4_assembler.py                      # Python CLI assembler (generates Logisim ROM hex)
│   ├── mips4_assembler_gui.py                  # Graphical Tkinter interface for the assembler
│   ├── code.asm / code.hex / code.lst          # Comprehensive ISA test program & assembled files
│   ├── program.asm / program.hex / program.lst # Quick-start demo program & assembled files
│   ├── Jan_2026_CSE_210_MIPS.pdf               # Assignment 3 specification sheet
│   ├── MIPS-code.pdf                           # Reference test codes and microinstruction notes
│   └── README.md                               # Detailed Assignment 3 technical documentation
├── MIPS-Online/
│   ├── MIPS_Online.pdf                         # MIPS Online exam problem sheet
│   └── README.md                               # Detailed MIPS assembly solutions & recursion notes
├── .gitignore                                  # Git ignore rules for Python & OS files
└── README.md                                   # Root repository documentation
```

---

## 💻 Assignments Summary

### Assignment 1: IC-Level ALU Design

- **Directory:** [`Assignment-1-ALU/`](./Assignment-1-ALU)
- **Circuit File:** [`ALU.circ`](./Assignment-1-ALU/ALU.circ)
- **Specification:** [`January_2026_CSE_210_Assignment_1_V0.pdf`](./Assignment-1-ALU/January_2026_CSE_210_Assignment_1_V0.pdf)
- **Documentation:** [`Assignment-1-ALU/README.md`](./Assignment-1-ALU/README.md) | [`January_2026_CSE_210_Assignment_1_V0.pdf`](./Assignment-1-ALU/January_2026_CSE_210_Assignment_1_V0.pdf)

#### Key Highlights:
- **Design Constraints:** Constructed using SSI (AND, OR, NOT, XOR) and MSI chips (Multiplexers, Adders, Decoders). The combinational logic driving the parallel adder consists strictly of SSI components.
- **Status Flags:**
  - **Carry ($C$):** Reflects arithmetic carry out.
  - **Sign ($S$):** Indicates negative results in 2's complement representation.
  - **Overflow ($V$):** Indicates signed arithmetic overflow.
  - **Zero ($Z$):** Set when output is zero.
- **Operations Supported:**
  - *Arithmetic:* Addition, Subtraction, Add with Carry, Subtract with Borrow, Increment, Decrement, Transfer.
  - *Logical:* Bitwise AND, Bitwise OR, Bitwise XOR, Bitwise NOT.

---

### Assignment 2: 16-Bit Floating Point Adder (FPA)

- **Directory:** [`Assignment-2-FPA/`](./Assignment-2-FPA)
- **Circuit File:** [`FPA3.circ`](./Assignment-2-FPA/FPA3.circ)
- **Documentation:** [`Assignment-2-FPA/README.md`](./Assignment-2-FPA/README.md) | [`CSE210_Assignment2.pdf`](./Assignment-2-FPA/CSE210_Assignment2.pdf) | [`CSE210_Assignment2testcases.pdf`](./Assignment-2-FPA/CSE210_Assignment2testcases.pdf) | [`FPA_BlockDiagram.pdf`](./Assignment-2-FPA/FPA_BlockDiagram.pdf)

#### 16-Bit Floating-Point Format:
| Sign ($S$) | Exponent ($E$) | Fraction / Mantissa ($F$) |
| :---: | :---: | :---: |
| 1 bit (Bit 15) | 5 bits (Bits 14–10, Bias = 15) | 10 bits (Bits 9–0, Implicit `1.F`) |

#### Hardware Features & Pipeline:
1. **Exponent Difference & Mantissa Alignment:** Calculates exponent difference and right-shifts smaller operand mantissa.
2. **Mantissa Addition/Subtraction:** Performs 2's complement addition/subtraction depending on operand sign bits.
3. **Normalization:** Handles sums $\ge 2.0$ (right-shift mantissa and increment exponent) and subnormal results (left-shift and decrement exponent).
4. **Rounding Logic:** Utilizes Guard ($G$), Round ($R$), and Sticky ($S$) bits to perform round-to-nearest rounding.
5. **Flag Generation:** Hardware detection for **Overflow** and **Underflow** conditions.

---

### Assignment 3: 4-Bit Custom MIPS Processor

- **Directory:** [`Assignment-3-MIPS/`](./Assignment-3-MIPS)
- **Circuit File:** [`MIPS.circ`](./Assignment-3-MIPS/MIPS.circ)
- **Documentation:** [`Assignment-3-MIPS/README.md`](./Assignment-3-MIPS/README.md) | [`Jan_2026_CSE_210_MIPS.pdf`](./Assignment-3-MIPS/Jan_2026_CSE_210_MIPS.pdf) | [`MIPS-code.pdf`](./Assignment-3-MIPS/MIPS-code.pdf)

#### Architecture Specifications:
- **Bus Widths:** 8-bit Address Bus, 4-bit Data Bus.
- **ALU:** Custom 4-bit Arithmetic Logic Unit supporting arithmetic, bitwise logic, and shifts (`sll`, `srl`).
- **Registers:** 6 4-bit General Purpose Registers (`$zero`, `$t0`, `$t1`, `$t2`, `$t3`, `$t4`) and hardware `$sp` code (`0110`).
- **Control Unit:** Microprogrammed control unit storing Control Words in Control Memory (ROM).
- **Instruction Formats (16-bit Instruction Length):**
  - **R-type:** `[Opcode: 4b | rs: 4b | rt: 4b | rd: 4b]`
  - **S-type:** `[Opcode: 4b | rs: 4b | rd: 4b | shamt: 4b]`
  - **I-type:** `[Opcode: 4b | rs: 4b | rt: 4b | Immediate/Offset: 4b]`
  - **J-type:** `[Opcode: 4b | Target Jump Address: 8b | Unused: 4b]`
- **Dedicated Stack Hardware:** Auto-adjusting stack operations via pseudo-instructions `push $reg` and `pop $reg`.
- **Custom Assembler:**
  - CLI: `python3 Assignment-3-MIPS/mips4_assembler.py input.asm -o output.hex --listing output.lst`
  - GUI: `python3 Assignment-3-MIPS/mips4_assembler_gui.py`

---

### MIPS Online Evaluation

- **Directory:** [`MIPS-Online/`](./MIPS-Online)
- **Documentation:** [`MIPS-Online/README.md`](./MIPS-Online/README.md) | [`MIPS_Online.pdf`](./MIPS-Online/MIPS_Online.pdf)

Contains handwritten and verified 32-bit MIPS assembly routines translating complex recursive C functions (`splitScore`, `arrayScore`) with detailed walkthroughs on stack frame allocation, preserving `$ra`, and argument restoration.

---

## 🛠️ Tools & Requirements

- **[Logisim](http://www.cburch.com/logisim/)** or **[Logisim-evolution](https://github.com/logisim-evolution/logisim-evolution)**: Used for opening and running `.circ` simulation files (`ALU.circ`, `FPA3.circ`, `MIPS.circ`).
- **Python 3.8+**: Used to run `mips4_assembler.py` and `mips4_assembler_gui.py` (standard `tkinter` included).
- **PDF Viewer**: For viewing problem specifications, test cases, and block diagrams.

---

## 🚀 How to Run Simulations

1. **Install Logisim:**
   Download and install Logisim or Logisim-evolution on your system.

2. **Open Circuit Files:**
   Launch Logisim and open the desired `.circ` file:
   - For ALU: `File` -> `Open` -> Select `Assignment-1-ALU/ALU.circ`
   - For Floating-Point Adder: `File` -> `Open` -> Select `Assignment-2-FPA/FPA3.circ`
   - For 4-bit MIPS Processor: `File` -> `Open` -> Select `Assignment-3-MIPS/MIPS.circ`

3. **Running Programs on the MIPS Processor:**
   - Assemble your `.asm` code using the assembler:
     ```bash
     python3 Assignment-3-MIPS/mips4_assembler.py Assignment-3-MIPS/code.asm
     ```
   - In Logisim, right-click the **Instruction ROM** $\rightarrow$ **Load Image...** $\rightarrow$ choose `code.hex`.
   - Enable clock simulation (`Ctrl+K` / `Cmd+K`) and observe the execution across registers and memory.

---

## 🎓 Course Details

- **Course Title:** Computer Architecture Sessional
- **Course Code:** CSE 210
- **Semester:** January 2026
- **Department:** Department of Computer Science and Engineering (CSE)
- **University:** Bangladesh University of Engineering and Technology (BUET)

---

*Maintained by [Shadman S. Shuvo](https://github.com/ShadmanSShuvo).*
