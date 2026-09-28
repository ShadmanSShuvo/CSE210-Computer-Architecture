You are an expert Computer Architecture teaching assistant and LaTeX technical-document author.

Your task is to create a COMPLETE, QUIZ-ORIENTED MASTER NOTE in LaTeX for my CSE210 Computer Architecture quiz tomorrow.

IMPORTANT:
- Do NOT create a generic Computer Architecture textbook.
- The notes must be based PRIMARILY on the actual contents of this repository.
- Inspect ALL relevant files before writing the notes.
- Infer what concepts are likely quiz-relevant from the assignments, PDFs, README files, circuit files, MIPS code, and test cases.
- The final document should be optimized for LAST-MINUTE REVISION: dense, precise, structured, and easy to scan.
- Explain concepts enough that I can actually understand/reconstruct them during the quiz.
- Include formulas, tables, diagrams where useful, worked examples, common mistakes, and likely quiz traps.
- Do not omit small details merely because they seem obvious. Quiz questions often target implementation details.

==================================================
REPOSITORY
==================================================

Current repository:

CSE210-CompArch
├── Assignment-1-ALU
│   ├── ALU.circ
│   ├── January_2026_CSE_210_Assignment_1_V0.pdf
│   └── README.md
├── Assignment-2-FPA
│   ├── CSE210_Assignment2.pdf
│   ├── CSE210_Assignment2testcases.pdf
│   ├── FPA3.circ
│   ├── FPA_BlockDiagram.pdf
│   └── README.md
├── Assignment-3-MIPS
│   ├── Jan_2026_CSE_210_MIPS.pdf
│   ├── MIPS-code.pdf
│   ├── MIPS.circ
│   ├── README.md
│   ├── code.asm
│   ├── code.hex
│   ├── code.lst
│   ├── mips4_assembler.py
│   ├── mips4_assembler_gui.py
│   ├── program.asm
│   ├── program.hex
│   └── program.lst
├── MIPS-Online
│   ├── MIPS_Online.pdf
│   └── README.md
└── README.md

==================================================
PHASE 1 — REPOSITORY FORENSICS
==================================================

Before creating the final notes, thoroughly inspect the repository.

1. Read:
   - root README.md
   - every assignment README.md

2. Extract and inspect ALL PDFs:
   - Assignment 1 PDF
   - Assignment 2 PDF
   - Assignment 2 test cases PDF
   - FPA block diagram PDF
   - Assignment 3 MIPS PDF
   - MIPS-code PDF
   - MIPS Online PDF

3. Inspect circuit files:
   - ALU.circ
   - FPA3.circ
   - MIPS.circ

   If these are Logisim/Logisim Evolution circuit files, inspect their XML/text structure and identify:
   - inputs
   - outputs
   - components
   - subcircuits
   - buses
   - control signals
   - multiplexers
   - adders
   - registers
   - ALU structure
   - datapaths
   - special implementation details

   Do NOT simply mention that the circuit exists. Extract its architecture.

4. Inspect ALL assembly/code files:
   - code.asm
   - program.asm
   - code.hex
   - program.hex
   - code.lst
   - program.lst
   - mips4_assembler.py
   - mips4_assembler_gui.py

5. Cross-reference the PDFs against the actual implementations.

6. Identify:
   - concepts explicitly taught
   - concepts required to complete assignments
   - implementation-specific details
   - terminology used by the course
   - instruction formats
   - datapath/control details
   - numerical representations
   - likely calculation questions
   - likely conceptual MCQs
   - likely trace/debug questions
   - common implementation mistakes

If a PDF contains important diagrams or screenshots, inspect them rather than relying only on extracted text.

==================================================
PHASE 2 — BUILD THE KNOWLEDGE MAP
==================================================

From the repository, construct a CSE210-specific knowledge map.

At minimum investigate whether the repository covers:

A. ALU / Digital Datapath
- binary arithmetic
- addition/subtraction
- two's complement
- overflow
- carry
- flags
- bitwise operations
- AND/OR/XOR/NOT
- comparators
- multiplexers
- ALU control
- ALU block structure
- zero detection
- signed vs unsigned behavior
- any assignment-specific ALU operations

B. Floating Point Arithmetic / FPA
- floating-point representation
- sign/exponent/mantissa
- normalization
- exponent alignment
- addition/subtraction
- multiplication/division if present
- rounding if present
- special cases if present
- overflow/underflow if present
- hardware datapath
- control signals
- exact FPA implementation in FPA3.circ
- all test cases from the test-case PDF

C. MIPS
- MIPS architecture
- registers
- register conventions if relevant
- instruction formats
- R/I/J formats
- opcode
- funct
- rs/rt/rd
- shamt
- immediate
- address/target fields
- arithmetic instructions
- logical instructions
- shifts
- comparison
- load/store
- branches
- jumps
- pseudo-instructions if relevant
- instruction encoding
- machine code
- hexadecimal representation
- sign extension
- zero extension
- PC behavior
- branch target calculation
- jump target calculation
- memory addressing
- datapath
- control signals
- single-cycle execution if present
- assembler behavior
- code.lst interpretation

D. MIPS Online / Course Tooling
- how the online simulator/tool works
- syntax
- supported instructions
- register/memory behavior
- execution/debugging workflow
- any course-specific conventions

IMPORTANT:
Do NOT include topics merely because they belong to standard Computer Architecture unless they are relevant to this repository/course.

If you add necessary background material, clearly label it as:
"Background required to understand the assignment"

==================================================
PHASE 3 — QUIZ-ORIENTED ANALYSIS
==================================================

For every major topic, organize information into:

1. CORE IDEA
   - What it does
   - Why it exists

2. MUST MEMORIZE
   - formulas
   - definitions
   - bit layouts
   - control signals
   - instruction formats
   - rules

3. MUST UNDERSTAND
   - explain the mechanism intuitively

4. HOW IT IS IMPLEMENTED
   - connect theory to the actual .circ files/code

5. WORKED EXAMPLE
   - solve at least one representative example step-by-step

6. QUIZ TRAPS
   - common mistakes
   - sign/bit-width errors
   - off-by-one errors
   - incorrect field ordering
   - incorrect branch/jump calculations
   - overflow confusion
   - signed/unsigned confusion
   - implementation-specific pitfalls

7. QUICK CHECK
   - 3–10 short questions that test whether I understood the topic

==================================================
PHASE 4 — EXTRACT ASSIGNMENT-SPECIFIC KNOWLEDGE
==================================================

Create dedicated sections:

# Assignment 1 — ALU

Explain:
- assignment requirements
- ALU architecture
- inputs/outputs
- supported operations
- bit widths
- control encoding
- internal circuit structure
- important subcircuits
- how each operation works
- overflow/carry/zero behavior if applicable
- examples
- test cases
- likely quiz questions derived from this assignment

Include a table like:

Operation | Control | Input Behavior | Output | Flags

Use the ACTUAL control encoding from the repository, not a generic encoding.

--------------------------------------------------

# Assignment 2 — Floating Point Arithmetic

Explain:
- required representation
- exact bit widths
- field layout
- normalization
- arithmetic algorithm
- intermediate steps
- hardware blocks
- control/data flow
- edge cases
- test cases
- expected outputs where available
- likely quiz questions

Include diagrams using TikZ when useful.

For floating point arithmetic, show binary examples step-by-step.

If the assignment uses a custom floating-point representation rather than IEEE-754, emphasize that distinction heavily.

--------------------------------------------------

# Assignment 3 — MIPS

Explain:
- assignment requirements
- MIPS instruction set used
- instruction formats
- encoding
- datapath
- control
- assembler
- machine-code generation
- hex representation
- program execution

For every instruction actually used in the repository, provide:

Instruction | Type | Syntax | Meaning | Fields | Encoding | Example

Then show how the actual programs are translated:

Assembly
→ fields
→ binary
→ hexadecimal

Use actual repository examples.

Explain every important line of code.asm/program.asm.

If code.lst contains addresses or machine code, explain how to interpret it.

--------------------------------------------------

# MIPS ONLINE

Create a compact practical section explaining:
- tool usage
- writing/running programs
- registers
- memory
- debugging
- interpreting output
- common errors

==================================================
PHASE 5 — MASTER REFERENCE TABLES
==================================================

Create high-density reference tables.

At minimum:

1. Binary/number representation cheat sheet
2. ALU operations
3. ALU control signals
4. Floating-point fields
5. FPA operations
6. MIPS register table
7. MIPS instruction formats
8. MIPS instruction reference
9. Opcode table
10. funct table
11. Branch/jump formulas
12. Control-signal table
13. Common assembler conventions
14. Common mistakes

Only include entries supported/relevant to the repository.

==================================================
PHASE 6 — FORMULA SHEET
==================================================

Create a dedicated "Formula & Rules Sheet".

Put every important formula/rule in one place.

Examples where relevant:

- two's complement
- signed range
- unsigned range
- overflow conditions
- floating-point exponent calculations
- normalization
- branch target calculation
- jump target calculation
- effective address
- instruction size/address progression
- any assignment-specific formulas

Make this section extremely easy to scan.

==================================================
PHASE 7 — QUIZ QUESTIONS
==================================================

Create a large question bank based on the repository.

Categories:

A. Conceptual MCQ
B. Numerical/problem-solving
C. Binary conversion
D. ALU tracing
E. Floating-point tracing
F. MIPS instruction decoding
G. MIPS instruction encoding
H. Assembly → machine code
I. Machine code → assembly
J. Datapath/control questions
K. Circuit tracing
L. Debugging/error identification

Target approximately 50–80 questions if the source material supports it.

DO NOT fabricate course-specific facts.

For each question:
- question
- answer
- short explanation

For especially important questions, mark:

★ HIGH PROBABILITY

But do NOT claim certainty about what will appear in the quiz.

==================================================
PHASE 8 — LAST-MINUTE REVISION
==================================================

At the end create:

# 30-Minute Revision Plan

Organize the repository topics into a realistic final revision sequence.

Then:

# 10-Minute Ultra-Quick Review

Only the highest-value formulas, tables, rules, and traps.

Then:

# Things I Must Be Able to Do

For example:
- decode an instruction
- encode an instruction
- calculate a branch address
- trace ALU behavior
- determine overflow
- perform floating-point normalization
- trace a datapath
- etc.

Only include skills actually relevant to the repository.

==================================================
PHASE 9 — LAB VIVA QUESTIONS AS HIGH-PRIORITY QUIZ TOPICS
==================================================

The following questions were explicitly asked during the CSE210 lab viva. Treat these as HIGH-PRIORITY topics because similar questions may appear in the upcoming quiz.

Do NOT assume the quiz will contain the exact same questions, but use these viva questions as strong signals about the instructor's expected depth and style of understanding.

------------------------------------------
A. ALU — 1-BIT ALU DESIGN & FLAGS
------------------------------------------

The lab viva asked about:

1. Creating a small 1-bit ALU from a given set of operations.
2. Determining the values of the ALU flags:
   - C = Carry
   - S = Sign
   - V = Overflow
   - Z = Zero
   directly from the ALU implementation/hardware.

Therefore, the master note MUST include a dedicated subsection:

"1-Bit ALU: Build It and Derive the Flags"

Cover:

- How to construct a 1-bit ALU from primitive operations/gates.
- How multiple operations are selected using multiplexers/control signals.
- How the 1-bit ALU can be extended to an n-bit ALU.
- Full-adder behavior:
  - A
  - B
  - Cin
  - Sum
  - Cout
- Derive the truth table where relevant.
- Explain how the carry propagates between ALU slices.
- Explain how the final carry is obtained.
- Explain how each flag is generated from the hardware.

For C, S, V, Z, explicitly show:

Flag | Hardware signal/expression | Meaning | How to determine it

Pay particular attention to:

- Carry vs signed overflow
- Sign bit of the result
- Zero detection across all result bits
- Signed overflow detection
- Difference between carry-out and overflow
- How the implementation produces the flags
- Any assignment-specific flag conventions

Show concrete bit-level examples where the learner is given A, B, Cin and control signals and must determine:

Result, C, S, V, Z

Also include reverse questions such as:

"Given these ALU inputs, operation, and flag outputs, determine what happened."

Create several quiz-style problems where the learner must inspect/trace the ALU hardware rather than simply memorize definitions.

If the actual ALU.circ implementation uses specific logic for C/S/V/Z, derive the explanations from that implementation and explicitly connect the hardware to the equations.

------------------------------------------
B. FPA — DECIMAL/BINARY FLOATING-POINT
------------------------------------------

The lab viva asked about:

1. Decimal → binary floating-point conversion.
2. Floating-point addition.
3. Floating-point subtraction.

Therefore, make these HIGH-PRIORITY quiz topics.

Create a dedicated subsection:

"FPA Viva Essentials: Conversion, Addition & Subtraction"

Cover step-by-step:

### Decimal → Binary Float

Show how to convert:

- integer part
- fractional part
- sign
- exponent
- mantissa/significand

Then show normalization.

If the assignment uses a custom floating-point representation, use the EXACT representation from the assignment rather than IEEE-754 assumptions.

Include multiple worked examples.

For every example, explicitly show:

Decimal
→ binary
→ normalized form
→ sign
→ exponent
→ mantissa/fraction
→ final encoded representation

### Floating-Point Addition

Explain the complete algorithm:

1. Compare exponents
2. Align significands
3. Shift the smaller significand
4. Add significands
5. Normalize
6. Adjust exponent
7. Handle sign
8. Apply rounding/truncation if applicable
9. Produce final representation

Show at least several worked binary examples.

### Floating-Point Subtraction

Explain:

1. Sign handling
2. Exponent alignment
3. Magnitude comparison
4. Subtraction
5. Normalization
6. Exponent adjustment
7. Final representation

Explicitly discuss the difference between:

A + B
A - B
(-A) + B
A + (-B)

Create quiz problems requiring the learner to perform the complete conversion/addition/subtraction manually.

Also connect the arithmetic procedure to the actual FPA3.circ hardware/datapath.

------------------------------------------
C. MIPS — CONTROL BITS FOR INSTRUCTIONS
------------------------------------------

The lab viva asked about:

"Finding the control bits of the processor for a given operation."

Examples included:

- add
- subi
- beq
- etc.

Treat this as a VERY HIGH-PRIORITY quiz topic.

Create a dedicated section:

"MIPS Control Signals — Given an Instruction, Derive the Control Bits"

For every relevant instruction in the repository, create a table such as:

Instruction | RegDst | ALUSrc | MemToReg | RegWrite | MemRead | MemWrite | Branch | ALUOp | Jump | Other

IMPORTANT:

Use the ACTUAL control architecture and signal names from the repository's MIPS implementation.

Do NOT blindly use a generic textbook MIPS control table if the course's MIPS.circ uses different signals, encodings, or conventions.

For each instruction, explain WHY each control bit has its value.

For example, conceptually:

Instruction
→ What data is read?
→ What data is written?
→ What operation does the ALU perform?
→ Is the second ALU operand a register or immediate?
→ Is memory accessed?
→ Is a register written?
→ Does PC change conditionally?
→ Therefore, what are the control signals?

Cover at minimum:

- add
- subi
- beq

and EVERY other instruction actually supported/used by the repository.

Create reverse-engineering questions:

"Given these control bits, what instruction/operation is being performed?"

Also create forward questions:

"Given this instruction, determine all control bits."

Include questions where only ONE control signal changes between two instructions, because these are useful for testing whether the learner actually understands the datapath.

------------------------------------------
QUIZ QUESTION GENERATION REQUIREMENT
------------------------------------------

Because these viva questions may appear in the quiz, the final question bank MUST contain a significant number of questions based on these three categories.

Prioritize questions of the following forms:

ALU:
- Build a 1-bit ALU from specified operations.
- Determine output of a 1-bit ALU.
- Determine C/S/V/Z from given inputs.
- Determine C/S/V/Z from an ALU circuit.
- Distinguish carry from overflow.
- Trace an n-bit ALU built from 1-bit slices.

FPA:
- Decimal → binary floating-point.
- Binary float → decimal where useful.
- Normalize a floating-point number.
- Floating-point addition.
- Floating-point subtraction.
- Determine intermediate exponent/significand values.
- Identify mistakes in an FPA calculation.

MIPS:
- Determine control bits for add.
- Determine control bits for subi.
- Determine control bits for beq.
- Determine control bits for other supported instructions.
- Infer an instruction from control signals.
- Trace the datapath for an instruction.
- Explain why each control signal is 0 or 1.
- Identify which control signal changes between two instructions.

Mark especially representative questions with:

★ VIVA-STYLE

and especially important ones with:

★ HIGH-PRIORITY

Do not claim that any question is guaranteed to appear. These labels mean that the question style is directly informed by the lab viva.

------------------------------------------
VIVA → QUIZ CONNECTION
------------------------------------------

Add a short boxed section near the beginning of the final document:

"Why These Viva Questions Matter"

Explain that the viva demonstrates the expected level of understanding:

ALU → hardware-level reasoning
FPA → numerical representation + arithmetic procedure
MIPS → datapath/control reasoning

Therefore, prioritize UNDERSTANDING and TRACEABILITY over memorizing isolated facts.

The learner should be able to move in both directions:

Concept
↔ Hardware
↔ Signals
↔ Numerical Example
↔ Final Result

The final notes should repeatedly reinforce this style of reasoning.

==================================================
LATEX REQUIREMENTS
==================================================

Create a professional standalone LaTeX document.

Prefer:

\\documentclass[10pt,a4paper]{article}

Use packages that are likely to compile on a standard TeX Live installation.

Recommended packages:

\\usepackage[margin=0.65in]{geometry}
\\usepackage{amsmath,amssymb}
\\usepackage{mathtools}
\\usepackage{booktabs}
\\usepackage{array}
\\usepackage{longtable}
\\usepackage{tabularx}
\\usepackage{multicol}
\\usepackage{xcolor}
\\usepackage{enumitem}
\\usepackage{microtype}
\\usepackage{tikz}
\\usepackage{listings}
\\usepackage{hyperref}
\\usepackage{fancyhdr}
\\usepackage{tcolorbox}

Avoid exotic fonts.

Do NOT require:
- Libertinus
- Fira
- custom fonts
- external font downloads

The document MUST compile with the user's existing TeX installation.

Use:
- compact margins
- small but readable typography
- colored boxes for warnings/formulas
- tables for reference material
- TikZ for architecture diagrams
- monospace formatting for assembly/code
- consistent hierarchy

Create reusable environments such as:

definition box
formula box
warning/trap box
example box
quiz box
memory box

For example:

\\begin{tcolorbox}[title=QUIZ TRAP]
...
\\end{tcolorbox}

==================================================
DIAGRAM REQUIREMENTS
==================================================

Where appropriate, create clean TikZ diagrams for:

- ALU structure
- FPA datapath
- MIPS datapath
- instruction format
- branch calculation
- floating-point normalization

Do NOT create decorative diagrams.

Every diagram must communicate useful information.

==================================================
CODE REQUIREMENTS
==================================================

For MIPS assembly, use listings.

Example style:

\\begin{lstlisting}[language={[x86masm]Assembler}]
...
\\end{lstlisting}

If the syntax highlighting package does not support MIPS properly, define a custom language.

==================================================
IMPORTANT ACCURACY RULES
==================================================

1. Never invent values, control signals, opcodes, field widths, or circuit behavior.

2. If sources disagree:
   - inspect the actual implementation
   - identify the discrepancy
   - explain it explicitly

3. Distinguish:
   - standard MIPS behavior
   - assignment-specific behavior
   - implementation-specific behavior

4. If something cannot be determined from the repository, say:
   "Not specified in the provided course materials."

5. Do not silently assume standard textbook conventions when the assignment uses a custom convention.

6. Preserve exact bit widths.

7. When showing binary:
   - group bits logically
   - label fields
   - show leading zeroes when they matter

8. When calculating hexadecimal:
   - show intermediate binary where useful

9. For circuit behavior:
   - explain actual signal flow

10. For code:
   - use actual code from the repository when demonstrating assignment-specific behavior.

==================================================
DOCUMENT STRUCTURE
==================================================

Use approximately this structure:

TITLE PAGE / HEADER
    CSE210 Computer Architecture
    Master Quiz Notes
    Assignment-Based Revision Guide

TABLE OF CONTENTS

0. How to Use This Note

1. CSE210 Big Picture

2. Number Representation & Digital Arithmetic
   2.1 Binary
   2.2 Signed Numbers
   2.3 Two's Complement
   2.4 Overflow
   2.5 Bitwise Operations

3. Assignment 1 — ALU
   3.1 Requirements
   3.2 Architecture
   3.3 Operations
   3.4 Control
   3.5 Circuit Internals
   3.6 Examples
   3.7 Traps
   3.8 Quiz Questions

4. Assignment 2 — Floating Point Arithmetic
   4.1 Representation
   4.2 Arithmetic
   4.3 Normalization
   4.4 Datapath
   4.5 Circuit Internals
   4.6 Test Cases
   4.7 Examples
   4.8 Traps
   4.9 Quiz Questions

5. Assignment 3 — MIPS
   5.1 Architecture
   5.2 Registers
   5.3 Instruction Formats
   5.4 Instruction Set
   5.5 Encoding
   5.6 Decoding
   5.7 Datapath
   5.8 Control
   5.9 Branches
   5.10 Jumps
   5.11 Memory
   5.12 Assembler
   5.13 Actual Assignment Programs
   5.14 Machine Code
   5.15 Traps
   5.16 Quiz Questions

6. MIPS Online

7. Master Reference Tables

8. Formula & Rules Sheet

9. Common Mistakes

10. 50–80 Quiz Questions

11. 30-Minute Revision

12. 10-Minute Ultra-Quick Review

13. Things I Must Be Able to Do

APPENDIX
    A. Important assignment files
    B. Repository-specific terminology
    C. Additional useful examples

==================================================
OUTPUT FILES
==================================================

Create:

CSE210_Master_Notes.tex

Compile it and verify that it actually builds.

Also produce:

CSE210_Master_Notes.pdf

Before finishing:
1. Compile the PDF.
2. Check for LaTeX errors/warnings that affect output.
3. Check that tables don't overflow.
4. Check that code blocks don't overflow.
5. Check that equations render correctly.
6. Check that TikZ diagrams render.
7. Check that the table of contents works.
8. Check that page numbers work.
9. Check that no section is accidentally empty.
10. Check that there are no unresolved references.

If compilation fails, FIX THE LATEX and recompile.

==================================================
FINAL QUALITY BAR
==================================================

The final document should feel like:

"Someone took my actual CSE210 assignments, reverse-engineered what I need to know, connected the theory to the implementations, and turned it into one comprehensive quiz survival document."

It should NOT feel like:

"Here is a generic Computer Architecture chapter copied from a textbook."

Prioritize:
COURSE-SPECIFIC ACCURACY
>
ASSIGNMENT IMPLEMENTATION DETAILS
>
QUIZ RELEVANCE
>
CLARITY
>
COMPACTNESS
>
AESTHETICS

Start by inspecting the repository. Do not write the notes until you have analyzed the source material.

WORKFLOW REQUIREMENT:

Do not attempt to generate the entire final LaTeX file in a single unverified pass.

Work in stages:

1. Repository inspection
2. Extracted knowledge map
3. Assignment-specific analysis
4. Draft LaTeX
5. Compile
6. Inspect compilation output
7. Fix layout/accuracy issues
8. Compile again
9. Final audit against the repository

Before finalizing, perform a "source coverage audit":

For every source file in the repository, record internally:
- Was it inspected?
- Did it contain quiz-relevant information?
- Was that information incorporated into the notes?

Do not include this audit in the final PDF unless useful.

If the repository contains diagrams/images that cannot be represented faithfully in text, use the source diagram as the basis for a clean recreated TikZ diagram rather than ignoring it.
