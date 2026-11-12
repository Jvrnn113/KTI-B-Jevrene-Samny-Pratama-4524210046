# main.py
"""
APP — Entry Point
=========================
Titik masuk utama aplikasi Kriptografi Klasik berbasis GUI.

Menginisialisasi komponen MVC:
1. Root window Tkinter.
2. View (MainView) — antarmuka grafis.
3. Controller (AppController) — penghubung View ↔ Model.
"""

import tkinter as tk

from views.main_view import MainView
from controllers.app_controller import AppController


def main() -> None:
    """Bangun dan jalankan aplikasi."""
    root = tk.Tk()

    # Inisialisasi View
    view = MainView(root)

    # Inisialisasi Controller (menghubungkan View ↔ Model secara internal)
    _controller = AppController(view)  # noqa: F841  — referensi dijaga oleh callback

    # Main loop
    root.mainloop()


if __name__ == "__main__":
    main()
