SEC1_BIG_PICTURE = r"""
\section{CSE 210 Course Big Picture: The Architectural Journey}

The CSE 210 Computer Architecture Sessional curriculum forms a continuous, bottom-up progression through modern digital computer systems. Rather than viewing the assignments as isolated exercises, understand how each layer builds upon the previous one:

\begin{center}
\begin{tikzpicture}[
    box/.style={draw=NavyBlue, thick, rounded corners=3pt, fill=NavyBlue!8!white, align=center, font=\small, inner sep=6pt},
    arrow/.style={-{Stealth[scale=1.1]}, thick, NavyBlue}
]
  \node[box, text width=12cm] (ass1) {
    \textbf{Assignment 1: IC-Level 4-Bit ALU (Hardware Primitives \& Logic Slices)}\\
    \footnotesize 74xx TTL SSI/MSI ICs \textbar\ 74283 Full Adder \textbar\ 74157 Multiplexers \textbar\ Status Flags ($C, S, V, Z$)
  };

  \node[box, text width=12cm, below=0.6cm of ass1] (ass2) {
    \textbf{Assignment 2: 16-Bit Floating Point Adder (FPA) (Pipelined Data Processing)}\\
    \footnotesize Exponent Comparison \textbar\ Significand Alignment \textbar\ 14-bit ALU \textbar\ G/R/S Bits \textbar\ RNE Rounding \textbar\ Over/Underflow
  };

  \node[box, text width=12cm, below=0.6cm of ass2] (ass3) {
    \textbf{Assignment 3: Custom 4-Bit MIPS Processor \& Assembler (Instruction Execution)}\\
    \footnotesize 16-bit Words \textbar\ 12-bit Microcode ROM \textbar\ 4 Formats (R/S/I/J) \textbar\ 6 GPRs + Hardware \$sp \textbar\ 2-Pass Assembler
  };

  \node[box, text width=12cm, below=0.6cm of ass3] (ass4) {
    \textbf{MIPS Online: High-Level Software \& Recursive Stack Frames}\\
    \footnotesize 32-bit MIPS \textbar\ Calling Conventions (\$sp, \$ra, \$a0-\$a3, \$v0) \textbar\ Stack Frame Preservation \textbar\ Array Traversal
  };

  \draw[arrow] (ass1) -- node[right, font=\scriptsize\itshape, text=NavyBlue] {scaling data widths \& complexity} (ass2);
  \draw[arrow] (ass2) -- node[right, font=\scriptsize\itshape, text=NavyBlue] {integrating control \& stored-program logic} (ass3);
  \draw[arrow] (ass3) -- node[right, font=\scriptsize\itshape, text=NavyBlue] {executing high-level procedural code} (ass4);
\end{tikzpicture}
\end{center}

\subsection{Architectural Comparison Across Assignments}

\begin{table}[h!]
\centering
\small
\begin{tabularx}{\textwidth}{l p{3.2cm} p{3.4cm} p{3.6cm} p{3.4cm}}
\toprule
\textbf{Parameter} & \textbf{Assignment 1: ALU} & \textbf{Assignment 2: FPA} & \textbf{Assignment 3: MIPS} & \textbf{MIPS Online} \\
\midrule
\textbf{Data Bus Width} & 4 bits & 16 bits (internal 14-bit mantissa) & 4 bits & 32 bits (word size) \\
\textbf{Address Bus Width} & N/A & N/A & 8 bits (256 addresses) & 32 bits (byte-addressed) \\
\textbf{Design Paradigm} & Discrete ICs (SSI/MSI) & Hierarchical subcircuits & Modular datapath + Microcode & Assembly programming \\
\textbf{Number Format} & 4-bit 2's Complement & 16-bit custom IEEE FP16 & 4-bit 2's Complement & 32-bit 2's Complement \\
\textbf{Control Mechanism} & Direct 3-bit wire select & Hardwired combinatorial logic & 16$\times$12-bit Control ROM & Software control flow (ISA) \\
\textbf{Memory Elements} & Combinatorial only & Combinatorial datapath & RAM (unified) + ROM + RegFile & Memory Hierarchy \& Stack \\
\textbf{Key Output} & $S[3:0]$, Flags ($C,S,V,Z$) & Sum[15:0], Flags (Ovf, Unf) & Register updates, Mem writes & Function return value (\$v0) \\
\bottomrule
\end{tabularx}
\end{table}
"""
