"""Uji penyiapan data standar."""
from nlp_hub.proyek import model_rujukan, siapkan


def test_siapkan_konsisten():
    d = siapkan()
    assert len(d.dev) == len(d.latih) + len(d.val) == len(d.y_dev)
    assert len(d.uji) == len(d.y_uji) and len(d.tangan) == len(d.y_tangan) == 48
    assert set(d.dev["event_id"]).isdisjoint(set(d.uji["event_id"]))


def test_model_rujukan_dapat_memprediksi():
    d = siapkan()
    m = model_rujukan(d)
    assert set(m.predict(d.tangan["text"])) <= {0, 1}
    assert hasattr(m, "decision_function")
