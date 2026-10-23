"""Pemantauan pergeseran data (Level 7): Population Stability Index (PSI) dan ringkasan."""
import numpy as np


def psi(acuan, baru, n_bin=10, eps=1e-4):
    """Population Stability Index antara sampel acuan dan sampel baru.

    Bin ditentukan dari kuantil data ACUAN. PSI = jumlah (q_i - p_i) * ln(q_i / p_i), dengan p_i proporsi acuan
    dan q_i proporsi baru di bin ke-i. Aturan praktis yang lazim dipakai (konvensi industri, bukan hukum statistik):
    < 0,1 stabil; 0,1-0,25 bergeser sedang; > 0,25 bergeser besar.
    """
    acuan, baru = np.asarray(acuan, dtype=float), np.asarray(baru, dtype=float)
    batas = np.unique(np.quantile(acuan, np.linspace(0, 1, n_bin + 1)[1:-1]))
    p = np.bincount(np.digitize(acuan, batas), minlength=len(batas) + 1) / len(acuan)
    q = np.bincount(np.digitize(baru, batas), minlength=len(batas) + 1) / len(baru)
    p, q = np.clip(p, eps, None), np.clip(q, eps, None)
    return float(np.sum((q - p) * np.log(q / p)))


def ringkas_aliran(skor, panjang):
    """Statistik ringkas satu jendela lalu lintas: rata-rata dan simpangan skor, median panjang teks."""
    skor, panjang = np.asarray(skor, dtype=float), np.asarray(panjang, dtype=float)
    return {"n": int(len(skor)), "skor_rata": round(float(skor.mean()), 3),
            "skor_std": round(float(skor.std()), 3), "panjang_median": float(np.median(panjang))}
