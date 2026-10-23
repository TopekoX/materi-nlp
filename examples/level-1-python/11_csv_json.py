"""CSV dan JSON dengan pustaka standar."""
import csv
import io
import json
from pathlib import Path

DATA = Path(__file__).parent / "data" / "laporan_contoh.csv"

# --8<-- [start:csv_baca]
with open(DATA, newline="", encoding="utf-8") as f:
    baris = list(csv.DictReader(f))
print(len(baris), baris[0])
print(type(baris[0]["id"]).__name__)
# --8<-- [end:csv_baca]

# --8<-- [start:saring]
print(sorted({b["label"] for b in baris}))
darurat = [b for b in baris if b["label"] == "Emergency"]
print(len(darurat))
# --8<-- [end:saring]

# --8<-- [start:csv_tulis]
buffer = io.StringIO()
penulis = csv.DictWriter(buffer, fieldnames=["id", "teks"])
penulis.writeheader()
penulis.writerow({"id": 1, "teks": "banjir, air naik"})
print(buffer.getvalue().splitlines())
print("split salah:", "1,banjir, air naik".split(","))
# --8<-- [end:csv_tulis]

# --8<-- [start:json]
s = json.dumps(darurat[0], ensure_ascii=False)
print(s)
kembali = json.loads(s)
print(kembali["lokasi"], type(kembali).__name__)
# --8<-- [end:json]

# --8<-- [start:ascii]
print(json.dumps({"teks": "tolong \U0001F64F"}))
print(json.dumps({"teks": "tolong \U0001F64F"}, ensure_ascii=False) == '{"teks": "tolong \U0001F64F"}')
print(json.loads(json.dumps({"teks": "tolong \U0001F64F"}))["teks"] == "tolong \U0001F64F")
# --8<-- [end:ascii]
