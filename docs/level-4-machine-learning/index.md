# Level 4: Machine Learning untuk Klasifikasi Teks

Level ini membangun baseline klasifikasi Emergency / Non-Emergency dengan TF-IDF dan
tiga algoritma klasik: Multinomial Naive Bayes, Logistic Regression, dan Linear SVM. Kita
membandingkannya dengan eksperimen yang adil, mencari hyperparameter dengan validasi silang
berkelompok, menyimpan model, dan memprediksi teks baru.

**Estimasi waktu:** 24–32 jam, termasuk latihan dan notebook.
**Prasyarat:** [Level 3](../level-3-representasi-teks/index.md).

!!! warning "Data sintetis, bukan bukti kelayakan"
    Semua skor berasal dari eksekusi nyata pada dataset **sintetis** dan set tulis-tangan
    (`examples/disaster-classification/DATA_CARD.md`). Skor tinggi pada data bertemplat tidak
    membuktikan model berfungsi pada data Twitter/X nyata, dan **tidak boleh** dipakai untuk menyatakan model
    layak untuk tanggap darurat.

## Daftar materi

| # | Materi | Topik spesifikasi |
|---|---|---|
| 1 | [Supervised Learning, X, y, Label Encoding](supervised-learning-xy.md) | 1, 2, 3 |
| 2 | [Pembagian Data: Latih/Validasi/Uji, Stratified, Seed](pembagian-data.md) | 4, 5, 14 |
| 3 | [Pipeline scikit-learn](pipeline-sklearn.md) | 6 |
| 4 | [Multinomial Naive Bayes](naive-bayes.md) | 7 |
| 5 | [Logistic Regression](logistic-regression.md) | 8 |
| 6 | [Linear SVM](linear-svm.md) | 9 |
| 7 | [Perbandingan Algoritma dan Eksperimen yang Adil](perbandingan-model.md) | 10, 18 |
| 8 | [Hyperparameter, Tuning, GridSearchCV, Cross-validation](tuning-cross-validation.md) | 11, 12, 13 |
| 9 | [Menyimpan Model dan Memprediksi Teks Baru](serialisasi-prediksi.md) | 15, 16 |
| 10 | [Kesalahan Umum dalam Training](kesalahan-umum-training.md) | 17 |

## Capaian

- [ ] Menentukan `X`, `y`, dan pengodean label tanpa menukar kelas positif.
- [ ] Membagi data per kejadian dan menjelaskan fungsi latih, validasi, dan uji.
- [ ] Menghitung Naive Bayes dan prediksi Logistic Regression dengan tangan dan mencocokkannya dengan scikit-learn.
- [ ] Membedakan probabilitas Logistic Regression dari skor keputusan SVM.
- [ ] Membandingkan algoritma dengan baseline dan menyebut batas kesimpulan dari tabelnya.
- [ ] Memakai `GridSearchCV` dengan pipeline dan kelompok, dan menjelaskan mengapa skor terbaik optimistis.

## Kode dan notebook

| Berkas | Isi |
|---|---|
| `examples/level-4-classification/01_*.py` – `10_*.py` | Skrip tiap halaman |
| `examples/level-4-classification/04_baseline_klasifikasi.ipynb` | Notebook baseline (sudah dieksekusi) |
| `examples/nlp_hub/modeling.py`, `data.py`, `eksperimen.py` | Pembangun model, pembagian data, protokol evaluasi |
| `examples/level-4-classification/hasil/*.csv` | Tabel hasil dari eksekusi nyata |
| `examples/tests/test_modeling.py`, `test_eksperimen.py` | Unit test |

## Hasil ringkas (dari eksekusi nyata)

Rincian lengkap dan cara membacanya ada di [Perbandingan Algoritma](perbandingan-model.md).
F1 makro, dataset sintetis:

| Model | Validasi silang (452 teks) | Uji sintetis (112) | Tulis-tangan (48) |
|---|---|---|---|
| Baseline selalu Non-Emergency | 0,398 | 0,398 | 0,333 |
| Multinomial NB | 0,983 | 0,970 | 0,916 |
| Logistic Regression | 0,975 | 0,980 | 0,681 |
| Linear SVM | 0,995 | 0,980 | 0,806 |

Peringkat berubah antar-kolom, sehingga tidak ada model yang dapat disebut terbaik
secara mutlak. Recall Emergency pada tulis-tangan: NB 0,833; SVM 0,625; LR 0,417.

## Checkpoint praktis

Sebelum lanjut ke Level 5, pastikan Anda dapat:

1. Menjelaskan mengapa `LabelEncoder` dapat menukar kelas positif dan bagaimana mencegahnya.
2. Menghitung $P(\text{tolong} \mid \text{Emergency})$ dengan smoothing Laplace pada contoh kecil.
3. Menjelaskan mengapa `LinearSVC` tidak memiliki `predict_proba`.
4. Menjelaskan mengapa `best_score_` dari `GridSearchCV` tidak boleh dilaporkan sebagai performa akhir.

## Materi selanjutnya

Mulai dengan [Supervised Learning, X, dan y](supervised-learning-xy.md). Setelah Level 4, lanjut ke
[Level 5: Evaluasi](../level-5-evaluasi/index.md).
