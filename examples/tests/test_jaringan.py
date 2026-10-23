"""Uji jaringan saraf NumPy (Level 6)."""
import numpy as np
import pytest

from nlp_hub.jaringan import MLPBiner, loss_bce, periksa_gradien, relu, sigmoid

XOR_X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
XOR_Y = np.array([0, 1, 1, 0])


def test_sigmoid_stabil_untuk_nilai_ekstrem():
    s = sigmoid(np.array([-1000.0, 0.0, 1000.0]))
    assert np.allclose(s, [0.0, 0.5, 1.0]) and np.isfinite(s).all()


def test_relu():
    assert relu(np.array([-2.0, 0.0, 3.0])).tolist() == [0.0, 0.0, 3.0]


def test_loss_bce_nilai_yang_diketahui():
    assert loss_bce(np.array([0.5]), np.array([1])) == pytest.approx(np.log(2))
    assert np.isfinite(loss_bce(np.array([0.0]), np.array([1])))      # dipotong, tidak menjadi inf


def test_bentuk_maju():
    m = MLPBiner(5, 3)
    p, (X, z1, a1) = m.maju(np.zeros((7, 5)))
    assert p.shape == (7,) and z1.shape == a1.shape == (7, 3)


@pytest.mark.parametrize("l2", [0.0, 0.05])
def test_gradien_analitik_cocok_dengan_numerik(l2):
    rng = np.random.default_rng(0)
    m = MLPBiner(5, 4, l2=l2, seed=1)
    assert periksa_gradien(m, rng.normal(size=(6, 5)), np.array([0, 1, 0, 1, 1, 0])) < 1e-6


def test_xor_dipelajari_mlp():
    m = MLPBiner(2, 8, seed=3)
    r = m.latih(XOR_X, XOR_Y, epoch=500, lr=0.05, ukuran_batch=4)
    assert (m.prediksi(XOR_X) == XOR_Y).all()
    assert r["loss_latih"][-1] < r["loss_latih"][0]


def test_pelatihan_deterministik_dengan_seed():
    def jalan():
        m = MLPBiner(2, 4, seed=5)
        m.latih(XOR_X, XOR_Y, epoch=20, lr=0.05, ukuran_batch=2, seed=9)
        return m.proba(XOR_X)
    assert np.allclose(jalan(), jalan())


def test_early_stopping_memulihkan_bobot_terbaik():
    rng = np.random.default_rng(0)
    X, y = rng.normal(size=(60, 6)), rng.integers(0, 2, 60)          # label acak -> overfit pasti
    m = MLPBiner(6, 32, seed=0)
    r = m.latih(X[:40], y[:40], epoch=200, lr=0.05, X_val=X[40:], y_val=y[40:], sabar=5)
    assert len(r["loss_val"]) < 200
    assert m.loss(m.proba(X[40:]), y[40:]) == pytest.approx(min(r["loss_val"]), abs=1e-9)


def test_l2_memperkecil_bobot():
    rng = np.random.default_rng(1)
    X, y = rng.normal(size=(50, 6)), rng.integers(0, 2, 50)
    norma = []
    for l2 in (0.0, 0.5):
        m = MLPBiner(6, 16, l2=l2, seed=0)
        m.latih(X, y, epoch=80, lr=0.02)
        norma.append(np.linalg.norm(m.W1))
    assert norma[1] < norma[0]
