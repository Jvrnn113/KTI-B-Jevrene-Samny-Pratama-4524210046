# models/vigenere_model.py
"""
Vigenère Cipher Model
======================
Mengimplementasikan logika enkripsi dan dekripsi Vigenère Cipher.

Rumus Matematis:
    Enkripsi : C_i = (M_i + K_i) mod 26
    Dekripsi : M_i = (C_i - K_i) mod 26

Kunci (K) adalah kata rahasia (string alfabetik).
Keystream diulang hanya untuk karakter huruf pada teks;
karakter non-alfabet dipertahankan apa adanya tanpa menggeser indeks kunci.
Format huruf besar/kecil (case) dipertahankan.
"""


class VigenereModel:
    """Model murni untuk operasi Vigenère Cipher."""

    # ------------------------------------------------------------------ #
    #  Validasi
    # ------------------------------------------------------------------ #
    @staticmethod
    def validate_key(key_text: str) -> str:
        """Validasi string kunci Vigenère.

        Kunci hanya boleh mengandung huruf alfabet (A-Z / a-z).
        Karakter non-huruf di dalam kunci diabaikan secara otomatis.

        Args:
            key_text: String kunci dari input pengguna.

        Returns:
            Kunci yang telah dibersihkan (huruf-huruf saja, uppercase).

        Raises:
            ValueError: Jika kunci kosong atau tidak mengandung huruf sama sekali.
        """
        if not key_text or not key_text.strip():
            raise ValueError("Kunci tidak boleh kosong. Masukkan kata kunci alfabetik.")

        # Ambil hanya huruf, abaikan karakter non-huruf
        alpha_only = "".join(ch for ch in key_text if ch.isalpha())

        if not alpha_only:
            raise ValueError(
                "Kunci Vigenère harus mengandung minimal satu huruf alfabet, "
                f"tetapi Anda memasukkan: '{key_text.strip()}'."
            )

        return alpha_only.upper()

    # ------------------------------------------------------------------ #
    #  Helper: Keystream Generator
    # ------------------------------------------------------------------ #
    @staticmethod
    def _keystream(key: str):
        """Generator tak-terbatas yang mengulang karakter kunci.

        Yields:
            Nilai integer 0-25 yang merepresentasikan setiap huruf kunci.
        """
        length = len(key)
        index = 0
        while True:
            yield ord(key[index % length]) - ord('A')
            index += 1

    # ------------------------------------------------------------------ #
    #  Enkripsi & Dekripsi
    # ------------------------------------------------------------------ #
    @classmethod
    def encrypt(cls, plaintext: str, key: str) -> str:
        """Enkripsi *plaintext* dengan kunci *key*.

        C_i = (M_i + K_i) mod 26

        Args:
            plaintext: Teks asli yang akan dienkripsi.
            key: Kunci huruf kapital yang telah divalidasi.

        Returns:
            Ciphertext hasil enkripsi.
        """
        ks = cls._keystream(key)
        result: list[str] = []
        for ch in plaintext:
            if ch.isalpha():
                k = next(ks)
                base = ord('A') if ch.isupper() else ord('a')
                shifted = (ord(ch) - base + k) % 26
                result.append(chr(base + shifted))
            else:
                # Karakter non-huruf: pertahankan, JANGAN geser indeks kunci
                result.append(ch)
        return "".join(result)

    @classmethod
    def decrypt(cls, ciphertext: str, key: str) -> str:
        """Dekripsi *ciphertext* dengan kunci *key*.

        M_i = (C_i - K_i) mod 26

        Args:
            ciphertext: Teks terenkripsi yang akan didekripsi.
            key: Kunci huruf kapital yang telah divalidasi.

        Returns:
            Plaintext hasil dekripsi.
        """
        ks = cls._keystream(key)
        result: list[str] = []
        for ch in ciphertext:
            if ch.isalpha():
                k = next(ks)
                base = ord('A') if ch.isupper() else ord('a')
                shifted = (ord(ch) - base - k) % 26
                result.append(chr(base + shifted))
            else:
                result.append(ch)
        return "".join(result)
