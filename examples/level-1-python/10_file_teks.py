"""Membaca dan menulis file teks (UTF-8)."""
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / "catatan.txt"
    p.write_text("banjir naik\ntolong evakuasi \U0001F64F\n", encoding="utf-8")
    isi = p.read_text(encoding="utf-8")
    print(ascii(isi))
    with open(p, encoding="utf-8") as f:
        for no, baris in enumerate(f, start=1):
            print(no, ascii(baris.rstrip("\n")))
    with open(p, "a", encoding="utf-8") as f:
        f.write("pos bantuan dibuka\n")
    print(len(p.read_text(encoding="utf-8").splitlines()))
try:
    Path("tidak_ada.txt").read_text(encoding="utf-8")
except FileNotFoundError:
    print("FileNotFoundError")
