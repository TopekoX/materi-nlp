"""Uji komponen Tahap A-B proyek: aturan anotasi dan validasi dataset."""
import pandas as pd
import pytest

from nlp_hub.anotasi import label_menurut_aturan
from nlp_hub.data import bagi_latih_uji, muat_dataset, muat_uji_tangan
from nlp_hub.validasi_data import (
    periksa_duplikat, periksa_kebocoran_kelompok, periksa_label_bertentangan, periksa_privasi, periksa_semua, periksa_skema,
)


@pytest.mark.parametrize("a, b, c, harapan", [
    (True, True, True, "Emergency"), (True, True, False, "uncertain"), (True, False, True, "Non-Emergency"),
    (False, True, True, "Non-Emergency"), (False, False, True, "Non-Emergency"), (False, True, False, "Non-Emergency"),
])
def test_aturan_anotasi(a, b, c, harapan):
    assert label_menurut_aturan(a, b, c) == harapan


def test_kedua_dataset_proyek_lolos_skema_dan_privasi():
    for df in (muat_dataset(hapus_duplikat=False), muat_uji_tangan()):
        h = periksa_semua(df)
        assert h["skema"] == [] and h["privasi"] == [] and h["label_bertentangan"] == []


def test_dataset_mentah_punya_10_duplikat_yang_disengaja():
    assert periksa_duplikat(muat_dataset(hapus_duplikat=False)) == ["10 baris adalah duplikat persis dari baris sebelumnya"]
    assert periksa_duplikat(muat_dataset()) == []


def test_skema_menangkap_masalah():
    df = pd.DataFrame({"text": ["a", "  ", None], "label": ["Emergency", "Darurat", "Non-Emergency"]})
    m = periksa_skema(df)
    assert any("hilang" in x for x in m) and any("kosong" in x for x in m) and any("Darurat" in x for x in m)
    assert periksa_semua(pd.DataFrame({"text": ["a"]})) == {"skema": ["kolom wajib tidak ada: ['label']"]}


def test_privasi_menandai_email_telepon_url_dan_mention_tetapi_bukan_akun_contoh():
    df = pd.DataFrame({"text": ["hubungi a@b.com", "telp 081234567890", "lihat https://x.org/a", "halo @budi",
                               "ok @posko_contoh lihat https://contoh.example/1"]})
    m = " ".join(periksa_privasi(df))
    for kata in ("email", "telepon", "URL", "mention"):
        assert kata in m
    aman = pd.DataFrame({"text": ["ok @posko_contoh lihat https://contoh.example/1"]})
    assert periksa_privasi(aman) == []


def test_email_tidak_dihitung_sebagai_mention():
    assert periksa_privasi(pd.DataFrame({"text": ["a@b.com"]})) == ["1 teks tampak memuat alamat email"]


def test_label_bertentangan():
    df = pd.DataFrame({"text": ["banjir ", "banjir"], "label": ["Emergency", "Non-Emergency"]})
    assert periksa_label_bertentangan(df) == ["1 teks identik punya label berbeda"]


def test_kebocoran_kelompok_pada_pembagian_acak_tetapi_tidak_pada_pembagian_per_kejadian():
    df = muat_dataset()
    latih, uji = bagi_latih_uji(df)
    assert periksa_kebocoran_kelompok(latih, uji) == []
    acak = df.sample(frac=1, random_state=0)
    n = len(acak) * 4 // 5
    assert periksa_kebocoran_kelompok(acak.iloc[:n], acak.iloc[n:]) != []
