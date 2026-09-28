SEC0_INTRO = r"""
\begin{center}
  {\Huge \textbf{CSE 210: Computer Architecture}}\\[4pt]
  {\Large \textbf{Master Quiz Notes \& Assignment-Based Revision Guide}}\\[4pt]
  \textbf{Department of Computer Science and Engineering \textbar\ BUET}\\[2pt]
  \textsl{January 2026 Term \textbar\ Comprehensive Exam-Oriented Synthesis}
\end{center}

\vspace{-6pt}
\hrule height 1pt
\vspace{6pt}

\tableofcontents
\newpage

\section{How to Use This Note \& Why Viva Questions Matter}

\begin{vivabox}[Why These Lab Viva Questions Matter for Tomorrow's Quiz]
During the CSE 210 lab viva, the course instructors directly tested your ability to explain \textbf{hardware mechanisms} rather than reproduce generic textbook definitions. The questions targeted three fundamental competencies:
\begin{enumerate}
  \item \textbf{ALU (Hardware-Level Reasoning):} Constructing a 1-bit ALU slice from primitive gates, multiplexing operations, ripple carry propagation, and deriving the exact hardware logic for the status flags ($C, S, V, Z$) directly from the adder outputs.
  \item \textbf{FPA (Numerical Representation \& Datapath Tracing):} Converting decimal values to custom IEEE-style 16-bit float, performing step-by-step floating-point addition and subtraction (with magnitude alignment, 14-bit arithmetic, Guard/Round/Sticky bit handling, round-to-nearest-even, and range checking).
  \item \textbf{MIPS (Datapath \& Control Reasoning):} Deriving all control bits for every instruction directly from the datapath connections rather than memorizing a table, and calculating exact branch offsets and jump addresses.
\end{enumerate}

\textbf{Core Exam Strategy:} You must be able to reason \textbf{bidirectionally}:
\[
\text{Architecture Concept} \iff \text{Datapath Schematics} \iff \text{Control Signals} \iff \text{Numerical / Bit Trace} \iff \text{Final Flag / Value}
\]
Throughout this master note, every topic is anchored directly in the repository's source circuits (\texttt{ALU.circ}, \texttt{FPA3.circ}, \texttt{MIPS.circ}), official specifications, and assembler code.
\end{vivabox}

\subsection{Document Conventions and Callout Taxonomy}
To enable rapid scanning during last-minute revision, the document uses specialized colored callout environments:
\begin{itemize}
  \item \textbf{\color{Orange!85!black}$\bigstar$ VIVA-STYLE ESSENTIAL:} Mandatory questions and concepts explicitly emphasized during the laboratory evaluations.
  \item \textbf{\color{Red!80!black}$\bigstar$ QUIZ TRAP / COMMON PITFALL:} Subtleties, off-by-one errors, sign-extension mistakes, and implementation quirks that frequently cause lost marks.
  \item \textbf{\color{NavyBlue!85!black}KEY FORMULA / HARDWARE RULE:} Equations, boolean expressions, and numerical bounds required for calculation problems.
  \item \textbf{\color{ForestGreen!80!black}WORKED STEP-BY-STEP EXAMPLE:} Full numerical and bit-level solutions with intermediate calculations explicitly shown.
  \item \textbf{\color{Purple!80!black}QUIZ PRACTICE PROBLEM:} Exam-style questions (MCQs, problem-solving, trace, reverse-engineering) with solutions and explanations.
\end{itemize}
"""
