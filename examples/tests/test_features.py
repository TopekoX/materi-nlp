"""Uji fitur buatan tangan."""
import pytest

from nlp_hub.features import NAMA_FITUR, FiturTangan, fitur_tangan, tabel_fitur


def test_semua_fitur_ada_dan_berurutan():
    f = fitur_tangan("Tolong!")
    assert list(f) == NAMA_FITUR


def test_fitur_dasar():
    f = fitur_tangan("TOLONG!! @bpbd_contoh banjir 08.12 https://contoh.example/1 #Siaga 🙏")
    assert f["n_seru"] == 2
    assert f["ada_url"] == 1 and f["ada_mention"] == 1
    assert f["n_hashtag"] == 1 and f["n_emoji"] == 1
    assert f["ada_waktu"] == 1 and f["ada_angka"] == 1
    assert f["kata_permintaan"] == 1


def test_rasio_kapital_dan_teks_tanpa_huruf():
    assert fitur_tangan("ABc")["rasio_kapital"] == pytest.approx(2 / 3)
    assert fitur_tangan("123 !!!")["rasio_kapital"] == 0.0


def test_lokasi_dan_negasi_dan_waktu_kata():
    f = fitur_tangan("Tidak ada korban di Jl. Melati RT 08, kejadian kemarin")
    assert f["ada_lokasi"] == 1 and f["ada_negasi"] == 1 and f["kata_lampau"] == 1
    assert f["kata_baru_terjadi"] == 0


def test_teks_kosong_tidak_error():
    f = fitur_tangan("")
    assert f["n_karakter"] == 0 and f["n_token"] == 0 and f["rasio_kapital"] == 0.0


def test_bukan_string_ditolak():
    with pytest.raises(TypeError):
        fitur_tangan(None)


def test_transformer_bentuk_dan_tanpa_state():
    t = FiturTangan()
    a = t.fit(["x"]).transform(["Banjir naik!", "Gempa kuat"])
    b = t.fit(["data lain sama sekali"]).transform(["Banjir naik!", "Gempa kuat"])
    assert a.shape == (2, len(NAMA_FITUR))
    assert (a == b).all()


def test_tabel_fitur_kolom():
    import pandas as pd

    df = tabel_fitur(pd.Series(["a", "b"]))
    assert list(df.columns) == NAMA_FITUR and len(df) == 2
