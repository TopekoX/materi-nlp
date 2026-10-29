"""Jaringan saraf kecil dengan NumPy untuk klasifikasi biner (Level 6).

Satu lapis tersembunyi (ReLU) dan satu keluaran sigmoid. Tujuannya mengajar: setiap langkah
maju dan mundur ditulis eksplisit sehingga dapat dibaca. Untuk pekerjaan nyata, pakai PyTorch.
"""
import numpy as np


def sigmoid(z):
    """1 / (1 + e^-z), dihitung stabil agar tidak overflow untuk |z| besar."""
    z = np.asarray(z, dtype=float)
    keluar = np.empty_like(z)
    pos = z >= 0
    keluar[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    e = np.exp(z[~pos])
    keluar[~pos] = e / (1.0 + e)
    return keluar


def relu(z):
    return np.maximum(0.0, z)


def loss_bce(p, y, eps=1e-12):
    """Binary cross-entropy rata-rata: -mean(y log p + (1-y) log(1-p))."""
    p = np.clip(p, eps, 1 - eps)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


class MLPBiner:
    """Jaringan: x -> Linear(W1,b1) -> ReLU -> Linear(W2,b2) -> sigmoid -> p(Emergency)."""

    def __init__(self, n_masuk, n_tersembunyi=16, l2=0.0, seed=42):
        rng = np.random.default_rng(seed)
        # Inisialisasi He: skala sqrt(2 / n_masuk) menjaga besar sinyal tetap wajar setelah ReLU.
        self.W1 = rng.normal(0.0, np.sqrt(2.0 / n_masuk), size=(n_masuk, n_tersembunyi))
        self.b1 = np.zeros(n_tersembunyi)
        self.W2 = rng.normal(0.0, np.sqrt(2.0 / n_tersembunyi), size=(n_tersembunyi, 1))
        self.b2 = np.zeros(1)
        self.l2 = l2

    def parameter(self):
        return {"W1": self.W1, "b1": self.b1, "W2": self.W2, "b2": self.b2}

    def maju(self, X):
        """Propagasi maju. Mengembalikan (p, cache); cache menyimpan nilai antara untuk langkah mundur."""
        z1 = X @ self.W1 + self.b1
        a1 = relu(z1)
        z2 = a1 @ self.W2 + self.b2
        p = sigmoid(z2).ravel()
        return p, (X, z1, a1)

    def loss(self, p, y):
        """BCE ditambah penalti L2 (hanya pada bobot W, bukan bias): l2/2 * jumlah(W^2)."""
        penalti = 0.5 * self.l2 * (np.sum(self.W1 ** 2) + np.sum(self.W2 ** 2))
        return loss_bce(p, y) + float(penalti)

    def mundur(self, p, y, cache):
        """Propagasi mundur (aturan rantai). Mengembalikan kamus gradien dengan kunci sama seperti parameter()."""
        X, z1, a1 = cache
        n = len(y)
        dz2 = (p - y).reshape(-1, 1) / n          # turunan BCE+sigmoid terhadap z2
        dW2 = a1.T @ dz2 + self.l2 * self.W2
        db2 = dz2.sum(axis=0)
        da1 = dz2 @ self.W2.T
        dz1 = da1 * (z1 > 0)                       # turunan ReLU: 1 bila z1 > 0, selain itu 0
        dW1 = X.T @ dz1 + self.l2 * self.W1
        db1 = dz1.sum(axis=0)
        return {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}

    def latih(self, X, y, epoch=100, lr=0.05, optimizer="adam", ukuran_batch=64, X_val=None, y_val=None,
              sabar=None, seed=42):
        """Melatih dengan mini-batch. Mengembalikan riwayat: {'loss_latih': [...], 'loss_val': [...], 'epoch_terbaik': int}.

        sabar: jika diisi (mis. 5) dan data validasi ada, berhenti bila loss validasi tidak membaik selama `sabar`
               epoch, lalu mengembalikan bobot dari epoch terbaik (early stopping).
        """
        rng = np.random.default_rng(seed)
        n = len(y)
        m = {k: np.zeros_like(v) for k, v in self.parameter().items()}
        v = {k: np.zeros_like(x) for k, x in self.parameter().items()}
        langkah = 0
        riwayat = {"loss_latih": [], "loss_val": [], "epoch_terbaik": 0}
        terbaik, salinan, tunggu = np.inf, None, 0
        for e in range(epoch):
            urutan = rng.permutation(n)
            for awal in range(0, n, ukuran_batch):
                idx = urutan[awal:awal + ukuran_batch]
                p, cache = self.maju(X[idx])
                grad = self.mundur(p, y[idx], cache)
                langkah += 1
                for k, param in self.parameter().items():
                    if optimizer == "sgd":
                        param -= lr * grad[k]
                    else:  # Adam (Kingma & Ba, 2015)
                        m[k] = 0.9 * m[k] + 0.1 * grad[k]
                        v[k] = 0.999 * v[k] + 0.001 * grad[k] ** 2
                        m_topi = m[k] / (1 - 0.9 ** langkah)
                        v_topi = v[k] / (1 - 0.999 ** langkah)
                        param -= lr * m_topi / (np.sqrt(v_topi) + 1e-8)
            riwayat["loss_latih"].append(self.loss(self.maju(X)[0], y))
            if X_val is not None:
                lv = self.loss(self.maju(X_val)[0], y_val)
                riwayat["loss_val"].append(lv)
                if lv < terbaik - 1e-6:
                    terbaik, tunggu = lv, 0
                    riwayat["epoch_terbaik"] = e
                    salinan = {k: x.copy() for k, x in self.parameter().items()}
                else:
                    tunggu += 1
                    if sabar is not None and tunggu >= sabar:
                        break
        if sabar is not None and salinan is not None:
            for k, x in self.parameter().items():
                x[...] = salinan[k]
        return riwayat

    def proba(self, X):
        return self.maju(X)[0]

    def prediksi(self, X, ambang=0.5):
        return (self.proba(X) >= ambang).astype(int)


def periksa_gradien(model, X, y, eps=1e-5):
    """Membandingkan gradien analitik (mundur) dengan beda hingga numerik. Mengembalikan selisih relatif terbesar (norma(a - n) / (norma(a) + norma(n)), per tensor parameter).

    Selisih < 1e-6 berarti turunan di `mundur` sangat mungkin benar. Dipakai sebagai uji.
    """
    p, cache = model.maju(X)
    analitik = model.mundur(p, y, cache)
    terburuk = 0.0
    for nama, param in model.parameter().items():
        numerik = np.zeros_like(param)
        for idx in np.ndindex(param.shape):
            asli = param[idx]
            param[idx] = asli + eps
            lp = model.loss(model.maju(X)[0], y)
            param[idx] = asli - eps
            lm = model.loss(model.maju(X)[0], y)
            param[idx] = asli
            numerik[idx] = (lp - lm) / (2 * eps)
        a = analitik[nama]
        # Norma per tensor, bukan per elemen: elemen bergradien ~0 (mis. neuron ReLU mati) membuat rasio per elemen berisik.
        rel = np.linalg.norm(a - numerik) / max(1e-12, np.linalg.norm(a) + np.linalg.norm(numerik))
        terburuk = max(terburuk, float(rel))
    return terburuk
