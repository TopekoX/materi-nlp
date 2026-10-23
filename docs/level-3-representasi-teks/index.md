# Level 3: Exploratory Text Analysis dan Representasi Fitur

Level ini mengajarkan cara memahami korpus dan mengubah teks menjadi angka:
statistik korpus, n-gram, Bag of Words, TF-IDF, matriks sparse, fitur buatan tangan,
dan representasi dengan scikit-learn. Dataset yang sama dengan Level 2 (sintetis).

**Estimasi waktu:** 18–24 jam, termasuk latihan dan notebook.
**Prasyarat:** [Level 2](../level-2-fondasi-teks/index.md).

!!! warning "Data sintetis"
    Angka berasal dari eksekusi nyata pada dataset sintetis dan set tulis-tangan
    (lihat `examples/disaster-classification/DATA_CARD.md`). Angka itu hanya menunjukkan
    bahwa kode bekerja dan memperlihatkan konsep (mis. pergeseran kosakata); bukan performa pada data nyata.

## Daftar materi

| # | Materi | Topik spesifikasi |
|---|---|---|
| 1 | [Statistik Korpus, Panjang Teks, Frekuensi Kata, Vocabulary](statistik-korpus.md) | 1, 2, 3, 4 |
| 2 | [Word n-gram dan Character n-gram](n-gram.md) | 5 |
| 3 | [Bag of Words](bag-of-words.md) | 6 |
| 4 | [TF-IDF dan Intuisi Matematisnya](tfidf.md) | 7 |
| 5 | [Sparse Matrix dan One-hot Encoding](sparse-matrix-one-hot.md) | 8, 9 |
| 6 | [Feature Engineering Teks Kebencanaan](feature-engineering-kebencanaan.md) | 10 |
| 7 | [Representasi dengan scikit-learn, Perbandingan Fitur, Vocabulary Leakage](representasi-sklearn.md) | 11, 12, 13 |
| 8 | [Latihan: Analisis Dataset](latihan-analisis-dataset.md) | 14 |

## Capaian

- [ ] Menjalankan EDA lengkap: struktur, duplikat, label, panjang, frekuensi kata.
- [ ] Menghitung TF-IDF dengan tangan dan mencocokkannya dengan scikit-learn.
- [ ] Menjelaskan mengapa matriks teks disimpan sebagai sparse.
- [ ] Merancang dan menguji fitur buatan tangan yang terkait dengan definisi label.
- [ ] Membandingkan representasi dengan protokol yang sama dan membaca hasilnya dengan jujur.

## Kode dan notebook

| Berkas | Isi |
|---|---|
| `examples/level-3-feature-engineering/01_*.py` – `08_*.py` | Skrip tiap halaman |
| `examples/level-3-feature-engineering/gambar_level3.py` | Pembuat gambar halaman Statistik Korpus |
| `examples/level-3-feature-engineering/03_eda_dan_fitur.ipynb` | Notebook EDA (sudah dieksekusi) |
| `examples/nlp_hub/features.py`, `eksperimen.py` | Fitur buatan tangan dan protokol evaluasi bersama |
| `examples/tests/` | Unit test |

## Checkpoint praktis

Sebelum lanjut ke Level 4, pastikan Anda dapat:

1. Menghitung TF-IDF tiga dokumen dengan kalkulator dan mencocokkannya dengan `TfidfVectorizer`.
2. Menjelaskan mengapa `fit` vektorizer hanya boleh pada data latih.
3. Menjelaskan mengapa pembagian per kejadian tidak cukup pada dataset ini (59 dari 61 templat uji ada di latih).
4. Menjelaskan mengapa BoW biner terbaik pada validasi silang tetapi terburuk pada set tulis-tangan.

## Materi selanjutnya

Mulai dengan [Statistik Dasar Korpus](statistik-korpus.md). Setelah Level 3, lanjut ke
[Level 4: Machine Learning](../level-4-machine-learning/index.md).
