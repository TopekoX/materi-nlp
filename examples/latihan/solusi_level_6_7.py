"""Kunci jawaban kode untuk Latihan Level 6-7 (deep learning dan deployment)."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # folder examples/

import numpy as np

from nlp_hub.atensi import atensi_titik_skala, softmax
from nlp_hub.embedding import kosinus
from nlp_hub.jaringan import MLPBiner, periksa_gradien
from nlp_hub.konsol import pakai_utf8
from nlp_hub.pantau import psi

if __name__ == "__main__":
    pakai_utf8()
    # --8<-- [start:vektor]
    a, b = np.array([1.0, 1.0]), np.array([2.0, 0.0])
    print("kosinus:", round(kosinus(a, b), 4), "| sudut (derajat):", round(float(np.degrees(np.arccos(kosinus(a, b)))), 1))
    print("softmax(0, ln2, ln3):", np.round(softmax(np.array([0, np.log(2), np.log(3)])), 3))
    # --8<-- [end:vektor]
    # --8<-- [start:atensi]
    Q = np.array([[1.0, 0.0]])
    K = np.array([[1.0, 0.0], [0.0, 1.0]])
    V = np.array([[10.0, 0.0], [0.0, 10.0]])
    keluaran, bobot = atensi_titik_skala(Q, K, V)
    print("bobot:", np.round(bobot, 3), "| keluaran:", np.round(keluaran, 3))
    # --8<-- [end:atensi]
    # --8<-- [start:psi]
    print("PSI (0,5/0,3/0,2 -> 0,3/0,3/0,4) ≈", round(float(np.sum((np.array([.3, .3, .4]) - np.array([.5, .3, .2])) * np.log(np.array([.3, .3, .4]) / np.array([.5, .3, .2])))), 3))
    rng = np.random.default_rng(0)
    acuan = rng.normal(size=1000)
    print("PSI sampel sama distribusi:", round(psi(acuan, rng.normal(size=1000)), 3), "| geser +1 simpangan baku:", round(psi(acuan, rng.normal(loc=1.0, size=1000)), 3))
    # --8<-- [end:psi]
    # --8<-- [start:gradien]
    X = rng.normal(size=(8, 4))
    y = rng.integers(0, 2, 8)
    model = MLPBiner(4, 3, seed=1)
    print("selisih gradien:", f"{periksa_gradien(model, X, y):.1e}")
    model.parameter()["W2"][0, 0] += 0.5          # merusak satu bobot tidak mengubah ketepatan turunan
    print("setelah bobot diubah, turunan tetap benar:", periksa_gradien(model, X, y) < 1e-6)
    # --8<-- [end:gradien]
    # --8<-- [start:api]
    from fastapi.testclient import TestClient

    from nlp_hub.api import buat_app
    from nlp_hub.layanan import pastikan_artefak

    with tempfile.TemporaryDirectory() as folder:
        pastikan_artefak(folder)
        klien = TestClient(buat_app(folder_artefak=folder), raise_server_exceptions=False)
        r = klien.post("/prediksi", json={"teks": "Pemerintah mengumumkan pembangunan tanggul untuk mengurangi risiko banjir."})
        print(r.status_code, r.json()["label"], "| skor negatif:", r.json()["skor"] < 0)
        print("teks 1001 karakter ->", klien.post("/prediksi", json={"teks": "x" * 1001}).status_code)
    # --8<-- [end:api]
