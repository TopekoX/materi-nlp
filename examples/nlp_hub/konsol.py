"""Pembantu konsol."""
import sys


def pakai_utf8():
    """Memaksa keluaran konsol memakai UTF-8 agar emoji tidak menyebabkan UnicodeEncodeError.

    Di Windows, konsol lama memakai cp1252 dan gagal mencetak emoji. Alternatif tanpa kode:
    jalankan `python -X utf8 skrip.py`.
    """
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
