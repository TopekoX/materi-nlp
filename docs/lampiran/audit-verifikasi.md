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

## Belum diperiksa (ditambah Tahap 4–5)

- Rumus LaTeX (MathJax via CDN) tidak dirender; hanya keseimbangan tanda `$` yang diperiksa.
- Tampilan di browser (tema gelap/terang, Mermaid) tidak diperiksa secara visual; hanya gambar PNG yang dilihat.
- Tidak ada tinjauan bahasa oleh penutur asli; tidak ada uji keterbacaan oleh pemula sungguhan.
- Tidak ada anotator independen untuk label; tulis-tangan dilabeli penulis yang sama dengan penulis data.
- Revisi Level 0–1 (Tahap 3b): latihan dan kuis baru belum diuji pada pembaca pemula; kualitas isi hanya diperiksa lewat pencocokan judul dan keluaran, bukan ditinjau manusia.

## Belum diperiksa (Tahap 1–3)

- Rendering visual di browser (hanya build statis yang diperiksa).
- Kebenaran DOI/URL di [Referensi](../referensi.md) terhadap sumber daring.
