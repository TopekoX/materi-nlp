# NLP Learning Hub

**Natural Language Processing dengan Python untuk Pemula hingga Mahir**

Materi belajar NLP berbahasa Indonesia, dibangun dengan [MkDocs](https://www.mkdocs.org/) dan [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). Pembaca dibimbing dari nol (belum mengenal NLP maupun Python) hingga mampu membangun, mengevaluasi, dan men-*deploy* aplikasi NLP.

## Studi kasus utama

Seluruh kurikulum memakai satu studi kasus: **klasifikasi teks Twitter/X berbahasa Indonesia terkait kebencanaan** menjadi dua label, `Emergency` dan `Non-Emergency`.

- Sebuah kiriman tidak otomatis `Emergency` hanya karena memuat kata bencana. Konteks, maksud, permintaan bantuan, urgensi, dan relevansi waktu ikut dipertimbangkan.
- Contoh teks di dokumentasi adalah ilustrasi sintetis, **bukan** dataset beranotasi yang tervalidasi.
- Model di materi ini adalah bahan belajar, bukan sistem yang siap dipakai untuk respons darurat sungguhan.
- Tidak ada scraping atau pengunduhan data Twitter/X otomatis.

## Kurikulum

| Level | Topik | Status |
|---|---|---|
| 0 | Orientasi NLP | Tersedia |
| 1 | Fondasi Python untuk NLP | Tersedia |
| 2 | Fondasi teks dan *preprocessing* | Tersedia |
| 3 | Analisis teks eksploratif dan representasi fitur (BoW, TF-IDF) | Tersedia |
| 4 | Machine learning untuk klasifikasi teks (Naive Bayes, Logistic Regression, Linear SVM) | Tersedia |
| 5 | Evaluasi, analisis kesalahan, dan eksperimen | Tersedia |
| 6 | Deep learning untuk NLP (embedding, neural network, RNN/LSTM/GRU, attention, Transformer, IndoBERT, fine-tuning) | Tersedia; kode NumPy diuji; kode PyTorch/Transformers (`berat/`) dieksekusi di CPU (IndoBERT 2 model × 5 seed, LSTM × 5 seed), hasil tidak diperiksa otomatis |
| 7 | Advanced NLP dan *deployment* (kalibrasi, interpretabilitas, bias, drift, FastAPI, model card) | Tersedia; API dijalankan lokal dan diuji, tanpa autentikasi |
| Proyek | Klasifikasi kebencanaan Tahap A–H (definisi, dataset, EDA, preprocessing, modeling, evaluasi, IndoBERT, API) | Tersedia |
| Latihan | Latihan Level 0–7, mini-proyek berrubrik, kuis gabungan, kunci jawaban yang diuji | Tersedia |

Status terkini dan keputusan teknis ada di [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md). Pemeriksaan yang benar-benar dijalankan dicatat di [`docs/lampiran/audit-verifikasi.md`](docs/lampiran/audit-verifikasi.md).

## Instalasi (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt        # dokumentasi (MkDocs)
pip install -r requirements-ml.txt     # contoh kode, notebook, pengujian
# Opsional dan berat, hanya untuk eksperimen di examples/level-6-deep-learning/berat/:
# pip install -r requirements-dl.txt
```

macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate`, lalu perintah `pip` yang sama.

| Berkas | Isi |
|---|---|
| `requirements.txt` | MkDocs, Material, pymdown-extensions |
| `requirements-ml.txt` | NumPy, pandas, scikit-learn, Sastrawi, pytest, JupyterLab, FastAPI, dll. |
| `requirements-dl.txt` | PyTorch dan Transformers (opsional, unduhan besar) |

## Menjalankan kode, tes, dan API

Semua perintah dari folder `examples/`:

```powershell
cd examples
python -m pytest -q                                          # seluruh tes (Level 2-7); tidak butuh PyTorch
python check_page_outputs.py ../docs/level-6-deep-learning   # blok "Output nyata" harus cocok dengan eksekusi skrip
python level-6-deep-learning/cek_lingkungan_dl.py            # apakah torch/transformers/CUDA tersedia
python level-7-deployment/01_arsitektur_pipeline.py          # membuat artefak model untuk API
python -m uvicorn nlp_hub.api:buat_app --factory --port 8000 # API; dokumentasi di http://127.0.0.1:8000/docs
```

- **Ringan vs berat.** Skrip `examples/level-6-deep-learning/01_*.py`-`06_*.py` dan seluruh Level 7 hanya butuh `requirements-ml.txt`. Skrip PyTorch/Transformers ada di `examples/level-6-deep-learning/berat/`, tidak dijalankan oleh `mkdocs build`, `pytest`, maupun pemeriksa keluaran. Lihat `berat/README.md`.
- **Dokumentasi penggunaan API:** `examples/level-7-deployment/README.md` (endpoint, variabel lingkungan, pengujian).
- API adalah demonstrasi pendidikan pada data sintetis: tanpa autentikasi, tidak untuk akses publik atau penggunaan operasional.

## Menjalankan dokumentasi

```powershell
mkdocs serve              # http://127.0.0.1:8000 dengan live reload
mkdocs build --strict     # build ke site/; gagal bila ada tautan rusak atau peringatan
```

Material 9.7 menampilkan pemberitahuan "MkDocs 2.0" di setiap build. Itu pengumuman dari pengembang Material, bukan peringatan proyek, dan tidak menggagalkan `--strict`. `requirements.txt` membatasi `mkdocs<2`.

## Struktur repository

```
mkdocs.yml                      identitas situs, theme, navigasi, ekstensi
SPEC_NLP_LEARNING_HUB.md        spesifikasi utama (kurikulum, proyek, urutan tahap)
CLAUDE.md                       aturan kerja: pedagogi, penjelasan kode, integritas data
docs/                           semua konten yang dipublikasikan
  index.md, panduan-belajar.md, glosarium.md, referensi.md
  level-0-orientasi/ ... level-7-advanced-nlp/
  proyek-klasifikasi-bencana/   proyek utama (Tahap A-H)
  latihan/                      latihan dan kuis
  lampiran/                     audit verifikasi
  authoring/                    panduan kontributor (komponen, kode, matematika)
  IMPLEMENTATION_PLAN.md        status tahap implementasi
  curriculum/, getting-started/, examples/   sisa halaman template, tidak tampil di navigasi
examples/                       kode contoh (.py, notebook), disertakan lewat snippets
  nlp_hub/                      paket kode bersama (preprocessing, fitur, model, evaluasi)
  disaster-classification/      dataset SINTETIS, pembangkit data, DATA_CARD.md
  level-N-.../                  skrip tiap halaman dan notebook yang sudah dieksekusi
  tests/                        unit test (python -m pytest dari folder examples/)
  check_page_outputs.py         memeriksa blok "Output nyata" terhadap keluaran skrip
  build_notebooks.py            membangun dan menjalankan notebook
```

## Menjalankan contoh kode, tes, dan notebook

```powershell
cd examples
python -m pytest                                   # unit test
python check_page_outputs.py ../docs/level-5-evaluasi   # blok keluaran halaman = keluaran skrip
python build_notebooks.py 2 3 4 5                  # bangun ulang notebook (opsional)
```

Dataset di `examples/disaster-classification/` **sintetis**: teks dibangkitkan dari templat dan ditulis tangan, label
mengikuti definisi operasional di materi, bukan hasil anotasi manusia. Baca `DATA_CARD.md` sebelum menafsirkan skor.
Folder `examples/**/artefak/` (model tersimpan) tidak ikut git.

## Menulis atau menambah materi

1. Baca `CLAUDE.md` dan `SPEC_NLP_LEARNING_HUB.md` terlebih dahulu.
2. Buat `docs/<level>/<nama>.md` dengan satu judul `# ...`, lalu daftarkan di `nav:` pada `mkdocs.yml`.
3. Kode contoh disimpan di `examples/` dan disertakan dengan `--8<-- "level-1-python/contoh.py"` (path relatif terhadap `examples/`).
4. Setiap halaman materi mengikuti struktur di bagian 5 `CLAUDE.md`: tujuan, prasyarat, penjelasan bertahap, kode per potongan, latihan dengan kunci jawaban, kuis, ringkasan, glosarium, dan referensi.
5. Jalankan `mkdocs build --strict` sebelum commit, dan catat hasil pemeriksaan di `docs/lampiran/audit-verifikasi.md`.

Referensi komponen (admonition, tab, tabel, kode, matematika, Mermaid) ada di `docs/authoring/`.

- **Matematika:** MathJax 3.2.2 dimuat dari `cdn.jsdelivr.net`, jadi rumus butuh koneksi internet.
- **Diagram:** Mermaid 11.17.2 di-*vendor* di `docs/assets/vendor/mermaid/`, tidak butuh jaringan.

## Deploy ke GitHub Pages

1. Pastikan `site_url` dan `repo_url` di `mkdocs.yml` menunjuk ke repository ini. Saat ini `site_url` bernilai `https://topekox.github.io/materi-nlp/`; pastikan sesuai dengan nama repository dan akun GitHub Anda.
2. Jalankan `mkdocs gh-deploy --strict` (build lalu push ke branch `gh-pages`).
3. Di GitHub: **Settings → Pages → Deploy from a branch → `gh-pages` / root**.

Belum ada deployment yang dilakukan dari repository ini.

## Ketergantungan jaringan saat dibuka di browser

| Dependensi | Kapan | Catatan |
|---|---|---|
| `cdn.jsdelivr.net` (MathJax 3.2.2) | setiap halaman | diperlukan untuk rumus |
| `api.github.com` | setiap halaman, bila `repo_url` diisi | Material menampilkan info repository di header |
| Google Fonts | tidak pernah | `theme.font: false` memakai font sistem |
| Mermaid | tidak pernah | sudah di-*vendor* |

## Asal template

Situs ini dibangun di atas template MkDocs + Material yang dapat dipakai ulang. Dokumen template asli tetap disimpan: `PRD.md`, `TECHNICAL_DESIGN.md`, `VALIDATION_REPORT.md`, dan `PROMPT_MKDOCS_TEMPLATE.md`.

## Lisensi

Dirilis di bawah [MIT License](LICENSE). Pustaka Mermaid yang di-*vendor* di `docs/assets/vendor/mermaid/` juga berlisensi MIT dan menyertakan berkas `LICENSE` sendiri.
