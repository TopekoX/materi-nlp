"""Uji perturbasi deterministik."""
import pytest

from nlp_hub import perturbasi as pt


def test_huruf_besar():
    assert pt.huruf_besar("Tolong banjir") == "TOLONG BANJIR"


def test_singkat_mengganti_kata_dikenal_dan_menjaga_lainnya():
    assert pt.singkat("Tolong, rumah sudah tidak aman") == "tlg, rmh udh gak aman"


def test_perpanjang_huruf_setiap_kata_ketiga_panjang():
    # kata panjang >= 4: tolong(1) banjir(2) cepat(3) -> hanya kata ketiga diperpanjang
    # vokal terakhir ditambah dua salinan (a -> aaa) agar tertangkap aturan huruf berulang >= 3
    assert pt.perpanjang_huruf("tolong banjir cepat") == "tolong banjir cepaaat"


def test_perpanjang_huruf_tidak_menyentuh_kata_pendek():
    assert pt.perpanjang_huruf("air naik di rt") == "air naik di rt"


def test_typo_menukar_dua_huruf_tengah_pada_kata_keempat():
    assert pt.typo("banjir besar sekali sungai meluap") == "banjir besar sekali sugnai meluap"


def test_tambah_derau_menambah_tiga_unsur():
    hasil = pt.tambah_derau("banjir")
    assert hasil.startswith("banjir") and "🙏" in hasil and "#SiagaBencana" in hasil and "https://" in hasil


def test_tanpa_tanda_baca():
    assert pt.tanpa_tanda_baca("Tolong!!! Air naik, cepat.") == "Tolong Air naik cepat"


@pytest.mark.parametrize("nama", list(pt.PERTURBASI))
def test_semua_perturbasi_deterministik_dan_mengembalikan_str(nama):
    f = pt.PERTURBASI[nama]
    teks = "Tolong, air sudah masuk rumah kami di Jl. Melati RT 04!"
    assert f(teks) == f(teks) and isinstance(f(teks), str)
