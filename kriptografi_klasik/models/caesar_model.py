# models/caesar_model.py
"""
Caesar Cipher Model
====================
Mengimplementasikan logika enkripsi dan dekripsi Caesar Cipher.

Rumus Matematis:
    Enkripsi : C = (M + K) mod 26
    Dekripsi : M = (C - K) mod 26

Kunci (K) adalah bilangan bulat (integer).
Karakter non-alfabet dipertahankan apa adanya pada posisi aslinya.
Format huruf besar/kecil (case) dipertahankan.
"""


class CaesarModel:
    """Model murni untuk operasi Caesar Cipher."""

    # ------------------------------------------------------------------ #
    #  Validasi
    # ------------------------------------------------------------------ #
    @staticmethod
    def validate_key(key_text: str) -> int:
        """Validasi dan konversi string kunci menjadi integer.

        Args:
            key_text: String kunci dari input pengguna.

        Returns:
            Nilai integer kunci.

        Raises:
            ValueError: Jika kunci kosong atau bukan bilangan bulat.
        """
        if not key_text or not key_text.strip():
            raise ValueError("Kunci tidak boleh kosong. Masukkan bilangan bulat.")

        stripped = key_text.strip()
        try:
            return int(stripped)
        except ValueError:
            raise ValueError(
                f"Kunci Caesar harus berupa bilangan bulat, "
                f"tetapi Anda memasukkan: '{stripped}'."
            )

    # ------------------------------------------------------------------ #
    #  Enkripsi & Dekripsi
    # ------------------------------------------------------------------ #
    @staticmethod
    def encrypt(plaintext: str, key: int) -> str:
        """Enkripsi *plaintext* dengan pergeseran *key*.

        C = (M + K) mod 26

        Args:
            plaintext: Teks asli yang akan dienkripsi.
            key: Bilangan bulat pergeseran.

        Returns:
            Ciphertext hasil enkripsi.
        """
        result: list[str] = []
        for ch in plaintext:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                shifted = (ord(ch) - base + key) % 26
                result.append(chr(base + shifted))
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def decrypt(ciphertext: str, key: int) -> str:
        """Dekripsi *ciphertext* dengan pergeseran *key*.

        M = (C - K) mod 26

        Args:
            ciphertext: Teks terenkripsi yang akan didekripsi.
            key: Bilangan bulat pergeseran.

        Returns:
            Plaintext hasil dekripsi.
        """
        result: list[str] = []
        for ch in ciphertext:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                shifted = (ord(ch) - base - key) % 26  # Python handles negative mod correctly
                result.append(chr(base + shifted))
            else:
                result.append(ch)
        return "".join(result)
