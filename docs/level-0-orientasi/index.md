# Level 0: Orientasi NLP

Level ini tidak menuntut kemampuan pemrograman. Tujuannya membangun peta mental: apa itu NLP, apa masalah yang akan kita selesaikan, dan bagaimana menyiapkan lingkungan kerja. Beberapa halaman memuat kode Python pendek; Anda boleh membacanya saja, dan setiap kode dijelaskan baris per baris. Python dipelajari sistematis di [Level 1](../level-1-python/index.md).

**Estimasi waktu:** 6–8 jam, termasuk instalasi dan mini proyek.
**Prasyarat:** tidak ada selain komputer dan kemauan belajar.

## Daftar materi

| # | Materi | Tingkat | Inti | Kode contoh |
|---|---|---|---|---|
| 1 | [AI, ML, Deep Learning, NLP, Text Mining](ai-ml-dl-nlp.md) | Pemula | Peta istilah | `kata_kunci.py` |
| 2 | [Hubungan NLP dengan Machine Learning](hubungan-nlp-ml.md) | Pemula | Teks → angka → keputusan | `teks_ke_angka.py` |
| 3 | [Penerapan NLP di Kehidupan Nyata](penerapan-nlp.md) | Pemula | Jenis tugas dan biaya kesalahan | `beban_peninjauan.py` |
| 4 | [Cara Kerja Klasifikasi Teks](cara-kerja-klasifikasi-teks.md) | Pemula | Training vs inference | `klasifikasi_mini.py` |
| 5 | [Masalah Emergency vs Non-Emergency](masalah-emergency.md) | Pemula | Definisi label dan aturan anotasi | (tanpa kode) |
| 6 | [Teks Media Sosial](teks-media-sosial.md) | Pemula | Informal, emoji, hashtag, URL | `ciri_media_sosial.py` |
| 7 | [Dataset, Fitur, Label, Model](istilah-dasar-ml.md) | Pemula | Kosakata dasar ML | `istilah_dasar.py` |
| 8 | [Persiapan Python dan Git](persiapan-python.md) | Pemula | venv, pip, Jupyter, Git | (perintah terminal) |
| 9 | [Instalasi dan Verifikasi](verifikasi-lingkungan.md) | Pemula | Lingkungan yang dapat direproduksi | `verifikasi_lingkungan.py` |
| 10 | [Mini Proyek: Pelabelan Manual](mini-proyek-manual.md) | Pemula | Anotasi, kesepakatan, kappa | `kesepakatan.py` |

## Capaian

- [ ] Menjelaskan hubungan AI, ML, DL, dan NLP.
- [ ] Menyatakan definisi operasional Emergency dan Non-Emergency.
- [ ] Menjelaskan training, inference, fitur, label, dan alasan data uji dipisahkan.
- [ ] Menjalankan skrip Python dari lingkungan virtual yang terverifikasi.

## Kode contoh

Semua skrip Level 0 ada di `examples/level-0-orientasi/` dan bersifat **ilustratif**; tidak ada yang merupakan eksperimen atau evaluasi model. Data pada skrip adalah data sintetis kecil dan angka kesepakatan atau akurasi di dalamnya bukan hasil penelitian.

Pada tiap halaman, skrip dipecah menjadi bagian bernama (`--8<-- "file.py:bagian"`), dan setiap blok "Output nyata" dicocokkan otomatis dengan hasil eksekusi skrip (`examples/check_page_outputs.py`). Blok yang bertuliskan "jalur dan versi berbeda tiap komputer" sengaja dikecualikan karena bergantung pada mesin. Lihat [Audit dan Verifikasi](../lampiran/audit-verifikasi.md).

Untuk menjalankan skrip dari akar repository (setelah `.venv` aktif):

```bash
python -X utf8 examples/level-0-orientasi/klasifikasi_mini.py
```

## Checkpoint praktis

Sebelum lanjut ke Level 1, pastikan Anda dapat, tanpa melihat catatan:

1. Menyebut dua syarat sebuah postingan diberi label Emergency, dan memberi satu contoh yang memuat kata "tolong" tetapi Non-Emergency.
2. Menjelaskan perbedaan training dan inference, serta mengapa akurasi pada data latih menyesatkan.
3. Menunjukkan di terminal bahwa `.venv` aktif (`sys.executable`).
4. Menghitung persentase kesepakatan dua anotator pada empat contoh.

## Materi selanjutnya

Mulai dengan [AI, ML, Deep Learning, NLP, dan Text Mining](ai-ml-dl-nlp.md). Setelah Level 0, lanjut ke [Level 1: Python](../level-1-python/index.md).
