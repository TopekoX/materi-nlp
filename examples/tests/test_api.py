"""Uji API FastAPI (Level 7). Memakai TestClient: tanpa port jaringan dan tanpa server sungguhan."""
import pytest
from fastapi.testclient import TestClient

from nlp_hub.api import buat_app
from nlp_hub.layanan import ArtefakTidakValid, pastikan_artefak

LAPORAN = "Tolong, air banjir sudah masuk ke rumah kami."


@pytest.fixture()
def klien(tmp_path):
    pastikan_artefak(tmp_path / "artefak")
    app = buat_app(folder_artefak=tmp_path / "artefak", path_db=":memory:")
    return TestClient(app, raise_server_exceptions=False)


def test_kesehatan_dan_info(klien):
    assert klien.get("/kesehatan").json()["status"] == "ok"
    info = klien.get("/model/info").json()
    assert info["jenis_keluaran"] == "skor_keputusan_svm" and info["ambang_tervalidasi"] is False


def test_prediksi_bentuk_respons_dan_tanpa_klaim_probabilitas(klien):
    r = klien.post("/prediksi", json={"teks": LAPORAN})
    j = r.json()
    assert r.status_code == 200 and j["label"] == "Emergency"
    assert "probabilitas" not in j and "bukan penentuan keadaan darurat" in j["catatan"]


@pytest.mark.parametrize("badan", [{}, {"teks": ""}, {"teks": "   "}, {"teks": 5}, {"teks": "a" * 1001}, {"teks": None}])
def test_masukan_tidak_valid_422(klien, badan):
    assert klien.post("/prediksi", json=badan).status_code == 422


def test_batch_urutan_sama_dan_batas(klien):
    teks = [LAPORAN, "Webinar mitigasi banjir gratis"]
    h = klien.post("/prediksi/batch", json={"teks": teks}).json()["hasil"]
    assert [x["label"] for x in h] == ["Emergency", "Non-Emergency"]
    assert klien.post("/prediksi/batch", json={"teks": []}).status_code == 422
    assert klien.post("/prediksi/batch", json={"teks": ["x"] * 101}).status_code == 422
    assert klien.post("/prediksi/batch", json={"teks": [LAPORAN, ""]}).status_code == 422


def test_batch_sama_dengan_prediksi_satuan(klien):
    teks = [LAPORAN, "Saya sedang membaca berita tentang gempa tahun lalu."]
    satu = [klien.post("/prediksi", json={"teks": t}).json()["skor"] for t in teks]
    batch = [x["skor"] for x in klien.post("/prediksi/batch", json={"teks": teks}).json()["hasil"]]
    assert satu == batch


def test_riwayat_mencatat_tanpa_teks_asli(klien):
    klien.post("/prediksi", json={"teks": LAPORAN})
    assert klien.get("/riwayat/ringkasan").json()["total"] == 1
    baris = klien.get("/riwayat/terbaru").json()[0]
    assert "teks" not in baris and LAPORAN not in str(baris)
    assert klien.get("/dasbor").status_code == 200


def test_input_ditolak_tidak_tercatat(klien):
    klien.post("/prediksi", json={"teks": ""})
    assert klien.get("/riwayat/ringkasan").json()["total"] == 0


def test_riwayat_n_dibatasi(klien):
    assert klien.get("/riwayat/terbaru?n=100000").status_code == 200
    assert klien.get("/riwayat/terbaru?n=abc").status_code == 422


def test_ambang_dapat_diatur_dan_mengubah_label(tmp_path):
    pastikan_artefak(tmp_path / "a")
    app = buat_app(folder_artefak=tmp_path / "a", ambang=5.0)
    r = TestClient(app).post("/prediksi", json={"teks": LAPORAN}).json()
    assert r["ambang"] == 5.0 and r["label"] == "Non-Emergency"


def test_ambang_dari_variabel_lingkungan(tmp_path, monkeypatch):
    pastikan_artefak(tmp_path / "a")
    monkeypatch.setenv("NLP_HUB_AMBANG", "-0.5")
    app = buat_app(folder_artefak=tmp_path / "a")
    assert TestClient(app).get("/model/info").json()["ambang_dipakai"] == -0.5


def test_galat_internal_tidak_membocorkan_detail(klien):
    klien.app.state.penilai.model = None
    r = klien.post("/prediksi", json={"teks": LAPORAN})
    assert r.status_code == 500 and "Traceback" not in r.text and "NoneType" not in r.text
    assert len(r.json()["id_galat"]) == 8


def test_start_gagal_cepat_bila_artefak_tidak_ada(tmp_path):
    with pytest.raises(ArtefakTidakValid):
        buat_app(folder_artefak=tmp_path / "tidak-ada")


def test_dokumentasi_openapi_tersedia(klien):
    skema = klien.get("/openapi.json").json()
    assert "/prediksi" in skema["paths"] and "/prediksi/batch" in skema["paths"]


def test_batas_panjang_teks_tepat(klien):
    assert klien.post("/prediksi", json={"teks": "a" * 1000}).status_code == 200
    assert klien.post("/prediksi", json={"teks": "a" * 1001}).status_code == 422


def test_waktu_prediksi_ada_dan_masuk_akal(klien):
    j = klien.post("/prediksi", json={"teks": LAPORAN}).json()
    assert isinstance(j["waktu_ms"], float) and 0 <= j["waktu_ms"] < 5000
    h = klien.post("/prediksi/batch", json={"teks": [LAPORAN, LAPORAN]}).json()["hasil"]
    assert h[0]["waktu_ms"] == h[1]["waktu_ms"]            # batch: rata-rata per teks, sama untuk semua butir
