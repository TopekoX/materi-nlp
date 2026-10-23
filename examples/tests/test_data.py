"""Uji dataset sintetis dan pembagian data."""
import pandas as pd
import pytest

from nlp_hub.data import (
    bagi_latih_uji, kodekan_label, muat_dataset, muat_uji_tangan,
)


def test_skema_dan_label_valid():
    df = muat_dataset(hapus_duplikat=False)
    assert {"source_id", "event_id", "post_type", "template_id", "text", "label"} <= set(df.columns)
    assert set(df["label"]) == {"Emergency", "Non-Emergency"}
    assert df["text"].notna().all() and (df["text"].str.strip() != "").all()
    assert df["source_id"].is_unique


def test_duplikat_disengaja_dan_dapat_dibuang():
    mentah = muat_dataset(hapus_duplikat=False)
    bersih = muat_dataset()
    assert mentah["text"].duplicated().sum() == 10
    assert bersih["text"].is_unique
    assert len(bersih) == len(mentah) - 10


def test_label_konsisten_dengan_jenis_postingan():
    df = muat_dataset(hapus_duplikat=False)
    emergency = {"laporan", "bantuan"}
    assert (df["post_type"].isin(emergency) == (df["label"] == "Emergency")).all()


def test_uji_tangan_seimbang_dan_tidak_beririsan_dengan_latih():
    uji = muat_uji_tangan()
    assert len(uji) == 48
    assert uji["label"].value_counts().to_dict() == {"Emergency": 24, "Non-Emergency": 24}
    assert set(uji["text"]).isdisjoint(set(muat_dataset()["text"]))


def test_kodekan_label():
    hasil = kodekan_label(pd.Series(["Emergency", "Non-Emergency", "Emergency"]))
    assert hasil.tolist() == [1, 0, 1]


def test_kodekan_label_menolak_label_asing():
    with pytest.raises(ValueError, match="Label tidak dikenal"):
        kodekan_label(pd.Series(["Emergency", "Darurat"]))


def test_pembagian_tidak_membocorkan_kejadian():
    latih, uji = bagi_latih_uji(muat_dataset())
    assert set(latih["event_id"]).isdisjoint(set(uji["event_id"]))
    assert len(latih) + len(uji) == len(muat_dataset())


def test_pembagian_deterministik_dan_kedua_kelas_ada():
    a = bagi_latih_uji(muat_dataset())
    b = bagi_latih_uji(muat_dataset())
    assert a[1]["source_id"].tolist() == b[1]["source_id"].tolist()
    for bagian in a:
        assert set(bagian["label"]) == {"Emergency", "Non-Emergency"}
