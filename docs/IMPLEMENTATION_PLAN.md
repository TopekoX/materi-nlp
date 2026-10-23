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

### Keputusan teknis tambahan (Tahap 4–5)

9. **Dataset sintetis** di `examples/disaster-classification/`: 574 baris dari templat (`generate_dataset.py`, seed 20261023; 10 duplikat
   disengaja) dan 48 teks tulis-tangan (`tulis_uji_tangan.py`). Label ditentukan dari jenis templat atau oleh satu penulis;
   tidak ada anotator independen. `DATA_CARD.md` menjelaskan skema, provenance, keterbatasan, dan penggunaan yang tidak sesuai.
10. **Kode bersama** di paket `examples/nlp_hub/` (kamus, preprocessing, fitur, model, evaluasi, perturbasi). Skrip pelajaran menambahkan
    `examples/` ke `sys.path`; pytest memakai `conftest.py`. Tidak ada dependensi baru (`requirements-ml.txt` tidak berubah).
11. **Protokol evaluasi tunggal** (`nlp_hub/eksperimen.py`, `proyek.py`): pembagian per `event_id` (`StratifiedGroupKFold`), model dibuat baru tiap lipatan,
    set tulis-tangan sebagai uji gaya-berbeda. Model rujukan Level 5 = Linear SVM, dipilih dari validasi silang Level 4 (bukan dari tulis-tangan).
12. **Potongan kode bernama**: skrip memakai penanda `# --8<-- [start:nama]` dan halaman menyertakan `file.py:nama`.
    `examples/check_page_outputs.py` memeriksa bahwa tiap blok "Output nyata" adalah potongan berurutan dari keluaran skrip.
13. **Notebook** dibangun dari `examples/build_notebooks.py` dan dieksekusi dengan nbclient, sehingga keluarannya asli.
14. **Gambar** dibuat skrip ke `docs/assets/gambar/` dengan pasangan warna oranye/biru yang lolos `validate_palette` (ΔE CVD 24,7).
15. **Model tersimpan** hanya di `examples/**/artefak/` (diabaikan git). Risiko memuat joblib dari sumber tak tepercaya didokumentasikan.
16. `examples/pytest.ini` menyaring `DeprecationWarning` dari Sastrawi 1.0.1 pada Python 3.14 (berasal dari library).
17. Tabel laporan Level 5 ditulis skrip ke `examples/level-5-evaluation/hasil/*.md` dan disertakan halaman lewat snippet.

## Tahapan

| Tahap | Isi | Status |
|---|---|---|
| 1 | Audit dan rencana | Selesai |
| 2 | Kerangka kurikulum, landing page, navigasi, glosarium | Selesai |
| 3 | Level 0 dan Level 1 + contoh Python | Selesai |
| 3b | Revisi Level 0 dan Level 1 sesuai `CLAUDE.md` (kerangka lengkap, kode berpotongan, latihan berkunci, glosarium) | Selesai (lihat catatan di bawah) |
| 4 | Level 2 (12 halaman) + paket `nlp_hub` + dataset sintetis + unit test + notebook preprocessing | Selesai (lihat catatan di bawah) |
| 5 | Level 3 (8 halaman), Level 4 (10), Level 5 (8) + baseline klasifikasi + notebook + tabel perbandingan dari kode | Selesai (lihat catatan di bawah) |
| 6 | Level 6–7 | Belum |
| 7 | Proyek utama, latihan, kuis, referensi, dokumentasi | Belum |
| 8 | Build, tautan, tes kode, audit akhir | Belum |

## Dokumen proyek

- `SPEC_NLP_LEARNING_HUB.md`: master specification (kurikulum Level 0-7, proyek Tahap A-H, urutan Tahap 1-8).
- `CLAUDE.md`: aturan kerja yang stabil (pedagogi, penjelasan kode, integritas data, definisi selesai).

## Catatan Tahap 3b (diselesaikan 2026-10-23)

Level 0 (10 halaman + indeks) dan Level 1 (16 halaman + indeks) direvisi agar sesuai `CLAUDE.md` bagian 4-5. Temuan audit M1-M7 ditangani:

- Setiap halaman memakai kerangka yang sama dengan Level 2-5: tingkat kesulitan, tujuan, prasyarat, konsep, penjelasan mendalam, alur, contoh sederhana, contoh kebencanaan, praktik kode per bagian, kesalahan umum, kelebihan dan keterbatasan, latihan bertahap, kunci jawaban, kuis, ringkasan, glosarium, referensi.
- Skrip contoh dipecah menjadi bagian bernama (`# --8<-- [start:nama]`) dan dijelaskan per bagian dengan nilai antara.
- Skrip baru di Level 0: `kata_kunci.py`, `teks_ke_angka.py`, `beban_peninjauan.py`. Skrip `klasifikasi_mini.py`, `ciri_media_sosial.py`, `istilah_dasar.py`, `kesepakatan.py`, dan `verifikasi_lingkungan.py` disusun ulang dan diperluas.
- `ciri_media_sosial.py` kini memaksa keluaran UTF-8 (M7); `csv-json.md` menampilkan escape surrogate sesuai keluaran nyata (M6).
- Istilah baru ditambahkan ke `glosarium.md` (104 istilah dari bagian glosarium tiap halaman).
- Blok keluaran bertanda "Output nyata" dicocokkan otomatis dengan eksekusi skrip oleh `examples/check_page_outputs.py`; blok bertanda "jalur dan versi berbeda tiap komputer" atau "waktu berubah-ubah" sengaja dikecualikan.

Keterbatasan: kuis dan latihan baru ditulis oleh penulis dan belum diuji pada pembaca pemula sungguhan; tidak ada tinjauan penutur asli; rumus LaTeX dan diagram Mermaid belum dilihat di browser.

## Catatan Tahap 4–5 (diselesaikan 2026-10-23)

Cakupan: Level 2–5 sesuai spesifikasi (topik 1–20 Level 2; 1–14 Level 3; 1–18 Level 4; 1–20 Level 5), dataset sintetis, paket kode, unit test, notebook, dan perbandingan model yang dihitung dari eksekusi.

Temuan penting yang sudah dituliskan jujur di halaman (bukan kegagalan, tetapi batas kesimpulan):

- Skor validasi silang sangat tinggi (F1 makro 0,97–0,99) karena data bertemplat; pembagian per kejadian tidak menutup kemiripan antar-templat (59 dari 61 templat uji ada di latih).
- Pada set tulis-tangan (48 teks), recall Emergency 0,417–0,833 dan peringkat model berbeda dari validasi silang.
- Hasil negatif dilaporkan: preprocessing tidak terbukti membantu; hipotesis "FN karena kosakata asing" tidak didukung; ambang dari validasi silang menurunkan recall tulis-tangan.
- Tidak ada klaim kelayakan operasional dan tidak ada ambang produksi.

Keterbatasan yang diketahui: tulis-tangan dilabeli satu orang yang juga menulis pembangkit data; satu seed untuk model akhir; rumus LaTeX (MathJax via CDN)
tidak dirender saat verifikasi; belum ada tinjauan penutur asli atas bahasa; belum ada pemeriksaan visual di browser selain gambar.

## Langkah berikutnya

1. **Tahap 6:** Level 6 (deep learning) dan Level 7 (advanced NLP dan deployment). Level 7 memakai model dan metadata dari Level 4 serta paket `nlp_hub`; endpoint tidak boleh menyebut skor SVM sebagai probabilitas.
2. **Tahap 7:** halaman `proyek-klasifikasi-bencana/`, `latihan/`, dan kuis gabungan; lengkapi `glosarium.md` dan `referensi.md` untuk Level 6–7.
3. **Tahap 8:** audit akhir, termasuk pemeriksaan visual di browser dan rendering rumus.

## Catatan verifikasi

Pemeriksaan yang berhasil, gagal, atau belum dilakukan dicatat di bagian
*Log verifikasi* pada [Audit akhir](lampiran/audit-verifikasi.md) setelah halaman tersebut dibuat.
