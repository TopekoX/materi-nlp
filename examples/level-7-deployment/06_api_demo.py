"""Memanggil API FastAPI tanpa membuka port: TestClient menjalankan aplikasi di dalam proses yang sama."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

from fastapi.testclient import TestClient

from nlp_hub.api import buat_app
from nlp_hub.konsol import pakai_utf8
from nlp_hub.layanan import pastikan_artefak

pakai_utf8()
ARTEFAK = Path(__file__).resolve().parent / "artefak"
pastikan_artefak(ARTEFAK)

# --8<-- [start:mulai]
app = buat_app(folder_artefak=ARTEFAK, path_db=":memory:")
klien = TestClient(app, raise_server_exceptions=False)
r = klien.get("/kesehatan")
print(r.status_code, r.json())
# --8<-- [end:mulai]

# --8<-- [start:prediksi]
r = klien.post("/prediksi", json={"teks": "Tolong, air banjir sudah masuk ke rumah kami."})
badan = r.json()
waktu = badan.pop("waktu_ms")                              # nilai waktu berubah-ubah; dicetak terpisah
print(r.status_code)
print(json.dumps(badan, indent=2, ensure_ascii=False))
print("waktu_ms ada dan bukan negatif:", isinstance(waktu, float) and waktu >= 0)
# --8<-- [end:prediksi]

# --8<-- [start:validasi]
for badan in ({"teks": ""}, {"teks": "   "}, {"kolom_salah": "x"}, {"teks": "a" * 1001}):
    r = klien.post("/prediksi", json=badan)
    detail = r.json()["detail"]
    pesan = detail if isinstance(detail, str) else detail[0]["msg"]
    print(f"{str(badan)[:30]:32} -> {r.status_code} | {pesan}")
# --8<-- [end:validasi]

# --8<-- [start:batch]
teks_batch = [
    "Tolong, air banjir sudah masuk ke rumah kami.",
    "Pemerintah mengumumkan pembangunan tanggul untuk mengurangi risiko banjir.",
    "Gempa terasa kuat, warga diminta menjauhi bangunan yang rusak.",
    "Saya sedang membaca berita tentang gempa tahun lalu.",
]
r = klien.post("/prediksi/batch", json={"teks": teks_batch})
for t, h in zip(teks_batch, r.json()["hasil"]):
    print(f"skor {h['skor']:+.3f} | {h['label']:13} | ragu: {str(h['zona_ragu']):5} | {t[:55]}")
print("batch 101 teks ->", klien.post("/prediksi/batch", json={"teks": ["x"] * 101}).status_code)
# --8<-- [end:batch]

# --8<-- [start:riwayat]
print(klien.get("/riwayat/ringkasan").json())
print("kolom riwayat:", list(klien.get("/riwayat/terbaru?n=1").json()[0]))
print("teks asli tersimpan di riwayat?", "teks" in klien.get("/riwayat/terbaru?n=1").json()[0])
print("dasbor HTML:", klien.get("/dasbor").status_code, "| memuat catatan wajib:", "bukan penentuan keadaan darurat" in klien.get("/dasbor").text)
# --8<-- [end:riwayat]

# --8<-- [start:galat]
app.state.penilai.model = None                               # mensimulasikan kerusakan internal
r = klien.post("/prediksi", json={"teks": "tes"})
print(r.status_code, r.json()["detail"], "| ada id_galat:", "id_galat" in r.json(), "| jejak tumpukan bocor ke klien:", "Traceback" in r.text)
# --8<-- [end:galat]
