# Audit dan Verifikasi

Log pemeriksaan jujur: apa yang sudah dijalankan, apa yang gagal, dan apa yang
belum dilakukan. Diperbarui setiap tahap.

## Log verifikasi

| Tanggal | Tahap | Pemeriksaan | Hasil |
|---|---|---|---|
| 2026-10-22 | 1 | `mkdocs build --strict` pada template awal | Lolos |
| 2026-10-22 | 2 | Build strict setelah kerangka | Gagal sementara: 1 tautan ke halaman Level 0 yang belum ada; diperbaiki di Tahap 3 |
| 2026-10-22 | 3 | Skrip `examples/level-0-orientasi/*.py` dijalankan; output disalin dari eksekusi | Lolos |
| 2026-10-22 | 3 | Skrip `examples/level-1-python/01-16_*.py` dijalankan (Python 3.14.7, numpy 2.5.4, pandas 3.1.0); output disalin dari eksekusi | Lolos |
| 2026-10-22 | 3 | `mkdocs build --strict` (Level 0-1) | Lolos |

## Audit Level 0 dan Level 1 terhadap CLAUDE.md (2026-10-23)

Cakupan: 10 halaman Level 0, 16 halaman Level 1, 21 skrip contoh. Python 3.14.7, numpy 2.5.4, pandas 3.1.0 (`.venv/`).

### Pemeriksaan yang dijalankan

| Pemeriksaan | Hasil |
|---|---|
| 21 skrip `examples/level-0-orientasi` dan `examples/level-1-python` dijalankan ulang | 21 berhasil (kode keluar 0). `ciri_media_sosial.py` hanya berhasil dengan `PYTHONIOENCODING=utf-8`; pada konsol Windows cp1252 gagal `UnicodeEncodeError` karena emoji |
| Setiap baris output asli dicocokkan dengan teks halaman pasangannya | Cocok, kecuali dua baris: path mesin pada `verifikasi-lingkungan.md` (sengaja disingkat `D:\...`) dan satu baris surrogate pada `csv-json.md` (lihat M5) |
| `mkdocs build --strict` | Lolos (kode keluar 0, tanpa peringatan build) |

### Temuan terhadap CLAUDE.md bagian 4-5

Kriteria diperiksa dengan pencocokan teks otomatis pada 26 halaman, lalu halaman `perulangan.md` dibaca penuh. Hasil untuk halaman lain belum dibaca satu per satu.

| # | Temuan | Aturan | Cakupan |
|---|---|---|---|
| M1 | Tidak ada "tingkat kesulitan" | 5.2 | 26 dari 26 halaman |
| M2 | Tidak ada glosarium istilah baru per halaman | 5.20 | 26 dari 26 halaman |
| M3 | Latihan mandiri (2-4 butir) tidak punya kunci jawaban dan pembahasan; hanya kuis yang punya jawaban. Pengecualian: `mini-proyek-manual.md` punya kunci pembahasan | 5.17, 11 | 25 dari 26 halaman |
| M4 | Tidak ada bagian "Cara kerja/alur", "Contoh sederhana" terpisah, dan "Kelebihan dan keterbatasan" sebagai judul | 5.8, 5.9, 5.15 | Hampir semua halaman (berdasarkan daftar judul) |
| M5 | Kode disajikan sebagai satu skrip utuh lewat snippet, lalu daftar penjelasan bernomor. Belum ada potongan bertahap, nilai antara, alasan pemilihan pendekatan, atau alternatifnya | 4.1, 4.2, 4.4, 4.5 | Semua halaman Level 1 dan sebagian Level 0 |
| M6 | `csv-json.md` menulis surrogate sebagai `🙏`, padahal output nyata `\ud83d\ude4f`. Baris terakhir skrip memakai `ensure_ascii=False` sehingga bukan contoh default, tetapi kalimat penjelasnya menyebut default | 4.4, 8 | 1 halaman |
| M7 | `ciri_media_sosial.py` gagal di konsol Windows bawaan; solusi UTF-8 hanya ada di tabel `verifikasi-lingkungan.md`, tidak di halaman `teks-media-sosial.md` | 4.6 | 1 halaman |

Temuan M1-M5 sama dengan "Utang revisi" di [Rencana Implementasi](../IMPLEMENTATION_PLAN.md); audit ini memastikan cakupannya dan menambah M6-M7.

### Kesimpulan

Pada saat audit ini, Level 0 dan Level 1 **belum memenuhi Definisi Selesai** pada CLAUDE.md bagian 14: kode benar dan terverifikasi, tetapi kedalaman pedagogi, latihan berkunci, dan glosarium belum terpenuhi. Temuan ditangani pada Tahap 3b (di bawah).

## Log verifikasi Tahap 3b (revisi Level 0–1), 2026-10-23

| Pemeriksaan | Hasil |
|---|---|
| `examples/check_page_outputs.py ../docs/level-0-orientasi` (dengan `PYTHONUTF8=1`) | 26 blok "Output nyata" diperiksa, 0 tidak cocok |
| `examples/check_page_outputs.py ../docs/level-1-python` | 94 blok diperiksa, 0 tidak cocok |
| Pemeriksaan judul bagian wajib (18 judul kunci) pada 10 halaman Level 0 dan 16 halaman Level 1 | Semua 26 halaman memiliki semua judul (pencocokan teks, bukan penilaian kualitas isi) |
| `pytest` di `examples/` | 97 lulus (tes tidak berubah oleh Tahap 3b; dijalankan ulang) |
| `mkdocs build --strict` | Lolos tanpa peringatan atau galat |
| Skrip Level 0 dijalankan ulang | `kesepakatan.py` memberi kappa 0,66; angka yang sama dengan `sklearn.metrics.cohen_kappa_score` (0,6552) dibandingkan sekali secara manual, bukan bagian tes otomatis. `cohen_kappa(["N"]*5, ["N"]*5)` menimbulkan `ZeroDivisionError` seperti yang dijelaskan pada halaman |
| Penggabungan istilah ke `glosarium.md` | 104 istilah ditambahkan dari bagian "Glosarium istilah baru"; jumlah definisi naik dari 86 ke 190+ |

Status temuan audit:

| # | Status |
|---|---|
| M1 tingkat kesulitan | Diperbaiki (info materi + kolom Tingkat di indeks) |
| M2 glosarium per halaman | Diperbaiki (bagian pada tiap halaman dan `glosarium.md`) |
| M3 latihan berkunci | Diperbaiki (latihan bertahap dan kunci pembahasan tiap halaman) |
| M4 bagian alur, contoh sederhana, kelebihan dan keterbatasan | Diperbaiki (judul tersedia di 26 halaman) |
| M5 kode berpotongan | Diperbaiki (skrip bersegmen, penjelasan per bagian, nilai antara) |
| M6 escape emoji di `csv-json.md` | Diperbaiki (menampilkan escape surrogate sesuai keluaran nyata) |
| M7 emoji di konsol Windows | Diperbaiki (skrip memanggil `sys.stdout.reconfigure`; halaman menjelaskan galatnya dan `python -X utf8`) |

Insiden proses: saat memperbarui `IMPLEMENTATION_PLAN.md`, sebuah skrip yang gagal mengosongkan berkas itu (dibuka untuk menulis sebelum galat). Isi dipulihkan dari transkrip sesi (keluaran `cat` awal dan skrip pengubah Tahap 4–5) dan dibandingkan dengan bagian yang sudah terlihat; commit di git hanya memuat versi awal (sebelum Tahap 4–5), sehingga tidak ada pembanding git untuk versi terakhir. Mohon periksa sekilas berkas itu.

## Log verifikasi Tahap 4–5 (Level 2–5), 2026-10-23

| Pemeriksaan | Hasil |
|---|---|
| `python -m pytest` (folder `examples/`, Python 3.14.7, scikit-learn 1.9.1) | **97 lolos**, 0 gagal, tanpa peringatan (peringatan Sastrawi disaring di `pytest.ini`) |
| `check_page_outputs.py` untuk Level 2, 3, 4, 5 | Blok "Output nyata" diperiksa: 54, 34, 44, 27; **0 tidak cocok** (blok harus potongan berurutan dari keluaran skrip) |
| `mkdocs build --strict` | Lolos setelah Level 2, 3, 4, dan 5 ditambahkan (build terakhir sebelum perubahan README/glosarium/referensi; lolos pula setelah perubahan itu pada build berikutnya) |
| Notebook `02`, `03`, `04`, `05` dibangun dan dieksekusi (nbclient) | Masing-masing berhasil saat dibangun; angkanya dibandingkan dengan halaman. Pembangunan ulang serentak untuk validasi akhir **dihentikan sistem karena memori** dan tidak diulang |
| 57 URL pada halaman Level 2–5 dan `referensi.md` dimuat dengan HTTP | Semua status 200 (halaman saja; fragmen `#...` tidak diperiksa) |
| Detail bibliografi 15 makalah dicocokkan lewat pencarian daring | Dicocokkan (penulis, judul, venue, tahun, DOI). Teks lengkap hanya dibaca untuk Pang dkk. (2002). Entri lain di `referensi.md` tanpa tanda "(diperiksa)" belum diperiksa |
| Tabel Markdown (jumlah kolom), keseimbangan `$`, karakter kontrol | Tidak ada masalah |
| Pemeriksa blok keluaran juga mendeteksi kesalahan penulisan sendiri | Beberapa kali selama penulisan (spasi tabel, teks terpotong); semuanya diperbaiki sebelum angka di atas |

### Bug nyata yang ditemukan dan diperbaiki saat menulis (dijaga tes)

- Regex emoji melewatkan `🆘` (blok U+1F100–1F1FF).
- Pola angka memotong `Rp50.000` menjadi `Rp50. tok_angka`; pola waktu salah membaca `1.50 m` (kelemahan terdokumentasi).
- Regex huruf berulang dengan `\w` merusak angka (`1000000` → `10`).
- Pemetaan `bgt`→`banget`→`sangat` berantai dan `kita`→`kami` yang keliru di kamus.

### Temuan substantif yang dilaporkan di halaman

Validasi silang ≈ 0,97–0,99 F1 makro vs tulis-tangan recall 0,417–0,833; peringkat model berbalik; 59 dari 61 templat uji ada di latih; hipotesis "kosakata asing" ditolak; ambang dari validasi silang menurunkan recall tulis-tangan; emoji+hashtag+URL menurunkan recall.

### Perubahan di luar rencana yang ditemukan

`site_url` pada `mkdocs.yml` berubah menjadi `https://topekox.github.io/materi-nlp/` di luar edit saya (diduga perubahan pengguna); dibiarkan dan README disesuaikan.

## Log verifikasi Tahap 8 (audit akhir), 2026-10-23

| Pemeriksaan | Hasil |
|---|---|
| `python -m pytest -q` | **198 lolos**, 0 gagal |
| `check_page_outputs.py` Level 2–7, proyek, latihan | 54, 34, 44, 27, 31, 27, 17, 18 blok "Output nyata"; 0 tidak cocok |
| `mkdocs build --strict` (akhir, setelah perubahan CSS/JS) | Lolos (exit 0) |
| Audit browser `examples/audit/audit_browser.py` (Edge via Playwright, 119 halaman × dua ukuran layar: 1280 px dan 390 px) | 795 rumus MathJax dirender (1.590 kontainer), 0 galat MathJax; 107 dari 107 diagram Mermaid dirender; 0 permintaan gagal; 0 halaman meluap horizontal; satu-satunya temuan adalah diagram rusak yang **sengaja** ada di halaman contoh template (`examples/mermaid`) |
| Parse sintaks 107 diagram dengan `mermaid.parse` | Semua lolos kecuali diagram rusak sengaja di atas |
| Audit statis `examples/audit/audit_statis.py` (110 halaman navigasi): satu H1 per halaman, kolom tabel konsisten, tanda `$` seimbang, tanpa karakter kontrol/heading kosong/rumus di heading | Lolos, kecuali tanda `@@` di rencana dan log audit (teks yang menjelaskan bug penanda, bukan sisa penanda) |
| 121 URL eksternal pada seluruh dokumentasi dan README | 117 berstatus 200; 4 gagal: `contoh.id` ×2 dan `t.co/xyz123` adalah contoh fiktif di halaman media sosial; `uvicorn.org` hanya disebut sebagai URL lama di log ini |
| Inspeksi visual tangkapan layar (diagram urutan, rumus, tabel tema gelap, tabel layar ponsel, diagram lebar, rumus inline) | Layak; diagram urutan memiliki teks yang sedikit menempel pada garis kotak `alt`, tidak diperbaiki |

### Temuan Tahap 8 dan perbaikan

- **Diagram lebar tidak terbaca:** 60 dari 96 diagram lebih lebar dari kolom konten sehingga diperkecil (skala terburuk 0,38, teks ≈ 6 px). `useMaxWidth: false` untuk flowchart dan sequence di `docs/javascripts/mermaid-config.js` plus `overflow-x: auto` di `extra.css` mempertahankan ukuran asli dan menggulir horizontal. Konsekuensi: diagram sangat lebar (±1.900 px) perlu digeser; tidak ada penanda gulir yang terlihat di tangkapan layar headless.
- **Halaman meluap di layar ponsel:** 8 halaman (ukuran 390 px) meluap 24–263 px akibat rumus inline panjang yang tidak dapat membungkus. Diperbaiki dengan `span.arithmatex { display:inline-block; max-width:100%; overflow-x:auto }`; rumus display tetap terpusat (versi pertama aturan ini juga mengenai rumus display dan merusak pemusatannya; diperbaiki sebelum dipublikasikan).
- **Rumus mentah di daftar isi:** judul `Bagian 3: proyeksi $W_Q,W_K,W_V$` tampil sebagai `\(...\)`; judul diganti teks biasa dan pemeriksa statis kini menandai rumus di heading.
- **Rumus pecahan besar dalam kalimat** (halaman RNN) diubah menjadi rumus display.
- **URL mati** di Level 0 (tutorial scikit-learn "Working With Text Data" sudah tidak ada) diganti contoh resmi 20newsgroups.
- **Halaman Lampiran** masih berisi teks "sedang disusun"; diganti isi sebenarnya. Beranda mendapat kartu Latihan dan Kuis.

### Belum diperiksa setelah Tahap 8

- Rendering hanya diuji di Edge/Chromium (Playwright); Firefox dan Safari tidak.
- Tema gelap hanya diperiksa pada satu halaman secara visual; kontras warna tidak diukur; aksesibilitas (pembaca layar, navigasi papan ketik) tidak diuji.
- Tampilan layar ponsel hanya diuji untuk meluapnya halaman, bukan kenyamanan baca; diagram lebar di ponsel memerlukan gulir horizontal.
- Teks lengkap makalah yang dikutip tidak dibaca; hanya metadata yang diperiksa.
- Tidak ada tinjauan penutur asli atas bahasa; tidak ada uji keterbacaan pada pemula; kuis dan latihan tidak diuji pada pembaca sungguhan.
- Tidak ada tinjauan keamanan independen, uji beban, autentikasi, atau HTTPS pada API.
- Python selain 3.14.7 dan platform selain Windows tidak diuji (README menyebut Python 3.10+, yang **tidak diverifikasi**).
- GPU tidak diuji; hasil IndoBERT/LSTM hanya CPU, lima seed.
- Deployment GitHub Pages tidak dilakukan.

## Log verifikasi Tahap 6b–7 (eksperimen berat, proyek, latihan), 2026-10-23

!!! warning "Koreksi atas log Tahap 6"
    Log Tahap 6 di bawah menyebut "Level 7: 22 blok diperiksa, 0 tidak cocok" dan "skrip berat TIDAK dijalankan". Keduanya sudah tidak berlaku: (a) lima blok keluaran di halaman Level 7 sempat berisi penanda mentah `@@OUT ...@@` karena pembuat halaman tidak mengganti penanda satu baris; pemeriksa tidak menangkapnya karena penanda bukan blok kode. Setelah perbaikan, Level 7 memiliki **27** blok diperiksa, 0 tidak cocok. (b) Skrip berat sudah dijalankan (tabel di bawah). Pencarian `@@` di seluruh `docs/` kini kosong (selain berkas biner/aset).

| Pemeriksaan | Hasil |
|---|---|
| `pip install -r requirements-dl.txt` di `.venv` (Python 3.14.7, Windows) | Berhasil: torch 2.14.1 (CPU), transformers 5.20.2, datasets 5.1.0, accelerate 1.15.0; `CUDA tersedia: False` |
| `11_tokenizer_indobert.py` | Berjalan: kosakata 30.521; keluaran disalin ke halaman |
| Uji asap `12_finetune_indobert.py --subset 64 --epochs 1` | Berjalan (≈21 detik latih; recall tulis-tangan 0,583 pada 64 teks). Peringatan jinak `num_labels=2` vs `id2label` panjang 5 dijelaskan di halaman |
| `13_ulang_seed.py` IndoBERT p1, seed 1–5 | Berhasil; 111–217 detik/seed; hasil di `berat/hasil/indobenchmark_indobert_base_p1.*` |
| `13_ulang_seed.py` IndoLEM, seed 1–5 | Berhasil; hasil di `berat/hasil/indolem_indobert_base_uncased.*` |
| `13_ulang_seed.py --jenis lstm`, seed 1–5 | Berhasil; 5–8 detik/seed; satu seed menghasilkan recall tulis-tangan 0,000 |
| Percobaan peluncuran pertama (`nohup ... &`) | Tidak menghasilkan keluaran (proses terhenti bersama shell peluncur); diulang dengan latar belakang resmi. Tidak ada hasil dari percobaan itu yang dipakai |
| `python -m pytest -q` | **198 lolos** (20 tes API; termasuk tes Tahap A–B, latihan, dan kompilasi skrip `berat/`) |
| `check_page_outputs.py` Level 2, 3, 4, 5 | 54, 34, 44, 27 blok; 0 tidak cocok |
| `check_page_outputs.py` Level 6, Level 7, proyek, latihan | **31, 27, 17, 18** blok diperiksa; 0 tidak cocok. Pemeriksa kini mendukung blok menjorok (di admonition) |
| `mkdocs build --strict` | Lolos (exit 0); tabel hasil berat disertakan lewat snippet (`<table>` ada di halaman Tahap G) |
| Notebook `tahap_c_eda.ipynb` dibangun dan dieksekusi (nbclient) | Berhasil |
| Metadata referensi: 22 makalah via arXiv API, 8 via Crossref DOI, 3 via ACL Anthology/JMLR (judul halaman) | Judul, penulis pertama, dan tahun cocok untuk seluruh yang dicek. Venue konferensi/jurnal dari pengetahuan penulis, tidak diverifikasi terpisah; teks makalah tidak dibaca |
| 51 URL pada halaman Level 6–7, proyek, latihan, referensi | 50 berstatus 200; `https://www.uvicorn.org/` gagal DNS dan diganti `https://uvicorn.dev/` (200) |
| Waktu latih/prediksi pada halaman proyek | Diukur tiga kali pada mesin tanpa beban lain; nilai berubah-ubah dan ditandai demikian di halaman |

### Bug dan koreksi yang ditemukan saat menulis

- Penanda keluaran satu baris tidak diganti (lihat koreksi di atas).
- Pemeriksa keluaran tidak mengenali blok menjorok.
- Heuristik mention menandai `@contoh` pada alamat email sebagai mention (lookbehind ditambahkan, dijaga tes).
- Dua klaim draf diperiksa lalu dikoreksi: arti peringatan `num_labels` (jinak; `id2label` bawaan generik) dan perbandingan SVM 452 vs IndoBERT 335 teks (kini SVM dilatih pada data latih yang sama).
- Draf hipotesis penyebab FN diberi label "dugaan" karena belum diuji.
- Ada tabel dalam draf `13_ulang_seed.py` yang membandingkan IndoBERT (335 teks) dengan SVM (452 teks); diperbaiki sebelum dipublikasikan.

### Belum diperiksa (ditambah Tahap 6b–7)

- Eksperimen berat hanya di CPU; GPU tidak diuji. Hasil IndoBERT dapat berbeda pada versi/perangkat lain. Hiperparameter tidak disetel; penyebab IndoLEM jauh lebih rendah daripada p1 tidak diselidiki.
- Hasil neural hanya lima seed; tidak ada uji statistik; tulis-tangan 48 teks (24 Emergency) dilabeli satu orang; data sintetis bertemplat.
- Waktu inferensi IndoBERT tidak diukur; waktu latih IndoBERT seed pertama dipengaruhi proses lain yang berjalan bersamaan.
- Rumus LaTeX dan diagram Mermaid (termasuk `sequenceDiagram`) tidak dilihat di browser; tampilan tema gelap/terang tidak diperiksa.
- Teks lengkap makalah yang dikutip tidak dibaca; hanya metadata. Sisa belum diperiksa: Levy & Goldberg (2014), Platt (1999), buku Quiñonero-Candela dkk., Tukey (1977), dan OWASP.
- Kuis dan latihan baru (Level 0–7, proyek) belum diuji pada pembaca pemula; tidak ada tinjauan penutur asli.
- Tidak ada anotator independen; kappa pada Tahap A adalah contoh buatan.
- API tidak diuji beban, tanpa autentikasi/HTTPS; tidak ada Dockerfile.

## Log verifikasi Tahap 6 (Level 6–7), 2026-10-23

| Pemeriksaan | Hasil |
|---|---|
| `python -m pytest -q` (folder `examples/`, Python 3.14.7, numpy 2.5.4, scikit-learn 1.9.1, FastAPI 0.159.1) | **174 lolos**, 0 gagal, tanpa peringatan; 19 di antaranya tes API |
| `check_page_outputs.py` Level 2, 3, 4, 5 (regresi) | 54, 34, 44, 27 blok diperiksa; 0 tidak cocok |
| `check_page_outputs.py` Level 6 dan Level 7 | 31 dan 22 blok "Output nyata" diperiksa; **0 tidak cocok** (skrip dijalankan ulang; keluaran deterministik) |
| `mkdocs build --strict` setelah Level 6–7, glosarium, referensi, README | Lolos (exit 0); build tidak membutuhkan PyTorch dan tidak menjalankan kode |
| API dijalankan sebagai server (`uvicorn nlp_hub.api:buat_app --factory --port 8765`) dan dipanggil dengan `curl` | `/kesehatan` 200, `POST /prediksi` skor 0,3028 `Emergency`, `/docs` 200, `/riwayat/ringkasan` `total` 1; server dihentikan, port 8765 tertutup. Pengujian manual satu kali |
| Skrip `berat/` (`10_lstm_pytorch.py`, `11_tokenizer_indobert.py`, `12_finetune_indobert.py`) | Hanya `py_compile` (dijaga tes). **TIDAK dijalankan**: `torch` dan `transformers` tidak terpasang. Tidak ada hasil yang diklaim |
| ID dan metadata `indobenchmark/indobert-base-p1` dan `indolem/indobert-base-uncased` | Diperiksa pada halaman model di Hugging Face (ID, lisensi MIT, 124,5 juta parameter untuk yang pertama, makalah dan venue) |
| Pengukuran sekali-jalan yang dikutip di halaman: XOR dengan 1/2/8 neuron selama 10 seed (0/10, 1/10, 10/10); proporsi kata `rt`/`rumah` per kelas; keberadaan `meledak`, `longsor`, `jurang` di kosakata; skor tiga bentuk huruf nama tempat | Dijalankan dan angkanya dikutip; **tidak** ada di skrip halaman |

### Kesalahan yang ditemukan dan diperbaiki saat menulis

- *Gradient check*: rasio relatif per elemen memberi 1,1e-5 pada gradien nyaris nol padahal selisih absolut 1e-11; diganti ukuran berbasis norma per tensor (5e-11).
- `cek_lingkungan_dl.py` versi awal mencampur nama pip dan nama impor (`PackageNotFoundError: sklearn`).
- Draf halaman interpretabilitas menyatakan kata `meledak`/`longsor` kemungkinan tidak ada di kosakata; pemeriksaan menunjukkan keduanya ada (hanya `jurang` yang tidak). Teks dikoreksi.
- Draf latihan arsitektur mengira mengedit `model.json` memicu galat checksum; ternyata checksum hanya mencakup `model.joblib`. Latihan dan jawaban ditulis ulang, dan keterbatasan didokumentasikan.
- Draf bias menyebut kata `baca` sebagai kata yang dikenal model; pemeriksaan menunjukkan `baca` justru kata asing. Diganti `lalu`.
- Contoh ilustratif memakai nama tempat nyata (Wamena); diganti nama fiktif.
- Jawaban latihan XOR (1/2/8 neuron) awalnya berupa dugaan; diganti hasil pengukuran.
- Percobaan penulisan berkas lewat heredoc shell gagal dua kali (kesalahan quoting); berkas ditulis ulang dengan alat Write. Tidak ada berkas setengah jadi yang tersisa.

### Belum diperiksa (ditambah Tahap 6)

- **Seluruh kode PyTorch/Transformers belum dieksekusi**; perkiraan waktu dan memori fine-tuning adalah orde besaran, bukan pengukuran. Hasil IndoBERT, LSTM PyTorch, dan keluaran tokenizer nyata tidak ada di halaman.
- Rumus LaTeX (MathJax via CDN) dan diagram Mermaid (termasuk `sequenceDiagram`) tidak dirender/dilihat di browser; hanya `mkdocs build --strict` yang lolos.
- Hampir semua referensi akademik Level 6–7 ditandai "belum diperiksa daring" di `referensi.md` dan di halaman; hanya dua halaman model Hugging Face (dan Mitchell dkk. 2019 dari Tahap 4–5) yang diperiksa. URL dokumentasi resmi tidak dimuat ulang pada tahap ini.
- API tidak diuji beban/konkurensi, tidak punya autentikasi, HTTPS, atau pembatasan laju; tidak ada Dockerfile; `--workers N` tidak dicoba.
- Dasbor HTML tidak dibuka di browser (hanya status 200 dan isi teks di tes).
- Probe OOD (6 teks), uji kontrafaktual (14 teks Emergency), dan tulis-tangan (48 teks) sangat kecil dan ditulis/dilabeli oleh penulis yang sama; tidak ada kesimpulan statistik.
- Latihan dan kuis baru belum diuji pada pembaca pemula; tidak ada tinjauan penutur asli; tidak ada tinjauan keamanan independen.
- Tahap 7 (halaman proyek, `latihan/`, kuis gabungan) belum dikerjakan.

## Belum diperiksa (ditambah Tahap 4–5)

- Rumus LaTeX (MathJax via CDN) tidak dirender; hanya keseimbangan tanda `$` yang diperiksa.
- Tampilan di browser (tema gelap/terang, Mermaid) tidak diperiksa secara visual; hanya gambar PNG yang dilihat.
- Tidak ada tinjauan bahasa oleh penutur asli; tidak ada uji keterbacaan oleh pemula sungguhan.
- Tidak ada anotator independen untuk label; tulis-tangan dilabeli penulis yang sama dengan penulis data.
- Revisi Level 0–1 (Tahap 3b): latihan dan kuis baru belum diuji pada pembaca pemula; kualitas isi hanya diperiksa lewat pencocokan judul dan keluaran, bukan ditinjau manusia.

## Belum diperiksa (Tahap 1–3)

- Rendering visual di browser (hanya build statis yang diperiksa).
- Kebenaran DOI/URL di [Referensi](../referensi.md) terhadap sumber daring.
