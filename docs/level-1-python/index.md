# Level 1: Fondasi Python untuk NLP

Level ini mengajarkan bagian Python yang paling sering dipakai dalam pemrosesan teks, semuanya dengan contoh laporan
kebencanaan. Jika Anda sudah mahir Python, kerjakan latihan di setiap halaman sebagai pemeriksaan cepat.

**Estimasi waktu:** 20–28 jam, termasuk latihan.
**Prasyarat:** [Level 0](../level-0-orientasi/index.md), terutama [Persiapan Python](../level-0-orientasi/persiapan-python.md).

## Daftar materi

| # | Materi | Tingkat | Skrip contoh |
|---|---|---|---|
| 1 | [Variabel dan tipe data](variabel-tipe-data.md) | Pemula | `01_variabel_tipe_data.py` |
| 2 | [String dan operasi teks](string-operasi-teks.md) | Pemula | `02_string_operasi_teks.py` |
| 3 | [Indexing dan slicing](indexing-slicing.md) | Pemula | `03_indexing_slicing.py` |
| 4 | [List, tuple, set, dictionary](list-tuple-set-dict.md) | Pemula–menengah | `04_koleksi.py` |
| 5 | [Kondisional](kondisional.md) | Pemula | `05_kondisional.py` |
| 6 | [Perulangan](perulangan.md) | Pemula–menengah | `06_perulangan.py` |
| 7 | [Function dan parameter](function-parameter.md) | Pemula–menengah | `07_function_parameter.py` |
| 8 | [Import dan modul](import-modul.md) | Pemula | `08_import_modul.py` |
| 9 | [Exception handling](exception-handling.md) | Pemula–menengah | `09_exception_handling.py` |
| 10 | [File teks](file-teks.md) | Pemula | `10_file_teks.py` |
| 11 | [CSV dan JSON](csv-json.md) | Pemula–menengah | `11_csv_json.py` |
| 12 | [Dasar NumPy](numpy-dasar.md) | Menengah | `12_numpy_dasar.py` |
| 13 | [Dasar pandas](pandas-dasar.md) | Menengah | `13_pandas_dasar.py` |
| 14 | [Missing values dan duplikasi](missing-values-duplikasi.md) | Menengah | `14_missing_duplikasi.py` |
| 15 | [Dasar regex](regex-dasar.md) | Menengah | `15_regex_dasar.py` |
| 16 | [Debugging dan pengujian](debugging-pengujian.md) | Menengah | `16_debugging_pengujian.py` |

## Capaian

- [ ] Menulis dan menjalankan skrip Python yang memakai variabel, kondisional, perulangan, dan function.
- [ ] Memilih wadah yang tepat (list, tuple, set, dictionary) dan menghitung frekuensi kata.
- [ ] Membaca dan menulis berkas teks, CSV, dan JSON dengan encoding UTF-8.
- [ ] Memakai NumPy dan pandas untuk memeriksa dan membersihkan tabel kecil.
- [ ] Menulis pola regex sederhana dan menjelaskan jebakannya.
- [ ] Membaca traceback, menangani galat, dan menulis uji sederhana.

## Cara menjalankan contoh

Dari akar repository, dengan `.venv` aktif:

```bash
python -X utf8 examples/level-1-python/01_variabel_tipe_data.py
```

`-X utf8` menghindari `UnicodeEncodeError` pada konsol Windows lama saat mencetak emoji. Halaman 12–14 membutuhkan `numpy` dan `pandas`;
halaman 16 membutuhkan `pytest` (`pip install -r requirements-ml.txt`). Dataset kecil sintetis ada di
`examples/level-1-python/data/laporan_contoh.csv`.

!!! info "Pola halaman dan status pengujian"
    Setiap halaman memecah skrip menjadi **bagian-bagian bernama** (`--8<-- "file.py:bagian"`), dan seluruh blok "Output nyata"
    dicocokkan otomatis dengan hasil eksekusi skrip (`examples/check_page_outputs.py`). Lihat [Audit dan Verifikasi](../lampiran/audit-verifikasi.md).

## Checkpoint praktis

Sebelum lanjut ke Level 2, pastikan Anda dapat, tanpa melihat catatan:

1. Menghitung frekuensi kata dari sebuah kalimat dengan dictionary.
2. Menjelaskan mengapa `0.1 + 0.2 == 0.3` salah dan mengapa string tidak dapat diubah.
3. Membaca `laporan_contoh.csv` dengan pandas dan menghitung jumlah teks kosong dan duplikat.
4. Menulis fungsi kecil beserta dua `assert` untuk kasus normal dan kasus tepi.

## Materi selanjutnya

Mulai dari [Variabel dan Tipe Data](variabel-tipe-data.md). Setelah Level 1, lanjut ke [Level 2](../level-2-fondasi-teks/index.md).
