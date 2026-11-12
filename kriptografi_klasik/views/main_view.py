# views/main_view.py
"""
Main View
==========
Mengelola seluruh antarmuka grafis (GUI) aplikasi Kriptografi Klasik.

Tanggung jawab:
- Layout dan penempatan widget (frame, label, entry, scrolled text, button).
- Menyediakan getter/setter untuk state UI.
- Meneruskan *callback* ke Controller melalui metode ``set_callbacks``.

View **tidak** mengandung logika bisnis apa pun.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Callable


class MainView:
    """Kelas View utama yang membangun dan mengelola seluruh GUI."""

    # ------------------------------------------------------------------ #
    #  Konstruktor
    # ------------------------------------------------------------------ #
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Kriptografi Klasik — Caesar & Vigenère Cipher")
        self.root.geometry("780x720")
        self.root.minsize(680, 640)
        self.root.resizable(True, True)

        # Variabel tkinter -------------------------------------------------
        self.cipher_var = tk.StringVar(value="caesar")
        self.mode_var = tk.StringVar(value="encrypt")

        # Styling -----------------------------------------------------------
        self._configure_styles()

        # Bangun UI ---------------------------------------------------------
        self._build_ui()

    # ------------------------------------------------------------------ #
    #  Styling (ttk)
    # ------------------------------------------------------------------ #
    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        # Warna utama
        BG       = "#f5f6fa"
        PRIMARY  = "#2c3e50"
        ACCENT   = "#2563EB"
        SUCCESS  = "#17872a"
        DANGER   = "#db1010"
        WHITE    = "#ffffff"

        self.root.configure(bg=BG)

        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=PRIMARY,
                         font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=BG, foreground=PRIMARY,
                         font=("Segoe UI", 18, "bold"))
        style.configure("SubHeader.TLabel", background=BG, foreground="#7f8c8d",
                         font=("Segoe UI", 9))
        style.configure("Section.TLabelframe", background=BG,
                         foreground=PRIMARY, font=("Segoe UI", 10, "bold"))
        style.configure("Section.TLabelframe.Label", background=BG,
                         foreground=PRIMARY, font=("Segoe UI", 10, "bold"))

        style.configure("TRadiobutton", background=BG, foreground=PRIMARY,
                         font=("Segoe UI", 10))

        # Tombol
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"),
                         foreground=WHITE, background=ACCENT, padding=(14, 6))
        style.map("Accent.TButton",
                  background=[("active", "#3498db"), ("disabled", "#bdc3c7")])

        style.configure("Success.TButton", font=("Segoe UI", 10),
                         foreground=WHITE, background=SUCCESS, padding=(12, 6))
        style.map("Success.TButton",
                  background=[("active", "#2ecc71"), ("disabled", "#bdc3c7")])

        style.configure("Danger.TButton", font=("Segoe UI", 10),
                         foreground=WHITE, background=DANGER, padding=(12, 6))
        style.map("Danger.TButton",
                  background=[("active", "#e55039"), ("disabled", "#bdc3c7")])

    # ------------------------------------------------------------------ #
    #  Layout Builder
    # ------------------------------------------------------------------ #
    def _build_ui(self) -> None:
        # Container utama
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=tk.BOTH, expand=True)

        # === Header ====================================================
        ttk.Label(container, text="Kriptografi Klasik",
                  style="Header.TLabel").pack(anchor=tk.W)
        ttk.Label(container,
                  text="Caesar & Vigenère Cipher",
                  style="SubHeader.TLabel").pack(anchor=tk.W, pady=(0, 10))

        ttk.Separator(container, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 10))

        # === Baris Pengaturan ==========================================
        settings_frame = ttk.Frame(container)
        settings_frame.pack(fill=tk.X, pady=(0, 8))

        # -- Metode Cipher ----------------------------------------------
        cipher_lf = ttk.LabelFrame(settings_frame, text="  Metode ",
                                    style="Section.TLabelframe", padding=8)
        cipher_lf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        ttk.Radiobutton(cipher_lf, text="Caesar Cipher",
                         variable=self.cipher_var, value="caesar",
                         command=self._on_cipher_changed).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(cipher_lf, text="Vigenère Cipher",
                         variable=self.cipher_var, value="vigenere",
                         command=self._on_cipher_changed).pack(anchor=tk.W, pady=2)

        # -- Mode Operasi -----------------------------------------------
        mode_lf = ttk.LabelFrame(settings_frame, text="  Mode Operasi  ",
                                  style="Section.TLabelframe", padding=8)
        mode_lf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0))

        ttk.Radiobutton(mode_lf, text="🔒 Enkripsi",
                         variable=self.mode_var, value="encrypt").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(mode_lf, text="🔓 Dekripsi",
                         variable=self.mode_var, value="decrypt").pack(anchor=tk.W, pady=2)

        # === Kunci =====================================================
        key_frame = ttk.Frame(container)
        key_frame.pack(fill=tk.X, pady=(0, 8))

        self.key_label = ttk.Label(key_frame, text="Kunci (Key):")
        self.key_label.pack(side=tk.LEFT)

        self.key_entry = ttk.Entry(key_frame, width=40, font=("Consolas", 11))
        self.key_entry.pack(side=tk.LEFT, padx=(8, 0), fill=tk.X, expand=True)

        # Set placeholder awal
        self._update_key_placeholder()

        # === Input Teks ================================================
        input_lf = ttk.LabelFrame(container, text="  Teks Input  ",
                                   style="Section.TLabelframe", padding=6)
        input_lf.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        self.input_text = scrolledtext.ScrolledText(
            input_lf, wrap=tk.WORD, height=7,
            font=("Consolas", 11), relief=tk.FLAT,
            bd=1, highlightthickness=1, highlightcolor="#2980b9",
            highlightbackground="#bdc3c7"
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)

        # === Tombol Aksi ===============================================
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=tk.X, pady=6)

        self.process_btn = ttk.Button(btn_frame, text="⚙  Proses",
                                       style="Accent.TButton")
        self.process_btn.pack(side=tk.LEFT, padx=(0, 6))

        self.clear_btn = ttk.Button(btn_frame, text="🗑  Clear Text",
                                     style="Danger.TButton")
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 6))

        self.copy_btn = ttk.Button(btn_frame, text="📋  Copy Hasil",
                                    style="Success.TButton")
        self.copy_btn.pack(side=tk.LEFT)

        # === Output Teks ===============================================
        output_lf = ttk.LabelFrame(container, text="  Hasil Output  ",
                                    style="Section.TLabelframe", padding=6)
        output_lf.pack(fill=tk.BOTH, expand=True, pady=(0, 0))

        self.output_text = scrolledtext.ScrolledText(
            output_lf, wrap=tk.WORD, height=7,
            font=("Consolas", 11), state=tk.DISABLED,
            relief=tk.FLAT, bd=1, highlightthickness=1,
            highlightcolor="#27ae60", highlightbackground="#bdc3c7",
            bg="#ecf0f1"
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------ #
    #  Callback Binding (dipanggil oleh Controller)
    # ------------------------------------------------------------------ #
    def set_callbacks(
        self,
        on_process: Callable[[], None],
        on_clear: Callable[[], None],
        on_copy: Callable[[], None],
    ) -> None:
        """Hubungkan tombol-tombol aksi ke callback Controller.

        Args:
            on_process: Dipanggil saat tombol Proses ditekan.
            on_clear: Dipanggil saat tombol Clear ditekan.
            on_copy: Dipanggil saat tombol Copy Hasil ditekan.
        """
        self.process_btn.configure(command=on_process)
        self.clear_btn.configure(command=on_clear)
        self.copy_btn.configure(command=on_copy)

    # ------------------------------------------------------------------ #
    #  Getter State UI
    # ------------------------------------------------------------------ #
    def get_cipher_method(self) -> str:
        """Mengembalikan metode cipher terpilih ('caesar' atau 'vigenere')."""
        return self.cipher_var.get()

    def get_mode(self) -> str:
        """Mengembalikan mode operasi terpilih ('encrypt' atau 'decrypt')."""
        return self.mode_var.get()

    def get_key(self) -> str:
        """Mengembalikan string kunci dari Entry."""
        return self.key_entry.get()

    def get_input_text(self) -> str:
        """Mengembalikan isi area teks input."""
        return self.input_text.get("1.0", tk.END).rstrip("\n")

    # ------------------------------------------------------------------ #
    #  Setter State UI
    # ------------------------------------------------------------------ #
    def set_output_text(self, text: str) -> None:
        """Tampilkan *text* di area output (read-only)."""
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.configure(state=tk.DISABLED)

    def clear_all(self) -> None:
        """Bersihkan semua field: input, output, dan kunci."""
        self.key_entry.delete(0, tk.END)
        self.input_text.delete("1.0", tk.END)
        self.set_output_text("")

    # ------------------------------------------------------------------ #
    #  Dialog Pesan
    # ------------------------------------------------------------------ #
    @staticmethod
    def show_error(title: str, message: str) -> None:
        """Tampilkan dialog error pop-up."""
        messagebox.showerror(title, message)

    @staticmethod
    def show_warning(title: str, message: str) -> None:
        """Tampilkan dialog peringatan pop-up."""
        messagebox.showwarning(title, message)

    @staticmethod
    def show_info(title: str, message: str) -> None:
        """Tampilkan dialog informasi pop-up."""
        messagebox.showinfo(title, message)

    # ------------------------------------------------------------------ #
    #  Internal: Placeholder Kunci
    # ------------------------------------------------------------------ #
    def _on_cipher_changed(self) -> None:
        """Dipanggil saat radio button metode cipher berubah."""
        self.key_entry.delete(0, tk.END)
        self._update_key_placeholder()

    def _update_key_placeholder(self) -> None:
        """Perbarui label dan placeholder input kunci sesuai metode."""
        method = self.cipher_var.get()
        if method == "caesar":
            self.key_label.configure(text="Kunci (Angka):")
            self.key_entry.configure(justify=tk.LEFT)
            self._set_placeholder("Masukkan angka pergeseran (misal: 3)")
        else:
            self.key_label.configure(text="Kunci (Kata):")
            self.key_entry.configure(justify=tk.LEFT)
            self._set_placeholder("Masukkan kata kunci (misal: RAHASIA)")

    def _set_placeholder(self, text: str) -> None:
        """Pasang pseudo-placeholder pada Entry kunci."""
        entry = self.key_entry
        entry.delete(0, tk.END)
        entry.insert(0, text)
        entry.configure(foreground="#aab7c4")

        def on_focus_in(_event: tk.Event) -> None:
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.configure(foreground="#2c3e50")

        def on_focus_out(_event: tk.Event) -> None:
            if not entry.get().strip():
                entry.delete(0, tk.END)
                entry.insert(0, text)
                entry.configure(foreground="#aab7c4")

        # Bersihkan binding lama agar tidak menumpuk
        entry.unbind("<FocusIn>")
        entry.unbind("<FocusOut>")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
