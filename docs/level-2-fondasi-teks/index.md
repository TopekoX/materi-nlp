# Level 2: Fondasi Teks dan Preprocessing

Level ini mengajarkan cara komputer memandang teks dan cara membangun
pipeline preprocessing yang dapat diuji. Kita memakai satu dataset sintetis
(klasifikasi Emergency / Non-Emergency) dan satu paket kode bersama, `nlp_hub`.

**Estimasi waktu:** 18–25 jam, termasuk latihan dan notebook.
**Prasyarat:** [Level 1: Python](../level-1-python/index.md) (terutama string, regex, pandas).

!!! warning "Data sintetis"
    Seluruh data di Level 2–5 sintetis (templat dan tulis-tangan). Baca berkas
    `examples/disaster-classification/DATA_CARD.md` di repository: isinya skema, cara label
    ditetapkan, keterbatasan, dan penggunaan yang tidak sesuai. Angka yang tampil berasal
    dari eksekusi nyata, tetapi tidak mewakili performa pada data Twitter/X nyata.

## Daftar materi

| # | Materi | Topik spesifikasi yang dicakup |
|---|---|---|
| 1 | [Karakter, Unicode, dan UTF-8](karakter-unicode-encoding.md) | 1, 2 |
| 2 | [Token, Kalimat, dan Tokenisasi](token-kalimat-tokenisasi.md) | 3, 4, 5 |
| 3 | [Case Folding, Tanda Baca, URL/Mention/Hashtag](case-folding-pembersihan.md) | 6, 7, 13 |
| 4 | [Emoji dan Emotikon](emoji-emotikon.md) | 8 |
| 5 | [Normalisasi Informal, Huruf Berulang, Typo](normalisasi-informal.md) | 9, 15, 16 |
| 6 | [Stopwords](stopwords.md) | 10 |
| 7 | [Stemming dan Lemmatization](stemming-lemmatization.md) | 11, 12 |
| 8 | [Negasi](negasi.md) | 14 |
| 9 | [Angka, Waktu, Lokasi](angka-waktu-lokasi.md) | 17 |
| 10 | [Perbandingan Pipeline](perbandingan-pipeline.md) | 18 (eksperimen) |
| 11 | [Data Leakage akibat Preprocessing](leakage-preprocessing.md) | 19 |
| 12 | [Pipeline yang Dapat Diuji](pipeline-teruji.md) | 20 |

## Capaian

- [ ] Menjelaskan perbedaan karakter, code point, dan byte.
- [ ] Menjalankan langkah preprocessing dan menjelaskan keputusan di balik tiap langkah.
- [ ] Menunjukkan, dengan contoh, bahwa preprocessing tertentu dapat merusak makna (negasi, stopword, stemming).
- [ ] Membandingkan konfigurasi preprocessing dengan eksperimen yang adil dan membaca hasilnya dengan jujur.
- [ ] Menulis unit test untuk fungsi preprocessing.

## Kode dan notebook

| Berkas | Isi |
|---|---|
| `examples/nlp_hub/` | Paket kode bersama (kamus, preprocessing, pemuatan data) |
| `examples/level-2-preprocessing/01_*.py` – `12_*.py` | Skrip tiap halaman |
| `examples/level-2-preprocessing/02_preprocessing_pipeline.ipynb` | Notebook ringkas (sudah dieksekusi; dibangun oleh `examples/build_notebooks.py`) |
| `examples/tests/` | Unit test (`python -m pytest` dari folder `examples/`) |
| `examples/disaster-classification/` | Dataset sintetis dan Kartu Data |

Menjalankan skrip dari folder utama repository:

```bash
python examples/level-2-preprocessing/05_normalisasi_informal.py
```

Di Windows, jika emoji menyebabkan `UnicodeEncodeError`, tambahkan `-X utf8`.

## Checkpoint praktis

Sebelum lanjut ke Level 3, pastikan Anda dapat:

1. Menjalankan `python -m pytest` dari folder `examples/` dan melihat seluruh tes lolos.
2. Menjelaskan, tanpa melihat catatan, mengapa stopword bawaan Sastrawi berbahaya untuk tugas ini.
3. Menjelaskan perbedaan preprocessing tanpa state dan yang mempelajari statistik data.
4. Menunjukkan pada tabel *Perbandingan Pipeline* mengapa tidak ada konfigurasi yang dapat disebut terbaik.

## Materi selanjutnya

Mulai dengan [Karakter, Unicode, dan UTF-8](karakter-unicode-encoding.md). Setelah Level 2, lanjut ke
[Level 3: Representasi Teks](../level-3-representasi-teks/index.md).
