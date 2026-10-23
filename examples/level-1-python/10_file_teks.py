"""Membaca dan menulis file teks (UTF-8)."""
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / "catatan.txt"

    # --8<-- [start:tulis]
    p.write_text("banjir naik\ntolong evakuasi \U0001F64F\n", encoding="utf-8")
    print(p.name, p.exists())
    # --8<-- [end:tulis]

    # --8<-- [start:baca]
    isi = p.read_text(encoding="utf-8")
    print(ascii(isi))
    print(len(isi), len(isi.encode("utf-8")))
    # --8<-- [end:baca]

    # --8<-- [start:baris]
    with open(p, encoding="utf-8") as f:
        for no, baris in enumerate(f, start=1):
            print(no, ascii(baris.rstrip("\n")))
    # --8<-- [end:baris]

    # --8<-- [start:tambah]
    with open(p, "a", encoding="utf-8") as f:
        f.write("pos bantuan dibuka\n")
    print(len(p.read_text(encoding="utf-8").splitlines()))
    # --8<-- [end:tambah]

    # --8<-- [start:encoding_salah]
    try:
        p.read_text(encoding="ascii")
    except UnicodeDecodeError as e:
        print("UnicodeDecodeError:", e.reason)
    mentah = p.read_bytes()[:8]
    print(mentah)
    # --8<-- [end:encoding_salah]

# --8<-- [start:tidak_ada]
try:
    Path("tidak_ada.txt").read_text(encoding="utf-8")
except FileNotFoundError:
    print("FileNotFoundError")
# --8<-- [end:tidak_ada]
