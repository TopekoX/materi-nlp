"""Uji pembagian tiga arah dan pembangun model."""
import pytest

from nlp_hub.data import bagi_latih_val_uji, kodekan_label, muat_dataset, muat_uji_tangan
from nlp_hub.modeling import ALGORITMA, buat_pipeline


def test_pembagian_tiga_arah_tidak_beririsan_dan_lengkap():
    df = muat_dataset()
    latih, val, uji = bagi_latih_val_uji(df)
    e = [set(x["event_id"]) for x in (latih, val, uji)]
    assert e[0].isdisjoint(e[1]) and e[0].isdisjoint(e[2]) and e[1].isdisjoint(e[2])
    assert len(latih) + len(val) + len(uji) == len(df)
    assert 0.5 < len(latih) / len(df) < 0.7
    for bagian in (latih, val, uji):
        assert set(bagian["label"]) == {"Emergency", "Non-Emergency"}


def test_pembagian_tiga_arah_deterministik():
    a = bagi_latih_val_uji(muat_dataset())
    b = bagi_latih_val_uji(muat_dataset())
    assert [x["source_id"].tolist() for x in a] == [x["source_id"].tolist() for x in b]


@pytest.mark.parametrize("nama", ALGORITMA)
def test_pipeline_dapat_dilatih_dan_memprediksi(nama):
    df, uji = muat_dataset(), muat_uji_tangan()
    model = buat_pipeline(nama).fit(df["text"], kodekan_label(df["label"]))
    pred = model.predict(uji["text"])
    assert len(pred) == len(uji) and set(pred) <= {0, 1}


def test_algoritma_tidak_dikenal():
    with pytest.raises(ValueError, match="tidak dikenal"):
        buat_pipeline("xgboost")


def test_param_model_menimpa_bawaan():
    assert buat_pipeline("svm", C=0.25).named_steps["model"].C == 0.25
    assert buat_pipeline("nb", alpha=0.1).named_steps["model"].alpha == 0.1


def test_pipeline_baru_tiap_dipanggil():
    assert buat_pipeline("lr") is not buat_pipeline("lr")
