# CSE 210: Computer Architecture Sessional

This repository contains the design, simulation files, specifications, and documentation for the **CSE 210: Computer Architecture Sessional** course offered by the Department of Computer Science and Engineering (CSE), **Bangladesh University of Engineering and Technology (BUET)**.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Assignments Summary](#assignments-summary)
  - [Assignment 1: IC-Level ALU Design](#assignment-1-ic-level-alu-design)
  - [Assignment 2: 16-Bit Floating Point Adder (FPA)](#assignment-2-16-bit-floating-point-adder-fpa)
  - [Assignment 3: 4-Bit Custom MIPS Processor](#assignment-3-4-bit-custom-mips-processor)
- [Tools & Requirements](#tools--requirements)
- [How to Run Simulations](#how-to-run-simulations)
- [Course Details](#course-details)

---

## 🔍 Overview

The experiments in this repository explore digital hardware architecture from low-level gate/IC design up to a full microprogrammed processor:
1. **ALU Design:** Combinational arithmetic and logic circuit design at the IC level with status flags.
2. **Floating-Point Arithmetic:** Implementation of a 16-bit IEEE-754 style floating-point adder featuring alignment, normalization, rounding, and flag detection.
3. **MIPS Processor:** Software/hardware specification and design of a microprogrammed 4-bit custom MIPS architecture.

---

## 📁 Repository Structure

```text
cse210-comparch/
├── Assignment-1-ALU/
│   ├── ALU.circ                                # Logisim circuit file for the ALU design
│   └── January_2026_CSE_210_Assignment_1_V0.pdf# Assignment 1 specification document
├── Assignment-2-FPA/
│   ├── FPA3.circ                               # Logisim circuit file for 16-bit Floating-Point Adder
│   ├── CSE210_Assignment2.pdf                  # Assignment 2 problem specification
│   ├── CSE210_Assignment2testcases.pdf         # Sample test cases and walkthrough
│   └── FPA_BlockDiagram.pdf                    # Hardware block diagram for FPA design
├── Assignment-3-MIPS/
│   └── Jan_2026_CSE_210_MIPS.pdf               # Assignment 3 specification (4-bit MIPS Processor)
└── README.md                                   # Repository documentation
```

---

## 💻 Assignments Summary

### Assignment 1: IC-Level ALU Design

- **Directory:** [`Assignment-1-ALU/`](file:///Users/shuvo/cse210-comparch/Assignment-1-ALU)
- **Circuit File:** [`ALU.circ`](file:///Users/shuvo/cse210-comparch/Assignment-1-ALU/ALU.circ)
- **Specification:** [`January_2026_CSE_210_Assignment_1_V0.pdf`](file:///Users/shuvo/cse210-comparch/Assignment-1-ALU/January_2026_CSE_210_Assignment_1_V0.pdf)

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

- **Directory:** [`Assignment-2-FPA/`](file:///Users/shuvo/cse210-comparch/Assignment-2-FPA)
- **Circuit File:** [`FPA3.circ`](file:///Users/shuvo/cse210-comparch/Assignment-2-FPA/FPA3.circ)
- **Documentation:** [`CSE210_Assignment2.pdf`](file:///Users/shuvo/cse210-comparch/Assignment-2-FPA/CSE210_Assignment2.pdf) | [`CSE210_Assignment2testcases.pdf`](file:///Users/shuvo/cse210-comparch/Assignment-2-FPA/CSE210_Assignment2testcases.pdf) | [`FPA_BlockDiagram.pdf`](file:///Users/shuvo/cse210-comparch/Assignment-2-FPA/FPA_BlockDiagram.pdf)

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

- **Directory:** [`Assignment-3-MIPS/`](file:///Users/shuvo/cse210-comparch/Assignment-3-MIPS)
- **Specification:** [`Jan_2026_CSE_210_MIPS.pdf`](file:///Users/shuvo/cse210-comparch/Assignment-3-MIPS/Jan_2026_CSE_210_MIPS.pdf)

#### Architecture Specifications:
- **Bus Widths:** 8-bit Address Bus, 4-bit Data Bus.
- **ALU:** Custom 4-bit Arithmetic Logic Unit.
- **Registers:** 6 4-bit registers (`$zero`, `$t0`, `$t1`, `$t2`, `$t3`, `$t4`).
- **Control Unit:** Microprogrammed control unit storing Control Words in Control Memory (ROM).
- **Instruction Formats (16-bit Instruction Length):**
  - **R-type:** `[Opcode: 4b | Src Reg 1: 4b | Src Reg 2: 4b | Dst Reg: 4b]`
  - **S-type:** `[Opcode: 4b | Src Reg 1: 4b | Dst Reg: 4b | Shift Amount: 4b]`
  - **I-type:** `[Opcode: 4b | Src Reg 1: 4b | Src/Dst Reg: 4b | Address/Immediate: 4b]`
  - **J-type:** `[Opcode: 4b | Target Jump Address: 8b | Unused: 4b]`
- **Instruction Set (16 Instructions):**
  - *Arithmetic:* `add`, `addi`, `sub`, `subi`
  - *Logic:* `and`, `andi`, `or`, `ori`, `sll`, `srl`, `nor`
  - *Memory:* `lw`, `sw`
  - *Control:* `beq`, `bneq`, `j`
- **Memory Units:** Instruction Memory (PC), Data Memory, and Stack Memory (sp).
- **Assembler:** Automatic conversion from MIPS assembly to binary machine code.

---

## 🛠️ Tools & Requirements

- **[Logisim](http://www.cburch.com/logisim/)** or **[Logisim-evolution](https://github.com/logisim-evolution/logisim-evolution)**: Used for running `.circ` simulation files (`ALU.circ`, `FPA3.circ`).
- **PDF Viewer**: For viewing problem specifications and block diagrams.
- **Python 3 / C++**: Recommended environment for building the custom MIPS assembler (Assignment 3).

---

## 🚀 How to Run Simulations

1. **Install Logisim:**
   Download and install Logisim or Logisim-evolution on your system.

2. **Open Circuit Files:**
   Launch Logisim and open the desired `.circ` file:
   - For ALU: `File` -> `Open` -> Select `Assignment-1-ALU/ALU.circ`
   - For Floating-Point Adder: `File` -> `Open` -> Select `Assignment-2-FPA/FPA3.circ`

3. **Simulate:**
   - Use the **Poke Tool** (`Ctrl+1` / `Cmd+1`) to toggle input pins and clock signals.
   - Enable simulation (`Simulate` -> `Simulation Enabled`).
   - For automated verification, observe output pins and flags ($C, S, V, Z$, Overflow, Underflow).

---

## 🎓 Course Details

- **Course Title:** Computer Architecture Sessional
- **Course Code:** CSE 210
- **Semester:** January 2026
- **Department:** Department of Computer Science and Engineering (CSE)
- **University:** Bangladesh University of Engineering and Technology (BUET)

---

*Maintained by [Shadman S. Shuvo](https://github.com/ShadmanSShuvo).*
