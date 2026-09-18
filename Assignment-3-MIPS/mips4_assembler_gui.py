#!/usr/bin/env python3
"""
Simple GUI front-end for the custom 4-bit MIPS assembler.
Keep this file in the same folder as mips4_assembler.py.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

import mips4_assembler as core


class AssemblerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("4-bit MIPS Assembler")
        self.geometry("1000x680")
        self.minsize(820, 560)

        self.source_path: Path | None = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        bar = ttk.Frame(self, padding=8)
        bar.grid(row=0, column=0, sticky="ew")
        bar.columnconfigure(4, weight=1)

        ttk.Button(bar, text="Open .asm", command=self.open_file).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(bar, text="Assemble", command=self.assemble).grid(row=0, column=1, padx=6)
        ttk.Button(bar, text="Save ROM image", command=self.save_rom).grid(row=0, column=2, padx=6)
        ttk.Button(bar, text="Clear", command=self.clear_all).grid(row=0, column=3, padx=6)
        self.status = ttk.Label(bar, text="Ready")
        self.status.grid(row=0, column=4, sticky="e")

        panes = ttk.Panedwindow(self, orient="horizontal")
        panes.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

        left = ttk.Frame(panes)
        right = ttk.Frame(panes)
        panes.add(left, weight=1)
        panes.add(right, weight=1)

        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)
        ttk.Label(left, text="Assembly source").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.source = tk.Text(left, wrap="none", undo=True, font=("Consolas", 11))
        self.source.grid(row=1, column=0, sticky="nsew")

        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)
        ttk.Label(right, text="Machine-code listing").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.listing = tk.Text(right, wrap="none", state="disabled", font=("Consolas", 11))
        self.listing.grid(row=1, column=0, sticky="nsew")

        bottom = ttk.Frame(self, padding=(8, 0, 8, 8))
        bottom.grid(row=2, column=0, sticky="ew")
        bottom.columnconfigure(0, weight=1)

        ttk.Label(bottom, text="Logisim ROM image").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.rom = tk.Text(bottom, height=5, wrap="word", state="disabled", font=("Consolas", 11))
        self.rom.grid(row=1, column=0, sticky="ew")

        demo = """# Example
addi $t0, $zero, 3
addi $t1, $zero, 2
add  $t2, $t0, $t1
sw   $t2, 0($zero)

loop:
j loop
"""
        self.source.insert("1.0", demo)
        self.words: list[int] = []
        self.source_lines = []

    def set_text(self, widget: tk.Text, text: str):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def open_file(self):
        name = filedialog.askopenfilename(
            title="Open assembly source",
            filetypes=[("Assembly files", "*.asm"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not name:
            return
        self.source_path = Path(name)
        self.source.delete("1.0", "end")
        self.source.insert("1.0", self.source_path.read_text(encoding="utf-8"))
        self.status.configure(text=self.source_path.name)

    def assemble(self):
        text = self.source.get("1.0", "end-1c")
        try:
            words, src = core.assemble(text)
        except core.AssemblerError as exc:
            messagebox.showerror("Assembler error", str(exc))
            self.status.configure(text="Assembly failed")
            return

        self.words = words
        self.source_lines = src

        listing_lines = [
            "ADDR  HEX   BINARY               SOURCE",
            "----  ----  -------------------  ----------------------------------------"
        ]
        for word, item in zip(words, src):
            b = f"{word:016b}"
            grouped = " ".join(b[i:i+4] for i in range(0, 16, 4))
            listing_lines.append(f"{item.address:02X}    {word:04X}  {grouped}  {item.text}")

        rom_rows = []
        for i in range(0, len(words), 8):
            rom_rows.append(" ".join(f"{w:04x}" for w in words[i:i+8]))
        rom_text = "v2.0 raw\n" + "\n".join(rom_rows) + ("\n" if words else "")

        self.set_text(self.listing, "\n".join(listing_lines) + "\n")
        self.set_text(self.rom, rom_text)
        self.status.configure(text=f"Assembled {len(words)} instruction(s)")

    def save_rom(self):
        if not self.words:
            self.assemble()
            if not self.words:
                return

        suggested = "program.hex"
        if self.source_path:
            suggested = self.source_path.with_suffix(".hex").name

        name = filedialog.asksaveasfilename(
            title="Save Logisim ROM image",
            defaultextension=".hex",
            initialfile=suggested,
            filetypes=[("Logisim ROM image", "*.hex"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not name:
            return

        core.write_logisim_image(Path(name), self.words)
        self.status.configure(text=f"Saved {Path(name).name}")
        messagebox.showinfo("Saved", f"ROM image saved to:\n{name}")

    def clear_all(self):
        self.source.delete("1.0", "end")
        self.set_text(self.listing, "")
        self.set_text(self.rom, "")
        self.words = []
        self.source_lines = []
        self.source_path = None
        self.status.configure(text="Ready")


if __name__ == "__main__":
    AssemblerGUI().mainloop()
