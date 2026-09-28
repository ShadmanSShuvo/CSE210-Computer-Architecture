PREAMBLE = r"""\documentclass[10pt,a4paper]{article}

% --- Margins and Geometry ---
\usepackage[margin=0.6in,top=0.7in,bottom=0.7in]{geometry}

% --- Math Packages ---
\usepackage{amsmath,amssymb,mathtools}

% --- Tables & Arrays ---
\usepackage{booktabs}
\usepackage{array}
\usepackage{longtable}
\usepackage{tabularx}
\usepackage{multirow}
\renewcommand{\arraystretch}{1.18}

% --- Color & Graphics ---
\usepackage[dvipsnames,table]{xcolor}
\usepackage{tikz}
\usetikzlibrary{calc,positioning,shapes.geometric,arrows.meta}

% --- Typography & Lists ---
\usepackage{enumitem}
\usepackage{microtype}
\setlist{nosep,leftmargin=1.4em}

% --- Code Listings ---
\usepackage{listings}
\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  frame=single,
  rulecolor=\color{gray!40},
  backgroundcolor=\color{gray!5},
  keywordstyle=\bfseries\color{NavyBlue},
  commentstyle=\itshape\color{OliveGreen},
  stringstyle=\color{BrickRed},
  numbers=left,
  numberstyle=\tiny\color{gray},
  numbersep=6pt,
  columns=fullflexible,
  keepspaces=true,
  showstringspaces=false
}

% --- Fancy Header & Footer ---
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\lhead{\textbf{\footnotesize CSE210: Computer Architecture} \textbar\ \scriptsize Master Quiz Notes}
\rhead{\scriptsize BUET CSE \textbar\ Jan 2026 Sessional}
\cfoot{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% --- TColorBox Environments ---
\usepackage[most]{tcolorbox}
\tcbuselibrary{breakable,skins}

\newtcolorbox{vivabox}[1][]{
  enhanced,
  breakable,
  colback=Orange!6!white,
  colframe=Orange!85!black,
  fonttitle=\bfseries\small,
  coltitle=white,
  title={$\bigstar$ VIVA-STYLE ESSENTIAL: #1},
  boxrule=0.8pt,
  arc=2pt,
  left=6pt,right=6pt,top=5pt,bottom=5pt,
  before skip=6pt,after skip=6pt
}

\newtcolorbox{quiztrapbox}[1][]{
  enhanced,
  breakable,
  colback=Red!6!white,
  colframe=Red!80!black,
  fonttitle=\bfseries\small,
  coltitle=white,
  title={$\bigstar$ QUIZ TRAP / COMMON PITFALL: #1},
  boxrule=0.8pt,
  arc=2pt,
  left=6pt,right=6pt,top=5pt,bottom=5pt,
  before skip=6pt,after skip=6pt
}

\newtcolorbox{formulabox}[1][]{
  enhanced,
  breakable,
  colback=NavyBlue!6!white,
  colframe=NavyBlue!85!black,
  fonttitle=\bfseries\small,
  coltitle=white,
  title={KEY FORMULA / HARDWARE RULE: #1},
  boxrule=0.8pt,
  arc=2pt,
  left=6pt,right=6pt,top=5pt,bottom=5pt,
  before skip=6pt,after skip=6pt
}

\newtcolorbox{examplebox}[1][]{
  enhanced,
  breakable,
  colback=ForestGreen!6!white,
  colframe=ForestGreen!80!black,
  fonttitle=\bfseries\small,
  coltitle=white,
  title={WORKED STEP-BY-STEP EXAMPLE: #1},
  boxrule=0.8pt,
  arc=2pt,
  left=6pt,right=6pt,top=5pt,bottom=5pt,
  before skip=6pt,after skip=6pt
}

\newtcolorbox{quizprob}[1][]{
  enhanced,
  breakable,
  colback=Purple!6!white,
  colframe=Purple!80!black,
  fonttitle=\bfseries\small,
  coltitle=white,
  title={QUIZ PRACTICE PROBLEM: #1},
  boxrule=0.8pt,
  arc=2pt,
  left=6pt,right=6pt,top=5pt,bottom=5pt,
  before skip=6pt,after skip=6pt
}

\newtcolorbox{defbox}[1][]{
  enhanced,
  breakable,
  colback=TealBlue!6!white,
  colframe=TealBlue!85!black,
  fonttitle=\bfseries\small,
  coltitle=white,
  title={ARCHITECTURE DEFINITION: #1},
  boxrule=0.8pt,
  arc=2pt,
  left=6pt,right=6pt,top=5pt,bottom=5pt,
  before skip=6pt,after skip=6pt
}

% --- Hyperref ---
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=NavyBlue,
  urlcolor=MidnightBlue,
  citecolor=ForestGreen
}

% --- Custom Math / Text Helpers ---
\newcommand{\inst}[1]{\texttt{#1}}
\newcommand{\reg}[1]{\texttt{#1}}
\newcommand{\hex}[1]{\texttt{0x#1}}
\newcommand{\bin}[1]{\texttt{#1}\textsubscript{2}}
\newcommand{\bit}[1]{\texttt{#1}}
"""
