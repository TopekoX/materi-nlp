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

### Keputusan teknis tambahan (Tahap 6)

18. **Pemisahan ringan vs berat.** Mekanisme deep learning ditulis dengan NumPy (`nlp_hub/embedding.py`, `jaringan.py`, `atensi.py`, `subword.py`) dan berjalan di CPU dalam hitungan detik; skrip PyTorch/Transformers ada di `examples/level-6-deep-learning/berat/`. `mkdocs build` hanya menyalin teks skrip (snippets) dan tidak menjalankan apa pun. pytest tidak mengumpulkan `berat/` (hanya tes kompilasi sintaks); `check_page_outputs.py` melewati `berat/` dan `nlp_hub/` (diubah, didokumentasikan di docstring).
19. **Skrip berat belum dieksekusi.** `torch` dan `transformers` tidak terpasang di mesin penulis dan tidak dipasang (unduhan besar, di luar lingkup izin). Halaman yang memuatnya berlabel "belum dieksekusi" dan tidak berisi angka hasil. Hanya sintaks yang diperiksa.
20. **Embedding = PPMI + SVD**, bukan Word2Vec/GloVe/FastText asli; dinyatakan di halaman. `vektor_subword` hanya mengilustrasikan ide subword.
21. **Level 7 memakai Linear SVM Level 5.** Keluaran API adalah `skor` (bukan probabilitas); ambang 0 ditandai `ambang_tervalidasi: false`; respons selalu memuat `catatan` dan `versi_model`. Kalibrasi Platt didemonstrasikan di halaman, tidak diterapkan ke API.
22. **Privasi bawaan.** Log dan riwayat hanya memuat sidik jari SHA-256 12 karakter, panjang, skor, dan label; teks disimpan hanya bila `NLP_HUB_SIMPAN_TEKS=1`.
23. **Artefak** (`examples/level-7-deployment/artefak/`, `examples/**/berat/artefak/`) diabaikan git; `pastikan_artefak` membuatnya bila tidak ada. Checksum hanya mencakup `model.joblib`, bukan `model.json` (didokumentasikan).
24. **Aplikasi FastAPI sebagai factory** (`nlp_hub.api:buat_app`) agar dapat diuji dengan `TestClient`. Tidak ada autentikasi, pembatasan laju, atau Dockerfile.
25. `examples/pytest.ini` menyaring peringatan deprecation Starlette untuk `TestClient` + httpx (dari library).

### Keputusan teknis tambahan (Tahap 6b–7)

26. **Eksperimen berat dijalankan di CPU** setelah `pip install -r requirements-dl.txt` (torch 2.14.1+cpu, transformers 5.20.2, Python 3.14.7, Windows, CUDA tidak tersedia). Skrip `berat/` tidak berubah dari draf awal dan berjalan tanpa perbaikan.
27. **`berat/13_ulang_seed.py`** menjalankan beberapa seed dan menulis ringkasan ke `berat/hasil/*.md|json` (disertakan di repository karena kecil; bobot model di `berat/artefak/` diabaikan git). Pembanding Linear SVM dilatih pada **data latih yang sama** (335 teks) dengan model neural, bukan data pengembangan (452).
28. **Keluaran heavy ditandai terpisah:** judul blok "Output nyata: dieksekusi penulis, bergantung versi dan unduhan (tidak diperiksa otomatis)"; `check_page_outputs.py` hanya memeriksa blok berjudul persis "Output nyata". Blok waktu berjudul "Output nyata: waktu berubah-ubah".
29. **`check_page_outputs.py`** kini mendukung blok di dalam admonition (menjorok) dan melewati modul `nlp_hub/` serta `berat/`.
30. **Respons API menambah `waktu_ms`** (syarat Tahap H spesifikasi); diukur hanya untuk pemanggilan model.
31. **Proyek:** skrip di `examples/disaster-classification/proyek/` (`tahap_a` … `tahap_h`), modul baru `nlp_hub/anotasi.py` dan `validasi_data.py`, notebook EDA `tahap_c_eda.ipynb` (dibangun `build_notebooks.py 7`). Aturan anotasi menjadi fungsi dari tiga jawaban ya/tidak.
32. **Latihan:** kunci jawaban kode di `examples/latihan/solusi_*.py`, diuji `tests/test_latihan.py`; halaman `docs/latihan/` per kelompok level + proyek/kuis gabungan.
33. **Verifikasi referensi:** metadata (judul, penulis pertama, tahun) dicocokkan lewat API arXiv, Crossref, dan ACL Anthology; teks makalah tidak dibaca; venue tidak diverifikasi terpisah. Satu URL (uvicorn.org) gagal DNS dan diganti uvicorn.dev.

## Tahapan

| Tahap | Isi | Status |
|---|---|---|
| 1 | Audit dan rencana | Selesai |
| 2 | Kerangka kurikulum, landing page, navigasi, glosarium | Selesai |
| 3 | Level 0 dan Level 1 + contoh Python | Selesai |
| 3b | Revisi Level 0 dan Level 1 sesuai `CLAUDE.md` (kerangka lengkap, kode berpotongan, latihan berkunci, glosarium) | Selesai (lihat catatan di bawah) |
| 4 | Level 2 (12 halaman) + paket `nlp_hub` + dataset sintetis + unit test + notebook preprocessing | Selesai (lihat catatan di bawah) |
| 5 | Level 3 (8 halaman), Level 4 (10), Level 5 (8) + baseline klasifikasi + notebook + tabel perbandingan dari kode | Selesai (lihat catatan di bawah) |
| 6 | Level 6 (8 halaman) dan Level 7 (8 halaman) + kode ringan/berat terpisah + API FastAPI + tes | Selesai; eksperimen berat kemudian dieksekusi (lihat catatan Tahap 6b) |
| 6b | Pemasangan `requirements-dl.txt`, eksekusi eksperimen berat (IndoBERT 2 model × 5 seed, LSTM × 5 seed, tokenizer) dan hasil ke halaman | Selesai (lihat catatan Tahap 6b) |
| 7 | Proyek utama (indeks + Tahap A–H), latihan Level 0–7 + proyek + kuis gabungan, verifikasi referensi, dokumentasi | Selesai dengan batasan (lihat catatan Tahap 7) |
| 8 | Build, tautan, tes kode, audit akhir (termasuk audit browser) | Selesai dengan batasan (lihat catatan Tahap 8) |

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

## Catatan Tahap 6 (diselesaikan 2026-10-23)

Cakupan: 25 topik Level 6 dan 20 topik Level 7 sesuai spesifikasi (lihat tabel di indeks masing-masing level). Level 6: 8 halaman + indeks; Level 7: 8 halaman + indeks; 6 skrip ringan Level 6, 7 skrip Level 7, 3 skrip berat, 1 utilitas lingkungan; 10 modul baru di `nlp_hub/`; 6 berkas tes baru. `glosarium.md` (78 istilah baru) dan `referensi.md` (bagian Level 6-7 dengan status verifikasi per entri) diperbarui.

Temuan yang dituliskan jujur di halaman (batas kesimpulan, bukan kegagalan):

- Embedding PPMI+SVD dari 564 teks bertemplat: tetangga banyak yang tidak bermakna (mis. `tolong` ↔ `akun`, `follow`).
- MLP NumPy pada TF-IDF: recall Emergency tulis-tangan 0,792-0,833 (3 seed) vs SVM 0,583, tetapi 48 teks, satu pelabel, tiga seed: **bukan klaim keunggulan**.
- Kalibrasi Platt baik pada validasi/uji sintetis (ECE 0,043 / 0,052) tetapi 0,186 pada tulis-tangan; ambang dari validasi (target recall 0,95) memberi recall tulis-tangan 0,083.
- Fitur teratas model: `rt`, `rumah`, `jalan`, `di` (shortcut templat); `rt` ada di ~63% teks Emergency vs ~2% Non-Emergency.
- PSI antara sampel acak 48 teks dan acuannya sendiri: median 0,185, p95 0,792; ambang konvensi 0,1 terlalu sensitif pada sampel kecil.
- Uji perturbasi register tidak menemukan penurunan pada uji sintetis karena data terlalu mudah, bukan bukti robust.

Bug nyata yang ditemukan saat menulis: ukuran relatif per elemen pada gradient check berisik (diganti norma per tensor, dijaga tes); `PackageNotFoundError` karena nama paket pip berbeda dari nama impor (`scikit-learn` vs `sklearn`); dua klaim awal di draf halaman interpretabilitas (kata `meledak`/`longsor` dikira tidak ada di kosakata) ternyata salah dan dikoreksi setelah diperiksa; satu jawaban latihan (ambang di `model.json`) diperbaiki setelah dicoba.

Keterbatasan yang diketahui: skrip PyTorch/Transformers belum dieksekusi; model IndoBERT tidak diunduh; perkiraan waktu dan memori fine-tuning adalah orde besaran, bukan pengukuran; API tidak diuji beban dan tidak punya autentikasi; kuis dan latihan belum diuji pada pembaca pemula; rumus LaTeX dan diagram Mermaid (termasuk `sequenceDiagram`) belum dilihat di browser; sebagian besar referensi akademik Level 6-7 belum diperiksa daring; tidak ada tinjauan penutur asli; tidak ada tinjauan keamanan independen.

## Catatan Tahap 6b (diselesaikan 2026-10-23)

`requirements-dl.txt` dipasang di `.venv` (CPU). Dieksekusi: `cek_lingkungan_dl.py`, `11_tokenizer_indobert.py`, uji asap `12_finetune_indobert.py --subset 64 --epochs 1` (sekitar 21 detik latih), lalu `13_ulang_seed.py` untuk `indobenchmark/indobert-base-p1` (seed 1–5), `indolem/indobert-base-uncased` (seed 1–5), dan LSTM PyTorch (seed 1–5).

| Model (data latih 335 teks) | Tulis-tangan: recall E (rata-rata, min–maks) | Presisi E | Uji sintetis F1 makro |
|---|---|---|---|
| Linear SVM | 0,583 | 1,000 | 0,980 |
| IndoBERT p1 | 0,825 (0,708–0,917) | 1,000 | 0,986 (0,980–1,000) |
| IndoLEM | 0,442 (0,375–0,542) | 0,879 | 0,915 |
| LSTM dari nol | 0,192 (0,000–0,333) | 0,778 | 0,974 |

Temuan: nama "IndoBERT" tidak menjamin hasil (IndoLEM di bawah SVM); LSTM dari nol baik pada uji sintetis tetapi runtuh pada tulis-tangan; p1 melampaui SVM pada recall tulis-tangan di kelima seed tanpa FP. Semua dibatasi: 24 Emergency, satu pelabel, data bertemplat, lima seed, tanpa penalaan hiperparameter. Waktu: 111–217 detik per seed IndoBERT (sebagian seed dengan proses lain berjalan bersamaan).

Halaman Level 6 (tokenizer, RNN, fine-tuning, indeks, komputasi) dan Level 7 (roadmap) diperbarui dari "belum dieksekusi" menjadi hasil nyata dengan label "tidak diperiksa otomatis".

## Catatan Tahap 7 (diselesaikan 2026-10-23)

Cakupan: `docs/proyek-klasifikasi-bencana/` (indeks + Tahap A–H, 8 halaman), `docs/latihan/` (indeks + 5 halaman), glosarium (+15 istilah), referensi (status verifikasi per entri), README, dan tes baru (`test_proyek_tahap.py`, `test_latihan.py`, tes `waktu_ms`).

Temuan yang dituliskan (batas kesimpulan): label proyek ditentukan oleh jenis templat (tabel silang `post_type` × label sempurna); panjang teks Emergency lebih besar (96,7 vs 81,1 karakter); 59 dari 61 templat uji ada di latih; strategi preprocessing tidak dibedakan oleh validasi silang (0,995–0,998), stopword konservatif menurunkan recall tulis-tangan 4 pesan; peringkat baseline berbalik antara validasi silang dan tulis-tangan; baseline kata kunci hanya 0,354 akurasi pada tulis-tangan; pembagian acak per baris memberi F1 makro 1,000 vs 0,980 per kejadian.

Bug nyata yang ditemukan saat menulis: (1) penanda keluaran satu baris (`@@OUT nama 5@@`) tidak diganti oleh pembuat halaman sehingga **lima blok keluaran di halaman Level 7 sempat berisi penanda mentah** padahal pemeriksa melaporkan 22 blok diperiksa dan 0 tidak cocok; ditemukan saat menulis halaman latihan, diperbaiki, dan hitungan yang benar adalah 27 blok; (2) pemeriksa keluaran tidak mengenali blok yang menjorok di dalam admonition; (3) URL `uvicorn.org` gagal DNS; (4) heuristik mention menandai bagian setelah `@` pada alamat email; (5) dua klaim draf (penyebab peringatan `num_labels`; FN karena kata asing) diperiksa dan dikoreksi.

Keterbatasan: label dan data tetap sintetis tanpa pelabel independen; tulis-tangan 48 teks; lima seed; tidak ada penalaan; kuis/latihan belum diuji pada pembaca pemula; rumus LaTeX dan diagram Mermaid belum dilihat di browser; API tanpa autentikasi dan tidak diuji beban; teks lengkap makalah tidak dibaca.

## Catatan Tahap 8 (diselesaikan 2026-10-23)

Audit akhir: 198 tes lolos; 218 blok "Output nyata" cocok dengan eksekusi; build strict lolos; audit browser (Edge, 119 halaman, desktop dan ponsel) merender 795 rumus dan 107 diagram tanpa galat; audit statis dan 121 URL diperiksa. Skrip audit disimpan di `examples/audit/` agar dapat diulang (`audit_browser.py` memerlukan `pip install playwright` dan Edge; `audit_statis.py` hanya memerlukan jaringan).

Perbaikan yang berasal dari audit: diagram Mermaid lebar tidak lagi diperkecil (ukuran asli, gulir horizontal); rumus inline panjang tidak lagi melebarkan halaman ponsel; rumus mentah di daftar isi; satu URL mati di Level 0; halaman Lampiran yang masih berstatus "sedang disusun". Keputusan: dua perubahan kecil pada aset template (`mermaid-config.js`, `extra.css`) dilakukan karena memperbaiki kerusakan nyata dan didokumentasikan di sini; tema dan struktur tidak diubah.

Keterbatasan akhir ada di [Audit dan Verifikasi](lampiran/audit-verifikasi.md) (bagian "Belum diperiksa setelah Tahap 8"): hanya Chromium; tanpa uji aksesibilitas, bahasa, dan keterbacaan; teks makalah tidak dibaca; API tidak aman untuk akses publik; hanya Python 3.14.7/Windows; GPU dan deployment tidak diuji.

## Langkah berikutnya

Seluruh tahap 1–8 selesai dalam lingkup yang tertulis. Pekerjaan lanjutan (bukan bagian tahap ini):

1. **Data dan pelabelan:** data nyata yang sah, pelabel independen (kappa), evaluasi lintas waktu.
2. **Eksperimen:** penalaan hiperparameter SVM dan IndoBERT di validasi, ≥10 seed, selang bootstrap pada selisih, GPU, dan penyelidikan mengapa IndoLEM jauh di bawah IndoBERT p1.
3. **Kualitas materi:** uji keterbacaan dengan pembaca pemula, tinjauan penutur asli, uji aksesibilitas, pembacaan teks makalah yang dikutip, dan uji pada Python/OS lain.
4. **Layanan dan publikasi:** autentikasi, HTTPS, pembatasan laju, uji beban; `mkdocs gh-deploy --strict` setelah `site_url` dipastikan benar.

## Catatan verifikasi

Pemeriksaan yang berhasil, gagal, atau belum dilakukan dicatat di bagian
*Log verifikasi* pada [Audit akhir](lampiran/audit-verifikasi.md) setelah halaman tersebut dibuat.
