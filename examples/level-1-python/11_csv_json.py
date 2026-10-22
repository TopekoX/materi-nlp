"""CSV dan JSON dengan pustaka standar."""
import csv
import json
from pathlib import Path

DATA = Path(__file__).parent / "data" / "laporan_contoh.csv"
with open(DATA, newline="", encoding="utf-8") as f:
    baris = list(csv.DictReader(f))
print(len(baris), baris[0])
print(sorted({b["label"] for b in baris}))

darurat = [b for b in baris if b["label"] == "Emergency"]
print(len(darurat))
s = json.dumps(darurat[0], ensure_ascii=False)
print(s)
print(json.loads(s)["lokasi"])
print(json.dumps({"teks": "tolong \U0001F64F"}))
print(ascii(json.dumps({"teks": "tolong \U0001F64F"}, ensure_ascii=False)))
