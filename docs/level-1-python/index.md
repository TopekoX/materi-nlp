# Level 1: Fondasi Python untuk NLP

Level ini mengajarkan bagian Python yang paling sering dipakai dalam
pemrosesan teks, semuanya dengan contoh laporan kebencanaan. Jika Anda sudah
mahir Python, kerjakan latihan di setiap halaman sebagai pemeriksaan cepat.

**Estimasi waktu:** 15–25 jam.

## Daftar materi

| # | Materi | Skrip contoh |
|---|---|---|
| 1 | [Variabel dan tipe data](variabel-tipe-data.md) | `01_variabel_tipe_data.py` |
| 2 | [String dan operasi teks](string-operasi-teks.md) | `02_string_operasi_teks.py` |
| 3 | [Indexing dan slicing](indexing-slicing.md) | `03_indexing_slicing.py` |
| 4 | [List, tuple, set, dictionary](list-tuple-set-dict.md) | `04_koleksi.py` |
| 5 | [Kondisional](kondisional.md) | `05_kondisional.py` |
| 6 | [Perulangan](perulangan.md) | `06_perulangan.py` |
| 7 | [Function dan parameter](function-parameter.md) | `07_function_parameter.py` |
| 8 | [Import dan modul](import-modul.md) | `08_import_modul.py` |
| 9 | [Exception handling](exception-handling.md) | `09_exception_handling.py` |
| 10 | [File teks](file-teks.md) | `10_file_teks.py` |
| 11 | [CSV dan JSON](csv-json.md) | `11_csv_json.py` |
| 12 | [Dasar NumPy](numpy-dasar.md) | `12_numpy_dasar.py` |
| 13 | [Dasar pandas](pandas-dasar.md) | `13_pandas_dasar.py` |
| 14 | [Missing values dan duplikasi](missing-values-duplikasi.md) | `14_missing_duplikasi.py` |
| 15 | [Dasar regex](regex-dasar.md) | `15_regex_dasar.py` |
| 16 | [Debugging dan pengujian](debugging-pengujian.md) | `16_debugging_pengujian.py` |

## Cara menjalankan contoh

Dari akar repository, dengan `.venv` aktif:

```bash
python -X utf8 examples/level-1-python/01_variabel_tipe_data.py
```

Halaman 12–14 membutuhkan `numpy` dan `pandas` (`pip install -r requirements-ml.txt`).
Dataset kecil sintetis ada di `examples/level-1-python/data/laporan_contoh.csv`.

!!! info "Status pengujian"
    Seluruh keluaran yang ditampilkan di level ini berasal dari eksekusi nyata
    skrip pada mesin penulis. Lihat [Audit dan Verifikasi](../lampiran/audit-verifikasi.md).

## Materi selanjutnya

Mulai dari [Variabel dan Tipe Data](variabel-tipe-data.md). Setelah Level 1, lanjut ke [Level 2](../level-2-fondasi-teks/index.md).
