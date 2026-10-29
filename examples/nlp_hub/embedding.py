"""Embedding kata dari hitungan ko-kemunculan (Level 6), hanya dengan NumPy.

Ini BUKAN Word2Vec, GloVe, atau FastText asli. Metode di sini (PPMI + SVD) adalah
cara berbasis hitungan yang sangat dekat secara konsep dan cukup kecil untuk dibaca
dan dijalankan di CPU dalam sekejap. Fungsi `vektor_subword` hanya mengilustrasikan
IDE di balik FastText (kata = jumlah potongan karakter), bukan melatih FastText.
"""
import numpy as np


def bangun_kosakata(daftar_token, min_hitung=2):
    """Daftar kata yang muncul minimal `min_hitung` kali, urut dari yang tersering (seri: abjad)."""
    hitung = {}
    for token in daftar_token:
        for t in token:
            hitung[t] = hitung.get(t, 0) + 1
    kata = [k for k, n in hitung.items() if n >= min_hitung]
    return sorted(kata, key=lambda k: (-hitung[k], k))


def matriks_koterjadian(daftar_token, kosakata, jendela=2):
    """Matriks C (V x V): C[i, j] = berapa kali kata j muncul dalam `jendela` kata di sekitar kata i."""
    indeks = {k: i for i, k in enumerate(kosakata)}
    C = np.zeros((len(kosakata), len(kosakata)))
    for token in daftar_token:
        ids = [indeks[t] for t in token if t in indeks]
        for posisi, i in enumerate(ids):
            for j in ids[max(0, posisi - jendela): posisi] + ids[posisi + 1: posisi + 1 + jendela]:
                C[i, j] += 1
    return C


def ppmi(C):
    """Positive Pointwise Mutual Information: max(0, log(P(i,j) / (P(i) P(j))))."""
    total = C.sum()
    p_baris = C.sum(axis=1, keepdims=True) / total
    p_kolom = C.sum(axis=0, keepdims=True) / total
    p_gabung = C / total
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log(p_gabung / (p_baris * p_kolom))
    pmi[~np.isfinite(pmi)] = 0.0
    return np.maximum(pmi, 0.0)


def embedding_svd(P, dimensi=20):
    """Memampatkan matriks PPMI menjadi `dimensi` angka per kata dengan SVD terpotong."""
    U, S, _ = np.linalg.svd(P, full_matrices=False)
    return U[:, :dimensi] * np.sqrt(S[:dimensi])


def kosinus(a, b):
    """Kemiripan kosinus dua vektor; 0.0 bila salah satunya vektor nol."""
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(a @ b / (na * nb)) if na and nb else 0.0


def tetangga_terdekat(kata, kosakata, E, k=5):
    """`k` kata dengan kosinus tertinggi terhadap `kata`. Menimbulkan KeyError bila kata di luar kosakata."""
    i = kosakata.index(kata)
    skor = [(kosinus(E[i], E[j]), kosakata[j]) for j in range(len(kosakata)) if j != i]
    return [(w, round(s, 3)) for s, w in sorted(skor, reverse=True)[:k]]


def ngram_karakter(kata, n_min=3, n_max=5):
    """Potongan karakter ala FastText dengan penanda batas kata: 'banjir' -> '<ba', 'ban', ..."""
    k = f"<{kata}>"
    return [k[i:i + n] for n in range(n_min, n_max + 1) for i in range(len(k) - n + 1)]


def vektor_subword(kata, kosakata, E, n_min=3, n_max=5, teratas=3):
    """Vektor untuk kata yang BOLEH di luar kosakata: rata-rata vektor `teratas` kata yang paling banyak berbagi potongan karakter.

    Kemiripan potongan diukur dengan Jaccard (irisan / gabungan). Mengembalikan (vektor, daftar kata yang dipakai);
    vektor nol dan daftar kosong bila tidak ada potongan yang cocok.
    """
    potongan = set(ngram_karakter(kata, n_min, n_max))
    skor = []
    for i, w in enumerate(kosakata):
        lain = set(ngram_karakter(w, n_min, n_max))
        j = len(potongan & lain) / len(potongan | lain)
        if j > 0:
            skor.append((j, i))
    skor = sorted(skor, reverse=True)[:teratas]
    if not skor:
        return np.zeros(E.shape[1]), []
    return E[[i for _, i in skor]].mean(axis=0), [kosakata[i] for _, i in skor]
