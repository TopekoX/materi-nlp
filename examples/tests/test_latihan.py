"""Uji kunci jawaban kode pada folder latihan/: jawaban yang dipublikasikan harus benar."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "latihan"))

from solusi_level_0_1 import ekstrak_penanda, hitung_kata, prediksi_kata_kunci  # noqa: E402
from solusi_level_2_3 import idf_tangan  # noqa: E402
from solusi_level_4_5 import hitung_metrik  # noqa: E402


def test_hitung_kata():
    assert hitung_kata("Tolong, air! tolong.") == {"tolong": 2, "air": 1}
    assert hitung_kata("") == {} and hitung_kata("... !!!") == {}


def test_ekstrak_penanda_tidak_menghitung_email():
    assert ekstrak_penanda("#a #b @x a@b.com") == (["a", "b"], ["x"])
    assert ekstrak_penanda("tanpa penanda") == ([], [])


def test_kata_kunci_mudah_tertipu():
    assert prediksi_kata_kunci("Tolong follow akun saya") == "Emergency"            # alarm palsu
    assert prediksi_kata_kunci("Air sudah sepinggang, anak saya terjebak") == "Non-Emergency"   # terlewat


def test_idf_tangan_sama_dengan_sklearn():
    from sklearn.feature_extraction.text import TfidfVectorizer
    korpus = ["air masuk rumah", "tolong air naik", "tolong tolong kirim bantuan"]
    tv = TfidfVectorizer().fit(korpus)
    for kata in ("air", "tolong", "rumah"):
        assert idf_tangan([k.split() for k in korpus], kata) == pytest.approx(tv.idf_[list(tv.get_feature_names_out()).index(kata)])


def test_hitung_metrik_nilai_diketahui_dan_nol_aman():
    m = hitung_metrik(tp=15, fp=0, fn=9, tn=24)
    assert m["recall"] == pytest.approx(0.625) and m["presisi"] == 1.0 and m["akurasi"] == pytest.approx(39 / 48)
    assert hitung_metrik(0, 0, 50, 950) == {"akurasi": 0.95, "presisi": 0.0, "recall": 0.0, "f1": 0.0}
    assert hitung_metrik(0, 0, 0, 0)["akurasi"] == 0.0


@pytest.mark.parametrize("skrip", ["solusi_level_0_1", "solusi_level_2_3", "solusi_level_4_5", "solusi_level_6_7"])
def test_skrip_solusi_berjalan(skrip):
    import subprocess
    hasil = subprocess.run([sys.executable, "-W", "ignore", str(Path(__file__).resolve().parents[1] / "latihan" / f"{skrip}.py")],
                           capture_output=True, text=True, encoding="utf-8", env={**__import__("os").environ, "PYTHONUTF8": "1"})
    assert hasil.returncode == 0, hasil.stderr[-500:]
