# Rencana Implementasi

Dokumen ini mencatat kondisi awal repository, keputusan teknis, dan tahapan
implementasi *NLP Learning Hub*. Dokumen ini diperbarui di akhir setiap tahap.

## Kondisi awal (hasil audit Tahap 1)

| Aspek | Temuan |
|---|---|
| Generator | MkDocs 1.6.1 |
| Theme | `mkdocs-material` 9.7.7 (palet indigo, mode System/Light/Dark, font sistem) |
| Direktori konten | `docs/` (bukan `materi-nlp/`) |
| Direktori contoh kode | `examples/` (basis `pymdownx.snippets`, `check_paths: true`) |
| Plugin | hanya `search` |
| Ekstensi | admonition, attr_list, def_list, footnotes, md_in_html, tables, toc, arithmatex (MathJax via CDN), highlight, superfences + Mermaid, tabbed, tasklist, emoji, snippets |
| Aset kustom | `extra.css`, `mathjax.js`, `mermaid-config.js`, Mermaid 11.17.2 yang di-*vendor* |
| Git | belum ada commit; seluruh berkas berstatus *untracked* |
| Build awal | `mkdocs build --strict` lolos tanpa peringatan |
| Dependensi terpasang | MkDocs, Material, pymdown-extensions, Sastrawi. pandas, scikit-learn, pytest, FastAPI, PyTorch, dan Transformers **belum** terpasang |
| Python | 3.14 |

## Keputusan teknis

1. **Konten di `docs/`**, mengikuti konfigurasi aktual. Struktur level yang
   direkomendasikan prompt dipetakan ke `docs/level-*/`.
2. **Theme, CSS, MathJax, dan Mermaid dipertahankan.** Tidak ada plugin baru.
3. `theme.language` diubah dari `en` ke `id` agar label bawaan theme berbahasa
   Indonesia. Ini satu-satunya perubahan theme.
4. **Halaman bawaan template** (`curriculum/`, `getting-started/`, `examples/`)
   tidak dihapus. Halaman tersebut dikeluarkan dari navigasi dengan
   `not_in_nav`. Folder `authoring/` dipertahankan sebagai *Panduan Kontributor*.
5. **Kode contoh** disimpan sebagai skrip `.py` dan notebook `.ipynb` di
   `examples/`. Halaman materi menyertakan skrip lewat snippets bila perlu
   agar kode yang ditampilkan sama dengan kode yang diuji.
6. **Dependensi dipisah**: `requirements.txt` (dokumentasi),
   `requirements-ml.txt` (Python/ML/pengujian), `requirements-dl.txt`
   (PyTorch dan Transformers, opsional dan berat).
7. **Dataset**: hanya dataset sintetis ilustratif yang dibuat di repository.
   Tidak ada scraping dan tidak ada unduhan otomatis.
8. **Angka hasil eksperimen** pada halaman hanya boleh disalin dari keluaran
   eksekusi nyata, dengan versi library dan seed dicatat.

## Tahapan

| Tahap | Isi | Status |
|---|---|---|
| 1 | Audit dan rencana | Selesai |
| 2 | Kerangka kurikulum, landing page, navigasi, glosarium | Selesai |
| 3 | Level 0 dan Level 1 + contoh Python | Selesai |
| 4 | Level 2 + notebook preprocessing | Belum |
| 5 | Level 3–5 + baseline klasifikasi kebencanaan | Belum |
| 6 | Level 6–7 | Belum |
| 7 | Proyek utama, latihan, kuis, referensi, dokumentasi | Belum |
| 8 | Build, tautan, tes kode, audit akhir | Belum |

## Dokumen proyek

- `SPEC_NLP_LEARNING_HUB.md`: master specification (kurikulum Level 0-7, proyek Tahap A-H, urutan Tahap 1-8).
- `CLAUDE.md`: aturan kerja yang stabil (pedagogi, penjelasan kode, integritas data, definisi selesai).

## Utang revisi (ditemukan setelah CLAUDE.md ditambahkan)

Halaman Level 0 dan Level 1 ditulis sesuai format 15 bagian pada spesifikasi. `CLAUDE.md` bagian 4-5 lebih ketat, sehingga halaman tersebut perlu direvisi:

- Tambah **tingkat kesulitan** dan **glosarium istilah baru** per halaman.
- Pecah skrip yang lebih dari beberapa langkah menjadi potongan kode bertahap (chunk) dengan penjelasan per potongan, lalu tampilkan skrip terpadu sesudahnya.
- Perdalam penjelasan sintaks untuk pemula dan tampilkan nilai antara.
- Perluas latihan menjadi bertingkat dengan kunci jawaban dan pembahasan.
- Tambahkan rumus dengan penjelasan simbol dan contoh numerik bila relevan.

Rencana: kerjakan revisi ini sebelum Tahap 4, atau sebagai Tahap 3b. Halaman Tahap 4 dan seterusnya ditulis langsung sesuai `CLAUDE.md`.

## Catatan verifikasi

Pemeriksaan yang berhasil, gagal, atau belum dilakukan dicatat di bagian
*Log verifikasi* pada [Audit akhir](lampiran/audit-verifikasi.md) setelah halaman tersebut dibuat.
