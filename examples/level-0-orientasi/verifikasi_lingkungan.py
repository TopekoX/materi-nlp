"""Memeriksa lingkungan belajar. Jalankan: python examples/level-0-orientasi/verifikasi_lingkungan.py"""
import importlib
import sys

PAKET_WAJIB = ["numpy", "pandas", "sklearn", "matplotlib", "Sastrawi", "joblib"]
PAKET_OPSIONAL = ["fastapi", "pytest", "torch", "transformers"]


def versi(nama_modul):
    """Mengembalikan versi paket, atau None bila tidak terpasang."""
    try:
        modul = importlib.import_module(nama_modul)
    except ImportError:
        return None
    return getattr(modul, "__version__", "terpasang")


def main():
    print(f"Python  : {sys.version.split()[0]}")
    print(f"Lokasi  : {sys.executable}")
    gagal = []
    for nama in PAKET_WAJIB:
        v = versi(nama)
        print(f"[{'OK' if v else 'XX'}] {nama:12} {v or 'TIDAK TERPASANG'}")
        if not v:
            gagal.append(nama)
    for nama in PAKET_OPSIONAL:
        v = versi(nama)
        print(f"[{'OK' if v else '--'}] {nama:12} {v or 'tidak terpasang (opsional)'}")
    if gagal:
        print("\nPaket wajib belum terpasang:", ", ".join(gagal))
        print("Jalankan: pip install -r requirements-ml.txt")
        return 1
    print("\nLingkungan siap untuk Level 1-5.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
