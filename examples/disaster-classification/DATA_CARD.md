# Kartu Data: dataset sintetis klasifikasi Emergency / Non-Emergency

> **Seluruh data di folder ini SINTETIS.** Tidak ada postingan Twitter/X nyata,
> tidak ada akun nyata, dan tidak ada data pribadi. Dataset ini hanya untuk
> belajar. Skor model di dataset ini **tidak** membuktikan bahwa model layak
> dipakai untuk menanggapi keadaan darurat.

## Berkas

| Berkas | Isi | Dibuat oleh |
|---|---|---|
| `data/synthetic_disaster_id.csv` | 574 baris, dibangkitkan dari templat | `generate_dataset.py` (seed 20261023) |
| `data/handwritten_challenge_id.csv` | 48 baris tulis-tangan (24 Emergency, 24 Non-Emergency) | `tulis_uji_tangan.py` |

## Skema `synthetic_disaster_id.csv`

| Kolom | Arti |
|---|---|
| `source_id` | ID baris sintetis (`S0001`, ...). Bukan ID Twitter/X. |
| `event_id` | Kejadian fiktif (`E001`-`E080`). Dipakai sebagai kelompok pembagian data (`split_group`). |
| `post_type` | Jenis postingan menurut tabel di halaman *Masalah Emergency*. |
| `template_id` | Templat asal kalimat. Hanya ada karena datanya sintetis; dipakai untuk menguji kebocoran antartemplat. |
| `text` | Teks. Lokasi fiktif; akun `@..._contoh`; URL `contoh.example`. |
| `label` | `Emergency` atau `Non-Emergency`. |

`handwritten_challenge_id.csv` memiliki kolom `source_id` (`H001`...), `text`, `label`, dan `catatan` (kasus ambigu menurut penulis).

## Cara label ditetapkan

- Label pada dataset templat **ditentukan oleh jenis templat**: `laporan` dan `bantuan` = Emergency; `berita`, `info_lama`, `opini`, `peringatan`, `edukasi`, `candaan`, `tidak_terkait` = Non-Emergency. Tidak ada anotator manusia, sehingga tidak ada ukuran kesepakatan antaranotator.
- Label pada set tulis-tangan ditetapkan satu orang (penulis materi) dengan definisi operasional di `docs/level-0-orientasi/masalah-emergency.md`. Kasus ragu ditandai di kolom `catatan`; tidak ada label `uncertain` pada set ini.

## Komposisi dan keterbatasan

- Teks dari templat sangat berulang. Banyak postingan hampir sama kecuali lokasi dan gaya penulisan. Pembagian acak akan membuat kalimat yang hampir sama muncul di data latih dan data uji.
- Variasi gaya informal (singkatan, huruf berulang, typo, huruf kapital, emoji, hashtag, mention, URL) ditambahkan secara acak dengan **peluang yang sama untuk kedua label**.
- Ada 10 duplikat persis yang disengaja untuk meniru *retweet*.
- Enam bahaya: banjir, gempa, kebakaran, longsor, angin kencang, dan letusan gunung. Tidak ada tsunami, kecelakaan, dan sebagainya pada set latih.
- Distribusi kelas (Emergency sekitar 35%) dipilih penulis dan **bukan** estimasi proporsi di dunia nyata.
- Bahasa Indonesia hanya satu ragam informal buatan penulis; tidak mewakili dialek, bahasa daerah, atau campur kode.

## Penggunaan yang diperbolehkan

- Belajar dan latihan di NLP Learning Hub, termasuk menjalankan ulang notebook dan pengujian.
- Menunjukkan konsep: kebocoran data, pembagian kelompok, perbandingan pipeline.

## Penggunaan yang tidak sesuai

- Mengklaim performa pada postingan nyata.
- Melatih model untuk sistem tanggap darurat sungguhan.
- Melaporkan skor dataset ini sebagai hasil penelitian.

## Privasi dan etika

Tidak ada data pribadi. Jika Anda mengganti dataset ini dengan data nyata,
periksa syarat penggunaan sumbernya, hapus mention dan identitas pengguna,
dan jangan masukkan data mentah ke repository publik.
