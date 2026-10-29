# Level 7: Deployment dan NLP lanjutan

Semua skrip di folder ini **ringan** (scikit-learn, FastAPI; tanpa PyTorch) dan dijalankan dari folder `examples/`.
Model berasal dari Level 5 (Linear SVM + TF-IDF) dan dilatih pada dataset **sintetis**. Ini demonstrasi pendidikan,
bukan sistem penentuan keadaan darurat.

## Instal

    pip install -r requirements-ml.txt        # dari akar repository; sudah memuat fastapi, uvicorn, httpx, pytest

## Skrip pelajaran

| Skrip | Isi |
|---|---|
| `01_arsitektur_pipeline.py` | Lapisan pipeline, penyimpanan artefak + checksum, biaya batch. **Membuat** `artefak/` |
| `02_kalibrasi_threshold.py` | Kalibrasi Platt, ECE, ambang dari validasi |
| `03_interpretabilitas.py` | Koefisien, kontribusi, oklusi |
| `04_bias_robustness_ood.py` | Uji kontrafaktual nama tempat, register, probe OOD |
| `05_pemantauan_drift.py` | PSI dan cakupan kosakata |
| `06_api_demo.py` | Memanggil API lewat `TestClient` |
| `07_model_card.py` | Menyusun model card dari metadata dan metrik |

`artefak/` (model, metadata, model card) dibuat oleh skrip, diabaikan git, dan bisa dihapus lalu dibuat ulang.

## Menjalankan API

Dari folder `examples/`:

    python level-7-deployment/01_arsitektur_pipeline.py          # sekali, untuk membuat artefak
    python -m uvicorn nlp_hub.api:buat_app --factory --port 8000

Buka <http://127.0.0.1:8000/docs> (dokumentasi interaktif OpenAPI) atau:

    curl -X POST http://127.0.0.1:8000/prediksi -H "Content-Type: application/json" \
         -d '{"teks": "Tolong, air banjir sudah masuk ke rumah kami."}'

| Endpoint | Fungsi |
|---|---|
| `GET /kesehatan` | Pemeriksaan hidup |
| `GET /model/info` | Metadata model (versi, checksum, ambang, status validasi) |
| `POST /prediksi` | Satu teks, maksimal 1000 karakter |
| `POST /prediksi/batch` | 1 sampai 100 teks |
| `GET /riwayat/ringkasan`, `GET /riwayat/terbaru?n=20` | Riwayat prediksi (tanpa teks asli) |
| `GET /dasbor` | Halaman HTML ringkasan riwayat |

Variabel lingkungan (semuanya opsional):

| Variabel | Arti | Bawaan |
|---|---|---|
| `NLP_HUB_ARTEFAK` | Folder berisi `model.joblib` dan `model.json` | `level-7-deployment/artefak` |
| `NLP_HUB_AMBANG` | Ambang skor; menimpa nilai di metadata | nilai metadata (0,0) |
| `NLP_HUB_DB` | Berkas SQLite riwayat | memori (hilang saat server berhenti) |
| `NLP_HUB_SIMPAN_TEKS` | `1` = simpan teks asli di riwayat | tidak menyimpan teks |

Respons memuat **skor keputusan**, bukan probabilitas. Ambang 0 adalah batas bawaan model dan belum divalidasi.

## Pengujian

    cd examples
    python -m pytest -q                      # seluruh tes (Level 2 sampai 7)
    python -m pytest tests/test_api.py -q    # hanya API

Tes API memakai `TestClient`; tidak membuka port dan tidak membutuhkan server berjalan.
