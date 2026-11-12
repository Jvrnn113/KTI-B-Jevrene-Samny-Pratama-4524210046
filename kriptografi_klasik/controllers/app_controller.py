# controllers/app_controller.py
"""
Application Controller
=======================
Menjembatani View dan Model dalam arsitektur MVC.

Tanggung jawab:
- Menangkap event pengguna dari View (tombol Proses, Clear, Copy).
- Memvalidasi input menggunakan metode validasi di Model.
- Memanggil operasi enkripsi/dekripsi di Model yang sesuai.
- Memperbarui View dengan hasil atau pesan error.
"""

from __future__ import annotations

from models.caesar_model import CaesarModel
from models.vigenere_model import VigenereModel
from views.main_view import MainView


class AppController:
    """Controller utama aplikasi Kriptografi Klasik."""

    def __init__(self, view: MainView) -> None:
        self.view = view
        self.caesar_model = CaesarModel()
        self.vigenere_model = VigenereModel()

        # Hubungkan callback tombol View ke handler Controller
        self.view.set_callbacks(
            on_process=self._handle_process,
            on_clear=self._handle_clear,
            on_copy=self._handle_copy,
        )

    # ------------------------------------------------------------------ #
    #  Handler: Proses (Enkripsi / Dekripsi)
    # ------------------------------------------------------------------ #
    def _handle_process(self) -> None:
        """Handler utama saat tombol Proses ditekan."""
        cipher = self.view.get_cipher_method()   # "caesar" | "vigenere"
        mode   = self.view.get_mode()             # "encrypt" | "decrypt"
        key_raw = self.view.get_key()
        text   = self.view.get_input_text()

        # --- Validasi teks input ---
        if not text.strip():
            self.view.show_error(
                "Input Kosong",
                "Silakan masukkan teks pada area input sebelum memproses."
            )
            return

        # --- Dispatch ke model yang sesuai ---
        if cipher == "caesar":
            self._process_caesar(mode, key_raw, text)
        else:
            self._process_vigenere(mode, key_raw, text)

    # ------------------------------------------------------------------ #
    #  Caesar Cipher
    # ------------------------------------------------------------------ #
    def _process_caesar(self, mode: str, key_raw: str, text: str) -> None:
        """Validasi kunci Caesar dan jalankan enkripsi/dekripsi."""
        # Validasi kunci
        try:
            key = self.caesar_model.validate_key(key_raw)
        except ValueError as exc:
            self.view.show_error("Kunci Tidak Valid", str(exc))
            return

        # Proses
        if mode == "encrypt":
            result = self.caesar_model.encrypt(text, key)
        else:
            result = self.caesar_model.decrypt(text, key)

        self.view.set_output_text(result)

    # ------------------------------------------------------------------ #
    #  Vigenère Cipher
    # ------------------------------------------------------------------ #
    def _process_vigenere(self, mode: str, key_raw: str, text: str) -> None:
        """Validasi kunci Vigenère dan jalankan enkripsi/dekripsi."""
        # Validasi kunci
        try:
            key = self.vigenere_model.validate_key(key_raw)
        except ValueError as exc:
            self.view.show_error("Kunci Tidak Valid", str(exc))
            return

        # Proses
        if mode == "encrypt":
            result = self.vigenere_model.encrypt(text, key)
        else:
            result = self.vigenere_model.decrypt(text, key)

        self.view.set_output_text(result)

    # ------------------------------------------------------------------ #
    #  Handler: Clear
    # ------------------------------------------------------------------ #
    def _handle_clear(self) -> None:
        """Bersihkan semua field input dan output."""
        self.view.clear_all()

    # ------------------------------------------------------------------ #
    #  Handler: Copy Hasil ke Clipboard
    # ------------------------------------------------------------------ #
    def _handle_copy(self) -> None:
        """Salin isi area output ke clipboard sistem."""
        output = self.view.output_text.get("1.0", "end-1c")
        if not output.strip():
            self.view.show_warning(
                "Tidak Ada Hasil",
                "Area output masih kosong. Proses teks terlebih dahulu."
            )
            return

        self.view.root.clipboard_clear()
        self.view.root.clipboard_append(output)
        self.view.show_info("Berhasil", "Hasil telah disalin ke clipboard!")
