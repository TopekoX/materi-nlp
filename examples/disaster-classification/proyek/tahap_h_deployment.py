"""Tahap H: layanan FastAPI untuk proyek: contoh request-response, validasi, penanganan error, dan waktu prediksi."""
import json
import statistics
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # folder examples/

from fastapi.testclient import TestClient

from nlp_hub.api import buat_app
from nlp_hub.konsol import pakai_utf8
from nlp_hub.layanan import pastikan_artefak

pakai_utf8()
folder = tempfile.mkdtemp()
pastikan_artefak(folder)
klien = TestClient(buat_app(folder_artefak=folder), raise_server_exceptions=False)

# --8<-- [start:contoh]
permintaan = {"teks": "Tolong, air banjir sudah masuk ke rumah kami."}
r = klien.post("/prediksi", json=permintaan)
badan = r.json()
waktu = badan.pop("waktu_ms")
print("POST /prediksi", json.dumps(permintaan, ensure_ascii=False))
print("status:", r.status_code)
print(json.dumps({k: badan[k] for k in ("skor", "label", "ambang", "zona_ragu", "versi_model")}, indent=2, ensure_ascii=False))
print("kolom respons:", sorted(badan) + ["waktu_ms"])
print("skor probabilitas dikembalikan?", "probabilitas" in badan)
# --8<-- [end:contoh]

# --8<-- [start:galat]
print("masukan kosong     ->", klien.post("/prediksi", json={"teks": ""}).status_code)
print("kolom salah        ->", klien.post("/prediksi", json={"text": "halo"}).status_code)
print("bukan JSON         ->", klien.post("/prediksi", content="halo", headers={"Content-Type": "application/json"}).status_code)
print("metode salah (GET) ->", klien.get("/prediksi").status_code)
print("alamat tidak ada   ->", klien.get("/tidak-ada").status_code)
# --8<-- [end:galat]

# --8<-- [start:waktu]
satu = []
for _ in range(50):
    satu.append(klien.post("/prediksi", json=permintaan).json()["waktu_ms"])
mulai = time.perf_counter()
klien.post("/prediksi/batch", json={"teks": [permintaan["teks"]] * 100})
batch_total = (time.perf_counter() - mulai) * 1000
print(f"waktu model per teks (50 permintaan tunggal): median {statistics.median(satu):.2f} ms, maks {max(satu):.2f} ms")
print(f"satu batch 100 teks: {batch_total:.1f} ms total (termasuk HTTP, validasi, dan pencatatan riwayat)")
# --8<-- [end:waktu]
