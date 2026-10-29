"""Uji inti layanan (artefak, penilai, riwayat) dan alat Level 7 (kalibrasi, interpretasi, pemantauan)."""
import numpy as np
import pytest

from nlp_hub.interpretasi import cakupan_kosakata, kontribusi_linear, oklusi_kata
from nlp_hub.kalibrasi import ece, pilih_ambang_target_recall, skor_brier, tabel_reliabilitas
from nlp_hub.layanan import ArtefakTidakValid, Penilai, hash_teks, muat_artefak, pastikan_artefak, simpan_artefak
from nlp_hub.pantau import psi
from nlp_hub.proyek import model_rujukan, siapkan
from nlp_hub.riwayat import Riwayat


@pytest.fixture(scope="module")
def model():
    return model_rujukan(siapkan())


@pytest.fixture()
def folder(tmp_path, model):
    simpan_artefak(model, tmp_path, "uji-0.1")
    return tmp_path


# ------------------------------------------------------------------ artefak
def test_simpan_dan_muat_menghasilkan_skor_identik(folder, model):
    dimuat, meta = muat_artefak(folder)
    teks = ["Tolong, air sudah masuk rumah", "Webinar mitigasi banjir"]
    assert np.allclose(dimuat.decision_function(teks), model.decision_function(teks))
    assert meta["model_version"] == "uji-0.1" and meta["ambang_tervalidasi"] is False
    assert meta["jenis_keluaran"] == "skor_keputusan_svm"


def test_checksum_berubah_ditolak(folder):
    berkas = folder / "model.joblib"
    berkas.write_bytes(berkas.read_bytes() + b"x")
    with pytest.raises(ArtefakTidakValid, match="checksum"):
        muat_artefak(folder)


def test_artefak_hilang_dan_json_rusak(tmp_path, folder):
    with pytest.raises(ArtefakTidakValid, match="tidak ada"):
        muat_artefak(tmp_path / "kosong")
    (folder / "model.json").write_text("{bukan json", encoding="utf-8")
    with pytest.raises(ArtefakTidakValid, match="JSON"):
        muat_artefak(folder)


def test_pastikan_artefak_membuat_sekali_saja(tmp_path):
    m1 = pastikan_artefak(tmp_path / "a")
    m2 = pastikan_artefak(tmp_path / "a")
    assert m1["sha256"] == m2["sha256"]


# ------------------------------------------------------------------ penilai
def test_penilai_keluaran_dan_zona_ragu(model):
    p = Penilai(model, {"ambang": 0.0, "margin_ragu": 0.3})
    h = p.nilai(["Tolong, air banjir sudah masuk ke rumah kami.", "Webinar mitigasi banjir gratis"])
    assert h[0]["label"] == "Emergency" and h[1]["label"] == "Non-Emergency"
    assert set(h[0]) == {"skor", "label", "ambang", "zona_ragu"}


def test_ambang_menentukan_label(model):
    teks = ["Tolong, air banjir sudah masuk ke rumah kami."]
    skor = Penilai(model, {"ambang": 0.0}).nilai(teks)[0]["skor"]
    assert Penilai(model, {"ambang": 0.0}).nilai(teks)[0]["label"] == "Emergency"
    assert Penilai(model, {"ambang": skor + 1}).nilai(teks)[0]["label"] == "Non-Emergency"


@pytest.mark.parametrize("masukan, galat", [("satu string", TypeError), ([""], ValueError), (["  "], ValueError),
                                           ([123], ValueError), (["a" * 1001], ValueError)])
def test_penilai_menolak_masukan_buruk(model, masukan, galat):
    with pytest.raises(galat):
        Penilai(model, {"ambang": 0.0}).nilai(masukan)


def test_penilai_menolak_model_tanpa_skor_dan_daftar_kosong_aman(model):
    assert Penilai(model, {"ambang": 0.0}).nilai([]) == []
    with pytest.raises(TypeError, match="decision_function"):
        Penilai(object(), {"ambang": 0.0})


def test_hash_teks_stabil_dan_tidak_membocorkan_teks():
    assert hash_teks("abc") == hash_teks("abc") and len(hash_teks("abc")) == 12 and "abc" not in hash_teks("abc")


# ------------------------------------------------------------------ riwayat
def test_riwayat_tidak_menyimpan_teks_secara_bawaan():
    r = Riwayat()
    h = {"skor": 0.5, "label": "Emergency", "zona_ragu": False}
    r.catat("rahasia", hash_teks("rahasia"), h, "v1")
    isi = r.sambungan.execute("SELECT teks FROM prediksi").fetchone()[0]
    assert isi is None
    assert r.ringkasan() == {"total": 1, "per_label": {"Emergency": 1}, "zona_ragu": 0, "skor_rata_rata": 0.5}


def test_riwayat_menyimpan_teks_bila_diminta_dan_kosong_aman():
    assert Riwayat().ringkasan()["total"] == 0 and Riwayat().terbaru() == []
    r = Riwayat(simpan_teks=True)
    r.catat("halo", "h", {"skor": -1.0, "label": "Non-Emergency", "zona_ragu": True}, "v1")
    assert r.sambungan.execute("SELECT teks FROM prediksi").fetchone()[0] == "halo"


# ------------------------------------------------------------------ kalibrasi
def test_ece_nol_untuk_prediksi_sempurna_dan_besar_untuk_salah():
    y = np.array([0, 0, 1, 1])
    assert ece(y, np.array([0.0, 0.0, 1.0, 1.0])) == pytest.approx(0.0)
    assert ece(y, np.array([1.0, 1.0, 0.0, 0.0])) == pytest.approx(1.0)


def test_tabel_reliabilitas_menjumlah_ke_n_dan_p_satu_masuk():
    t = tabel_reliabilitas(np.array([0, 1, 1]), np.array([0.0, 0.5, 1.0]), n_bin=5)
    assert sum(b[2] for b in t) == 3


def test_brier():
    assert skor_brier([1, 0], [1.0, 0.0]) == 0.0 and skor_brier([1, 0], [0.0, 1.0]) == 1.0


def test_ambang_target_recall():
    y = np.array([1, 1, 1, 1, 0, 0])
    skor = np.array([0.9, 0.8, 0.4, 0.3, 0.5, 0.1])
    ambang, presisi, recall = pilih_ambang_target_recall(y, skor, 0.75)
    assert ambang == 0.4 and recall == 0.75 and presisi == pytest.approx(0.75)
    with pytest.raises(ValueError, match="positif"):
        pilih_ambang_target_recall(np.zeros(3, dtype=int), np.arange(3.0), 0.5)


# ------------------------------------------------------------------ interpretasi & pemantauan
def test_kontribusi_menjumlah_ke_skor(model):
    teks = "Tolong, air banjir sudah masuk ke rumah kami."
    semua, intersep = kontribusi_linear(model, teks, atas=10_000)
    assert sum(v for _, v in semua) + intersep == pytest.approx(model.decision_function([teks])[0])


def test_oklusi_kata_dan_satu_kata(model):
    hasil, dasar = oklusi_kata(model, "Tolong air masuk rumah")
    assert [k for k, _ in hasil] == ["Tolong", "air", "masuk", "rumah"] and np.isfinite(dasar)
    assert len(oklusi_kata(model, "banjir")[0]) == 1          # teks satu kata tidak menyebabkan galat


def test_cakupan_kosakata_rentang(model):
    assert 0.9 < cakupan_kosakata(model, ["tolong air masuk rumah"]) <= 1.0
    assert cakupan_kosakata(model, ["zzzz qqqq"]) == 0.0


def test_psi_nol_untuk_data_sama_dan_besar_untuk_geser():
    rng = np.random.default_rng(0)
    a = rng.normal(size=2000)
    assert psi(a, a) == pytest.approx(0.0, abs=1e-9)
    assert psi(a, rng.normal(size=2000)) < 0.1
    assert psi(a, rng.normal(loc=2.0, size=2000)) > 0.25
