# Kriptografi Klasik — Caesar & Vigenère Cipher

Aplikasi desktop GUI berbasis **Python 3 + Tkinter** yang mengimplementasikan algoritma kriptografi klasik (**Caesar Cipher** dan **Vigenère Cipher**) dengan arsitektur **Model-View-Controller (MVC)** yang bersih dan modular.

---

## Daftar Isi

1. [Prasyarat](#prasyarat)
2. [Cara Menjalankan](#cara-menjalankan)
3. [Struktur Proyek](#struktur-proyek)
4. [Arsitektur MVC](#arsitektur-mvc)
5. [Algoritma Kriptografi](#algoritma-kriptografi)
   - [Caesar Cipher](#1-caesar-cipher)
   - [Vigenère Cipher](#2-vigenère-cipher)
6. [Penanganan Teks](#penanganan-teks)
7. [Fitur GUI](#fitur-gui)
8. [Dokumentasi Modul](#dokumentasi-modul)
9. [Contoh Penggunaan](#contoh-penggunaan)
10. [Lisensi](#lisensi)

---

## Prasyarat

| Kebutuhan | Keterangan |
|-----------|------------|
| **Python** | Versi 3.8 atau lebih baru |
| **Library** | `tkinter` (sudah termasuk dalam instalasi standar Python) |
| **Dependensi Eksternal** | **Tidak ada** — cukup Python standar |

> **Catatan:** Pada beberapa distribusi Linux, `tkinter` mungkin perlu diinstal terpisah:
> ```bash
> sudo apt-get install python3-tk   # Debian / Ubuntu
> ```

---

## Cara Menjalankan

```bash
# 1. Buka terminal / command prompt
# 2. Masuk ke direktori proyek
cd kriptografi_klasik

# 3. Jalankan aplikasi
python main.py
```

Jendela GUI akan terbuka dan aplikasi siap digunakan.

---

## Struktur Proyek

```
kriptografi_klasik/
│
├── models/                     # Layer MODEL — Logika bisnis kriptografi
│   ├── __init__.py             # Package init, mengekspor CaesarModel & VigenereModel
│   ├── caesar_model.py         # Implementasi Caesar Cipher
│   └── vigenere_model.py       # Implementasi Vigenère Cipher
│
├── views/                      # Layer VIEW — Antarmuka grafis (GUI)
│   ├── __init__.py             # Package init, mengekspor MainView
│   └── main_view.py            # Layout widget, styling, dan binding UI
│
├── controllers/                # Layer CONTROLLER — Penghubung View ↔ Model
│   ├── __init__.py             # Package init, mengekspor AppController
│   └── app_controller.py       # Event handler, validasi, dispatch ke Model
│
├── main.py                     # Entry point — menginisialisasi MVC & mainloop
└── README.md                   # Dokumentasi proyek (file ini)
```

---

## Arsitektur MVC

Aplikasi ini menggunakan pola **Model-View-Controller (MVC)** murni:

```
┌──────────────────────────────────────────────────────────────┐
│                           main.py                            │
│            (Inisialisasi Root, View, Controller)             │
└──────────┬──────────────────────┬────────────────────────────┘
           │                      │
           ▼                      ▼
┌─────────────────┐    ┌───────────────────────┐
│      VIEW       │◄──►│       CONTROLLER      │
│  (main_view.py) │    │  (app_controller.py)  │
│                 │    │                       │
│ • Layout GUI    │    │ • Tangkap event user  │
│ • Widget state  │    │ • Validasi input      │
│ • Dialog pesan  │    │ • Panggil Model       │
│ • Callback bind │    │ • Update View         │
└─────────────────┘    └───────────┬───────────┘
                                   │
                                   ▼
                       ┌───────────────────────┐
                       │         MODEL         │
                       │ • caesar_model.py     │
                       │ • vigenere_model.py   │
                       │                       │
                       │ • Rumus matematis     │
                       │ • Enkripsi / Dekripsi │
                       │ • Validasi kunci      │
                       └───────────────────────┘
```

### Alur Data

1. **User** berinteraksi dengan **View** (klik tombol, isi field).
2. **View** meneruskan event ke **Controller** via callback.
3. **Controller** memvalidasi input, lalu memanggil **Model** yang sesuai.
4. **Model** menjalankan operasi kriptografi murni dan mengembalikan hasil.
5. **Controller** menerima hasil dan memperbarui **View** (menampilkan output atau dialog error).

---

## Algoritma Kriptografi

### 1. Caesar Cipher

Algoritma substitusi monoalfabetik yang menggeser setiap huruf sebanyak *K* posisi dalam alfabet.

| Operasi | Rumus |
|---------|-------|
| **Enkripsi** | `C = (M + K) mod 26` |
| **Dekripsi** | `M = (C − K) mod 26` |

- **M** = Nilai numerik huruf plaintext (A=0, B=1, ..., Z=25)
- **C** = Nilai numerik huruf ciphertext
- **K** = Kunci berupa bilangan bulat (integer)

**Contoh** (K = 3):

| Plaintext  | H  | e  | l  | l  | o  |
|------------|----|----|----|----|-----|
| Nilai M    | 7  | 4  | 11 | 11 | 14  |
| (M+3) % 26| 10 | 7  | 14 | 14 | 17  |
| Ciphertext | K  | h  | o  | o  | r   |

> Huruf besar tetap besar, huruf kecil tetap kecil.

### 2. Vigenère Cipher

Algoritma substitusi polialfabetik yang menggunakan kata kunci berulang sebagai deretan pergeseran.

| Operasi | Rumus |
|---------|-------|
| **Enkripsi** | `C_i = (M_i + K_i) mod 26` |
| **Dekripsi** | `M_i = (C_i − K_i) mod 26` |

- **M_i** = Nilai numerik huruf plaintext ke-*i*
- **C_i** = Nilai numerik huruf ciphertext ke-*i*
- **K_i** = Nilai numerik huruf kunci ke-*i* (kunci diulang secara siklik)

**Aturan Keystream:**
- Indeks kunci hanya maju ketika memproses karakter **huruf**.
- Karakter non-huruf (spasi, angka, tanda baca) **tidak** menggeser indeks kunci.

**Contoh** (K = "KEY"):

| Plaintext  | H  | e  | l  | l  | o  | ,  | ␣  | W  | o  | r  | l  | d  | !  |
|------------|----|----|----|----|----|----|----|----|----|----|----|----|-----|
| Kunci      | K  | E  | Y  | K  | E  | —  | —  | Y  | K  | E  | Y  | K  | —  |
| Ciphertext | R  | i  | j  | v  | s  | ,  | ␣  | U  | y  | v  | j  | n  | !  |

> Tanda koma, spasi, dan tanda seru tidak berubah dan tidak mengonsumsi huruf kunci.

---

## Penanganan Teks

Aturan penanganan teks berlaku untuk **kedua** cipher:

| Aturan | Keterangan |
|--------|------------|
| **Case-preserving** | Huruf besar → tetap besar; huruf kecil → tetap kecil |
| **Non-alfabet dipertahankan** | Spasi, angka, tanda baca (`!@#$,.` dll.) tetap pada posisi asli |
| **Multi-line** | Mendukung kalimat panjang, paragraf, dan baris baru |

---

## Fitur GUI

| Fitur | Deskripsi |
|-------|-----------|
| **Pemilihan Cipher** | Radio button untuk memilih Caesar atau Vigenère |
| **Pemilihan Mode** | Radio button untuk memilih Enkripsi atau Dekripsi |
| **Input Kunci Dinamis** | Label dan placeholder berubah sesuai metode cipher |
| **Area Input Multi-line** | ScrolledText untuk memasukkan plaintext / ciphertext |
| **Tombol Proses** | Menjalankan enkripsi / dekripsi |
| **Tombol Clear Text** | Membersihkan semua field (input, output, kunci) |
| **Tombol Copy Hasil** | Menyalin hasil output ke clipboard sistem |
| **Area Output Read-only** | ScrolledText yang menampilkan hasil (tidak dapat diedit manual) |
| **Dialog Error** | Pop-up error jika input kosong atau kunci tidak valid |
| **Styling Modern** | Tema `clam` dengan skema warna profesional |

---

## Dokumentasi Modul

### `models/caesar_model.py` — `CaesarModel`

| Metode | Parameter | Return | Deskripsi |
|--------|-----------|--------|-----------|
| `validate_key(key_text)` | `str` | `int` | Validasi & konversi string ke integer. Raise `ValueError` jika tidak valid. |
| `encrypt(plaintext, key)` | `str`, `int` | `str` | Enkripsi plaintext dengan pergeseran key. |
| `decrypt(ciphertext, key)` | `str`, `int` | `str` | Dekripsi ciphertext dengan pergeseran key. |

### `models/vigenere_model.py` — `VigenereModel`

| Metode | Parameter | Return | Deskripsi |
|--------|-----------|--------|-----------|
| `validate_key(key_text)` | `str` | `str` | Validasi string kunci, kembalikan huruf saja (uppercase). Raise `ValueError` jika tidak valid. |
| `encrypt(plaintext, key)` | `str`, `str` | `str` | Enkripsi plaintext dengan kata kunci. |
| `decrypt(ciphertext, key)` | `str`, `str` | `str` | Dekripsi ciphertext dengan kata kunci. |

### `views/main_view.py` — `MainView`

| Metode | Deskripsi |
|--------|-----------|
| `set_callbacks(on_process, on_clear, on_copy)` | Hubungkan tombol ke callback Controller. |
| `get_cipher_method()` | Kembalikan metode cipher terpilih (`"caesar"` / `"vigenere"`). |
| `get_mode()` | Kembalikan mode operasi (`"encrypt"` / `"decrypt"`). |
| `get_key()` | Kembalikan string kunci dari Entry. |
| `get_input_text()` | Kembalikan isi area teks input. |
| `set_output_text(text)` | Tampilkan teks di area output (read-only). |
| `clear_all()` | Bersihkan semua field. |
| `show_error(title, message)` | Tampilkan dialog error pop-up. |
| `show_warning(title, message)` | Tampilkan dialog peringatan pop-up. |
| `show_info(title, message)` | Tampilkan dialog informasi pop-up. |

### `controllers/app_controller.py` — `AppController`

| Metode | Deskripsi |
|--------|-----------|
| `__init__(view)` | Inisialisasi Controller, hubungkan View dengan Model. |
| `_handle_process()` | Handler tombol Proses: validasi → dispatch → update View. |
| `_process_caesar(mode, key_raw, text)` | Sub-handler untuk operasi Caesar Cipher. |
| `_process_vigenere(mode, key_raw, text)` | Sub-handler untuk operasi Vigenère Cipher. |
| `_handle_clear()` | Handler tombol Clear Text. |
| `_handle_copy()` | Handler tombol Copy Hasil ke clipboard. |

### `main.py`

| Fungsi | Deskripsi |
|--------|-----------|
| `main()` | Entry point: buat root Tk, inisialisasi View & Controller, jalankan `mainloop()`. |

---

## Contoh Penggunaan

### Caesar Cipher — Enkripsi

```
Metode  : Caesar Cipher
Mode    : Enkripsi
Kunci   : 3
Input   : Hello, World! 123
Output  : Khoor, Zruog! 123
```

### Caesar Cipher — Dekripsi

```
Metode  : Caesar Cipher
Mode    : Dekripsi
Kunci   : 3
Input   : Khoor, Zruog! 123
Output  : Hello, World! 123
```

### Vigenère Cipher — Enkripsi

```
Metode  : Vigenère Cipher
Mode    : Enkripsi
Kunci   : KEY
Input   : Hello, World!
Output  : Rijvs, Uyvjn!
```

### Vigenère Cipher — Dekripsi

```
Metode  : Vigenère Cipher
Mode    : Dekripsi
Kunci   : KEY
Input   : Rijvs, Uyvjn!
Output  : Hello, World!
```

---

## Lisensi

Proyek ini dibuat untuk keperluan edukasi mata kuliah **Kriptografi** — Semester 5, Program Studi Teknologi Informasi.

---

*Dibuat menggunakan Python 3 & Tkinter*
