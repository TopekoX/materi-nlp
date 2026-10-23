# Level 7: Advanced NLP dan Deployment

Membawa model ke aplikasi yang dapat diuji, dipantau, dan didokumentasikan, dengan batas klaim yang jelas.

**Estimasi waktu:** 26–34 jam, termasuk latihan.
**Prasyarat:** [Level 5](../level-5-evaluasi/index.md); [Level 6](../level-6-deep-learning/index.md) membantu tetapi tidak wajib (kode Level 7 tidak memerlukan PyTorch).

!!! danger "Bukan sistem penentu keadaan darurat"
    Model dan layanan di level ini adalah **demonstrasi pendidikan pada dataset sintetis**. Jangan menganggapnya sebagai sistem penentuan keadaan darurat yang otomatis penuh atau pengganti verifikasi manusia. Output model adalah **skor keputusan SVM**, bukan probabilitas; ambang 0 adalah batas bawaan yang **belum divalidasi**. Lihat [Keamanan, Model Card, dan Keterbatasan](keamanan-model-card-roadmap.md).

## Daftar materi

| # | Materi | Topik spesifikasi | Kode |
|---|---|---|---|
| 1 | [Arsitektur Pipeline, Optimasi, Versioning, Penyimpanan Model](arsitektur-pipeline.md) | 1, 2, 7, 8 | `01_arsitektur_pipeline.py` |
| 2 | [Kalibrasi dan Pemilihan Threshold](kalibrasi-threshold.md) | 3 | `02_kalibrasi_threshold.py` |
| 3 | [Interpretabilitas (Explainable NLP)](interpretabilitas.md) | 4 | `03_interpretabilitas.py` |
| 4 | [Bias, Fairness, Robustness, OOD](bias-robustness-ood.md) | 5, 6 | `04_bias_robustness_ood.py` |
| 5 | [Pemantauan Performa dan Data Drift](pemantauan-drift.md) | 14 | `05_pemantauan_drift.py` |
| 6 | [FastAPI: Prediksi, Validasi, Logging, Error, Deployment Lokal](fastapi-dasar.md) | 9, 10, 11, 16 | `nlp_hub/api.py`, `06_api_demo.py` |
| 7 | [Batch, Riwayat, Dasbor, Pengujian Otomatis](fastapi-batch-riwayat-tes.md) | 12, 13, 15 | `nlp_hub/riwayat.py`, `tests/test_api.py` |
| 8 | [Keamanan, Model Card, Keterbatasan, Roadmap](keamanan-model-card-roadmap.md) | 17, 18, 19, 20 | `07_model_card.py` |

Semua 20 topik wajib spesifikasi tercakup. Dokumentasi penggunaan (instal, menjalankan API, variabel lingkungan, pengujian) ada di `examples/level-7-deployment/README.md`.

## Capaian

- [ ] Menjelaskan lapisan pipeline inferensi dan menyimpan/memuat artefak bermetadata dengan pemeriksaan checksum.
- [ ] Membedakan skor dan probabilitas, mengkalibrasi, dan menjelaskan batas pemilihan ambang.
- [ ] Menjelaskan prediksi dengan kontribusi/oklusi dan mengenali shortcut.
- [ ] Melakukan uji kontrafaktual, perturbasi, dan probe OOD serta menyatakan batas klaimnya.
- [ ] Memantau drift dengan PSI dan menetapkan ambang dari simulasi derau.
- [ ] Membangun dan menguji API FastAPI dengan validasi, penanganan error, batch, dan riwayat tanpa teks mentah.
- [ ] Menyusun model card dan daftar periksa sebelum model dipakai di luar pembelajaran.

## Temuan utama (dari eksekusi nyata, dataset sintetis)

| Temuan | Halaman |
|---|---|
| Berkas model yang diubah satu byte ditolak oleh pemeriksaan checksum; batch 448 teks sekitar 19× lebih cepat pada mesin penulis | [Arsitektur](arsitektur-pipeline.md) |
| ECE: validasi 0,043, uji sintetis 0,052, tulis-tangan 0,186; ambang dari validasi (target recall 0,95) memberi recall tulis-tangan **0,083** | [Kalibrasi](kalibrasi-threshold.md) |
| Fitur teratas: `rt`, `rumah`, `jalan`, `di` (shortcut dari templat); kontribusi menjumlah tepat ke skor | [Interpretabilitas](interpretabilitas.md) |
| Ganti nama tempat: 5/140 label berbalik (dikenal), 4/70 (baru); 6/6 probe OOD benar (sampel sangat kecil) | [Bias dan OOD](bias-robustness-ood.md) |
| PSI derau pada 48 teks: median 0,185, p95 0,792; drift besar tetap terdeteksi (tulis-tangan 5,42) | [Drift](pemantauan-drift.md) |
| 422 untuk masukan buruk, 500 tanpa jejak tumpukan; 20 tes API, 198 tes total lolos | [FastAPI](fastapi-dasar.md), [Batch dan Tes](fastapi-batch-riwayat-tes.md) |
| Model card dihasilkan dari kode; penggunaan yang tidak sesuai dinyatakan eksplisit | [Keamanan dan Model Card](keamanan-model-card-roadmap.md) |

## Kode, dependensi, dan tes

| Berkas | Isi |
|---|---|
| `examples/level-7-deployment/01_*.py` – `07_*.py` | Skrip pelajaran |
| `examples/level-7-deployment/README.md` | Cara instal, menjalankan API, variabel lingkungan, pengujian |
| `examples/nlp_hub/layanan.py`, `api.py`, `riwayat.py` | Inti layanan, aplikasi FastAPI, riwayat SQLite |
| `examples/nlp_hub/kalibrasi.py`, `interpretasi.py`, `pantau.py` | Kalibrasi/ambang, penjelasan, PSI |
| `examples/tests/test_layanan.py`, `test_api.py` | Tes unit dan API |
| `requirements-ml.txt` | Seluruh dependensi Level 7 (FastAPI, uvicorn, httpx, pytest); tidak butuh PyTorch |

Menjalankan semua tes dari folder `examples/`: `python -m pytest -q`.

## Checkpoint praktis

Sebelum menyebut proyek ini "selesai", pastikan Anda dapat:

1. Menjelaskan mengapa API mengembalikan `skor` dan bukan `probabilitas`.
2. Menunjukkan di kode tempat checksum diperiksa dan menyebut apa yang tidak dilindunginya.
3. Menjelaskan mengapa ambang yang dipilih di validasi gagal pada tulis-tangan.
4. Menjelaskan mengapa PSI > 0,1 pada 117 vs 112 teks tidak membuktikan drift.
5. Menjelaskan mengapa respons 500 hanya memuat `id_galat`.
6. Menyebut tiga syarat sebelum model boleh dipakai di luar pembelajaran.

## Materi selanjutnya

Mulai dengan [Arsitektur Pipeline](arsitektur-pipeline.md). Setelah Level 7, lanjut ke [Proyek Klasifikasi Bencana](../proyek-klasifikasi-bencana/index.md).
