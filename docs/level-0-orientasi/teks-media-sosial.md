# Mengenal Teks Media Sosial

## Tujuan pembelajaran

- [ ] Mengenali ciri khas teks media sosial: bahasa informal, singkatan, emoji, hashtag, URL, dan mention.
- [ ] Menjelaskan mengapa ciri tersebut menyulitkan NLP dan kapan justru informatif.
- [ ] Mengekstrak ciri tersebut dengan regex sederhana.

## Prasyarat

[Memahami Masalah Emergency vs Non-Emergency](masalah-emergency.md).

## Pengantar dan intuisi

Teks buku dan berita ditulis rapi. Postingan saat bencana ditulis terburu-buru,
dari ponsel, sering dengan panik. Akibatnya teks penuh singkatan, salah ketik,
huruf diulang, dan simbol. NLP yang dilatih pada teks rapi sering gagal di sini.

## Konsep

| Ciri | Contoh | Tantangan | Bisa informatif? |
|---|---|---|---|
| Bahasa informal | "cepet bgt", "gak", "udh" | Banyak variasi ejaan | Ya, penanda gaya darurat |
| Singkatan | "tlg", "yg", "dgn" | Ambigu, tidak baku | Ya |
| Huruf berulang | "TOLOOONG" | Memecah kosakata | Ya, intensitas emosi |
| Huruf kapital | "BANJIR!!" | Case folding menghilangkannya | Mungkin |
| Emoji | 🙏 🆘 😭 | Bukan kata, makna kontekstual | Mungkin |
| Hashtag | #banjir #gempaMalang | Gabungan kata, bisa menandai peristiwa | Ya |
| Mention | @bpbd_kota | Nama akun, mengandung identitas | Kadang; mempertimbangkan privasi |
| URL | https://t.co/xyz | Tidak bermakna sebagai kata | Sering hanya penanda berita |
| Bahasa campuran | "stuck di jalan, tolong help" | Kosakata multibahasa | Ya |

!!! tip "Jangan buang otomatis"
    Banyak tutorial menghapus semua tanda baca, emoji, dan hashtag.
    Keputusan itu harus berdasarkan tujuan dan eksperimen. Misalnya, URL
    berita bisa menjadi sinyal Non-Emergency, sedangkan "!!!" bisa menjadi
    sinyal urgensi. Pembahasan lengkap ada di Level 2.

### Privasi

Mention dan nama pengguna dapat mengidentifikasi orang. Untuk materi belajar
dan dataset, **anonimkan** mention (mis. ganti menjadi `@USER`) dan jangan
menyimpan identitas yang tidak dibutuhkan.

## Contoh kontekstual kebencanaan

Satu postingan sintetis:

```text
@bpbd_kota TOLOOONG banjir naik cepet bgt di Jl. Melati 🙏 #banjir https://t.co/xyz123
```

Ia memuat mention, huruf berulang, singkatan (`bgt`), emoji, hashtag, dan URL
sekaligus. Satu kalimat pendek, enam tantangan.

## Contoh kode

```python title="ciri_media_sosial.py" linenums="1"
--8<-- "level-0-orientasi/ciri_media_sosial.py"
```

### Penjelasan kode

1. `POLA` adalah kamus nama ciri → pola regex yang sudah dikompilasi. Regex dipelajari lebih dalam di Level 1.
2. `https?://\S+` cocok dengan `http`/`https` diikuti karakter bukan spasi; `@\w+` dan `#\w+` cocok dengan mention dan hashtag; `(\w)\1{2,}` cocok dengan karakter yang sama berturut-turut tiga kali atau lebih.
3. `ekstrak_ciri` mengembalikan kamus nama ciri → daftar kecocokan.

### Output dan interpretasi

Output nyata (dijalankan dengan `python -X utf8` agar emoji tampil di Windows):

```text
@bpbd_kota TOLOOONG banjir naik cepet bgt di Jl. Melati 🙏 #banjir https://t.co/xyz123
url            : ['https://t.co/xyz123']
mention        : ['@bpbd_kota']
hashtag        : ['#banjir']
emoji          : ['🙏']
huruf_berulang : ['OOO']
```

Perhatikan bahwa `huruf_berulang` hanya menangkap `OOO` dari `TOLOOONG`, bukan
kata utuhnya, karena pola menangkap rangkaian yang diulang. Menormalkan
`TOLOOONG` menjadi `tolong` membutuhkan langkah lanjutan (Level 2). Singkatan
`bgt` dan `cepet` juga tidak tertangkap; itu perlu kamus normalisasi.

## Kesalahan umum

- Menghapus semua simbol tanpa mengevaluasi dampaknya.
- Menyimpan nama pengguna asli pada dataset belajar.
- Mengira regex dapat menyelesaikan seluruh variasi informal. Regex menangkap pola, bukan makna.
- Lupa mengatur encoding UTF-8 saat membaca atau mencetak emoji.

## Latihan mandiri

1. Tambahkan pola untuk mendeteksi tanda seru berulang (`!!!`) pada `POLA`.
2. Tulis tiga postingan sintetis dengan campuran bahasa Indonesia dan Inggris, lalu daftar ciri yang muncul.
3. Berikan argumen kapan URL dapat membantu dan kapan merugikan klasifikasi.

## Kuis singkat

**1.** Mengapa `TOLOOONG` dan `tolong` menjadi masalah bagi model?

??? success "Jawaban"
    Keduanya dianggap kata berbeda sehingga kosakata membengkak dan sinyal terpecah, kecuali dinormalisasi.

**2.** Mengapa mention perlu dianonimkan pada dataset belajar?

??? success "Jawaban"
    Mention dapat mengidentifikasi individu; privasi harus dijaga dan identitas tidak diperlukan untuk tujuan klasifikasi.

## Ringkasan

Teks media sosial penuh variasi informal. Ciri-cirinya dapat berupa masalah
sekaligus sinyal; keputusan memakai atau membuangnya harus berdasarkan tujuan
dan eksperimen, serta mempertimbangkan privasi.

## Referensi

- Dokumentasi Python: modul `re` (<https://docs.python.org/3/library/re.html>).

## Materi selanjutnya

[Dataset, Fitur, Label, Model, Training, dan Inference](istilah-dasar-ml.md)
