"""Uji tokenizer subword mini dan kelengkapan skrip eksperimen berat (Level 6)."""
import py_compile
from pathlib import Path

import pytest

from nlp_hub.subword import hitung_kata, latih_bpe, pecah_wordpiece, terapkan_bpe

BERAT = Path(__file__).resolve().parents[1] / "level-6-deep-learning" / "berat"


def test_bpe_menggabungkan_pasangan_tersering():
    h = hitung_kata(["aaab"] * 3 + ["ab"])
    aturan = latih_bpe(h, 1)
    assert aturan == [("a", "a")]
    assert terapkan_bpe("aaab", aturan) == ["aa", "a", "b", "</w>"]


def test_bpe_deterministik_dan_kata_asing_terpecah_jadi_huruf():
    h = hitung_kata(["banjir"] * 5 + ["banjar"] * 2)
    assert latih_bpe(h, 5) == latih_bpe(h, 5)
    assert terapkan_bpe("xyz", latih_bpe(h, 5)) == ["x", "y", "z", "</w>"]


def test_wordpiece_longest_match_dan_unk():
    kos = {"banjir", "##nya", "[UNK]"}
    assert pecah_wordpiece("banjirnya", kos) == ["banjir", "##nya"]
    assert pecah_wordpiece("gempa", kos) == ["[UNK]"]


@pytest.mark.parametrize("nama", sorted(p.name for p in BERAT.glob("*.py")))
def test_skrip_berat_dapat_dikompilasi_tanpa_torch(nama, tmp_path):
    """Hanya memeriksa sintaks. Skrip TIDAK dijalankan karena butuh torch/transformers dan unduhan model."""
    py_compile.compile(str(BERAT / nama), cfile=str(tmp_path / "x.pyc"), doraise=True)
