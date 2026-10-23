"""Kalibrasi probabilitas dan pemilihan ambang pada data validasi (Level 7)."""
import numpy as np


def tabel_reliabilitas(y, p, n_bin=5):
    """Daftar (batas_bawah, batas_atas, n, rata_prediksi, frekuensi_nyata) untuk bin berisi minimal satu contoh."""
    y, p = np.asarray(y, dtype=float), np.asarray(p, dtype=float)
    batas = np.linspace(0, 1, n_bin + 1)
    # np.digitize dengan batas dalam; p == 1.0 masuk bin terakhir
    nomor = np.clip(np.digitize(p, batas[1:-1]), 0, n_bin - 1)
    baris = []
    for b in range(n_bin):
        m = nomor == b
        if m.any():
            baris.append((float(batas[b]), float(batas[b + 1]), int(m.sum()), float(p[m].mean()), float(y[m].mean())))
    return baris


def ece(y, p, n_bin=10):
    """Expected Calibration Error: rata-rata tertimbang |frekuensi nyata - rata-rata prediksi| per bin. 0 = terkalibrasi sempurna."""
    total = len(y)
    return float(sum(n / total * abs(nyata - pred) for _, _, n, pred, nyata in tabel_reliabilitas(y, p, n_bin)))


def skor_brier(y, p):
    """Rata-rata kuadrat selisih antara probabilitas dan label (0/1); makin kecil makin baik."""
    return float(np.mean((np.asarray(p, dtype=float) - np.asarray(y, dtype=float)) ** 2))


def pilih_ambang_target_recall(y, skor, target_recall):
    """Ambang TERTINGGI pada data (y, skor) yang masih mencapai recall >= target. Mengembalikan (ambang, presisi, recall).

    Hanya boleh dipakai pada data VALIDASI. Memakainya pada data uji adalah kebocoran seleksi. Bila tidak ada
    contoh positif, atau target tak tercapai, ValueError.
    """
    y, skor = np.asarray(y).astype(int), np.asarray(skor, dtype=float)
    if y.sum() == 0:
        raise ValueError("tidak ada contoh positif; recall tidak terdefinisi")
    terbaik = None
    for ambang in sorted(set(skor), reverse=True):
        pred = skor >= ambang
        tp = int((pred & (y == 1)).sum())
        recall = tp / y.sum()
        if recall >= target_recall:
            terbaik = (float(ambang), tp / max(1, int(pred.sum())), float(recall))
            break
    if terbaik is None:
        raise ValueError(f"recall {target_recall} tidak tercapai pada ambang mana pun")
    return terbaik
