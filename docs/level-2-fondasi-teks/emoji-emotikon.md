# Penanganan Emoji dan Emotikon

!!! abstract "Info materi"
    **Tingkat kesulitan:** Pemula–menengah. **Estimasi waktu:** 60–80 menit.
    **Jenis kode:** snippet edukatif (`examples/level-2-preprocessing/04_emoji.py`) dan fungsi `proses_emoji`.

## Tujuan pembelajaran

- [ ] Membedakan emoji (karakter Unicode) dan emotikon (rangkaian tanda baca seperti `:(`).
- [ ] Menjelaskan tiga strategi: pertahankan, hapus, ubah menjadi kata.
- [ ] Mengenali keterbatasan pemetaan emoji ke kata (emoji ambigu, emoji majemuk, emoji yang tidak dikenal).
- [ ] Memeriksa dengan data apakah emoji benar-benar berkorelasi dengan label.

## Prasyarat

- [Karakter, Unicode, dan Encoding UTF-8](karakter-unicode-encoding.md).
- [Case Folding, Tanda Baca, dan Pembersihan](case-folding-pembersihan.md).

## Pengantar dan motivasi

Emoji membawa emosi dan konteks yang sering tidak ada di kata-kata. `🙏`
dapat berarti permohonan ("tolong 🙏") atau terima kasih. `🌊` dan `🔥` dapat
menjadi kata kunci bencana. Namun `😭` dapat berarti sedih, tetapi juga dipakai
saat tertawa. Jika semua emoji dibuang, sinyal itu hilang; jika semua dipetakan
tanpa berpikir, ambiguitas ikut masuk ke model.

## Konsep dasar

| Istilah | Penjelasan | Contoh |
|---|---|---|
| **Emoji** | Karakter Unicode bergambar | 🙏 😭 🔥 🌊 🆘 |
| **Emotikon** | Rangkaian karakter ASCII yang membentuk wajah | `:(` `:)` `T_T` `:'(` |
| **Emoji majemuk** | Beberapa code point membentuk satu gambar (warna kulit, hati dengan *variation selector*) | `👍🏽`, `❤️` |

## Penjelasan mendalam

### Tiga strategi

| Strategi | Efek | Kapan masuk akal |
|---|---|---|
| `pertahankan` | Teks tidak diubah. Namun tokenizer regex membuang emoji, sehingga efeknya sama dengan `hapus` pada paket ini | Bila akan memakai tokenizer lain yang mengenal emoji |
| `hapus` | Emoji dan emotikon dibuang | Bila emoji dianggap tidak informatif |
| `kata` | Emoji diganti token seperti `emo_doa`, emotikon `emo_sedih` | Bila emoji dianggap membawa sinyal |

Memetakan emoji ke kata tertentu adalah **keputusan penafsiran**, bukan fakta.
Kamus pada `nlp_hub/kamus.py` (`EMOJI_KE_KATA`) kecil dan dibuat tangan:
hanya 12 emoji. Emoji di luar daftar menjadi `emo_lain`.

### Emoji tidak dikenal dan emoji majemuk

Emoji dengan warna kulit (`👍🏽`) terdiri dari dua code point: emoji dasar
dan *modifier* warna kulit. Pola sederhana memperlakukan keduanya sebagai dua
emoji terpisah. Hati merah `❤️` terdiri dari U+2764 dan *variation
selector* U+FE0F yang sudah dibuang oleh normalisasi Unicode.

### Ambiguitas

Emoji yang sama bisa dipakai pada konteks berlawanan. `😭` pada "rumah kami
terendam 😭 tolong" dan pada "dompetku kebanjiran 😭 wkwk" dipetakan ke token
yang sama, `emo_menangis`, padahal pertama darurat dan kedua candaan. Model
perlu kata di sekitarnya untuk membedakan.

## Cara kerja atau alur proses

1. Ganti emotikon lebih dulu (pola lebih panjang dahulu: `:'(` sebelum `:(`).
2. Ganti emoji menurut kamus; sisanya `emo_lain`.
3. Lanjut ke case folding dan tokenisasi.

Emoji harus ditangani **sebelum** tokenisasi karena tokenizer regex hanya
mengenal huruf dan angka.

## Contoh sederhana

`"Tolong 🙏"` → `"Tolong emo_doa"`. Emoji berubah menjadi satu kata yang dapat
dihitung seperti kata lain.

## Contoh dalam konteks Twitter/X kebencanaan

Dua postingan sintetis dengan emoji yang sama:

| Postingan | Label menurut definisi |
|---|---|
| "Rumah kami terendam 😭 tolong" | Emergency |
| "Dompetku kebanjiran 😭 wkwk" | Non-Emergency |

Contoh ini menunjukkan bahwa emoji saja tidak menentukan label.

## Praktik Python

Berkas: `examples/level-2-preprocessing/04_emoji.py`.

### Bagian 1 — Mendeteksi emoji

```python title="Bagian 1"
--8<-- "level-2-preprocessing/04_emoji.py:deteksi"
```

`POLA_EMOJI` adalah regex yang cocok dengan satu karakter di rentang emoji.
`findall` mengembalikan list semua kecocokan.

```text title="Output nyata"
['🙏', '😭', '😭']
3
```

Interpretasi: tiga emoji terdeteksi. Emotikon `:(` dan `T_T` **tidak** terdeteksi
karena memang bukan emoji; keduanya ditangani pola terpisah.

### Bagian 2 — Tiga mode

```python title="Bagian 2"
--8<-- "level-2-preprocessing/04_emoji.py:mode"
```

```text title="Output nyata"
pertahankan -> 'Tolong 🙏 air naik 😭😭 :( T_T'
hapus -> 'Tolong air naik'
kata -> 'Tolong emo_doa air naik emo_menangis emo_menangis emo_sedih emo_menangis'
```

Interpretasi: mode `kata` mengubah `:(` menjadi `emo_sedih` dan `T_T` menjadi
`emo_menangis`. Dua emoji `😭` berurutan menghasilkan dua token yang sama;
jumlah pengulangan masih terbawa sebagai frekuensi.

### Bagian 3 — Kasus tepi

```python title="Bagian 3"
--8<-- "level-2-preprocessing/04_emoji.py:tak_dikenal"
```

```text title="Output nyata"
aman emo_lain emo_setuju emo_lain
2 ['0x1f44d', '0x1f3fd']
hati emo_hati untuk korban
```

Interpretasi:

- `🦖` tidak ada di kamus → `emo_lain`.
- `👍🏽` menghasilkan **dua** token: `emo_setuju` dan `emo_lain` (modifier warna kulit). Panjang string 2 dan dua code point berbeda, ini mengonfirmasi penyebabnya.
- `❤️` menghasilkan satu token karena `praproses` memakai `normalisasi_unicode`, yang membuang U+FE0F lebih dulu.

### Bagian 4 — Ambiguitas

```python title="Bagian 4"
--8<-- "level-2-preprocessing/04_emoji.py:ambigu"
```

```text title="Output nyata"
rumah kami terendam emo_menangis tolong
dompetku kebanjiran emo_menangis wkwk
```

Interpretasi: token `emo_menangis` sama pada dua teks yang berlabel berbeda. Yang
membedakan keduanya adalah kata lain (`tolong` dan `wkwk`).

### Bagian 5 — Apakah emoji berkorelasi dengan label?

```python title="Bagian 5"
--8<-- "level-2-preprocessing/04_emoji.py:statistik"
```

- `df["text"].apply(...)` menjalankan fungsi pada tiap teks.
- `groupby("label")[...].agg(["sum", "count", "mean"])` menghitung per kelas: jumlah teks berisi emoji (`sum`), jumlah teks (`count`), dan proporsinya (`mean`).

```text title="Output nyata"
               sum  count   mean
label                           
Emergency       37    191  0.194
Non-Emergency   75    373  0.201
```

Interpretasi: kurang dari 20% teks pada kedua kelas memuat emoji, dan
proporsinya hampir sama (0,194 versus 0,201). Ini **bukan temuan tentang
dunia nyata**: pada dataset sintetis ini, emoji ditambahkan secara acak dengan
peluang yang sama untuk kedua label (lihat `DATA_CARD.md`). Karena itu
dataset ini tidak dapat dipakai untuk menilai manfaat emoji pada data
sungguhan. Pada data nyata, cek tabel serupa terlebih dahulu.

### Skrip terpadu

Fungsi siap pakai `proses_emoji` ada di `examples/nlp_hub/preprocessing.py`,
dengan tes di `examples/tests/test_preprocessing.py` (termasuk
`test_emoji_sos_di_blok_berbeda_tetap_terdeteksi`, lihat bagian berikut).

## Kesalahan umum dan debugging

| Gejala | Penyebab | Perbaikan |
|---|---|---|
| `🆘` tidak terdeteksi sebagai emoji | Pola awal hanya mencakup blok `1F300–1FAFF`; `🆘` ada di blok `1F100–1F1FF` | Perluas rentang pola. Kasus ini ditemukan saat menyusun pelajaran ini, dan diperbaiki dengan tes khusus |
| Satu emoji menjadi dua token (`👍🏽`) | Modifier warna kulit dipecah | Buang modifier `\U0001F3FB`–`\U0001F3FF` sebelum pemetaan |
| `UnicodeEncodeError` saat mencetak | Konsol tidak mendukung emoji | `python -X utf8` atau `pakai_utf8()` |
| Emotikon rusak karena tanda baca dibuang lebih dulu | Urutan langkah | Tangani emotikon sebelum tanda baca dihapus |
| Semua emoji tidak dikenal menjadi `emo_lain` | Kamus kecil | Tambah emoji yang sering muncul di **data Anda**, bukan dari tebakan |

!!! info "Pelajaran dari bug `🆘`"
    Emoji SOS adalah salah satu yang paling relevan untuk darurat, tetapi
    regex pertama tidak mengenalinya. Kesalahan jenis ini hanya tertangkap bila
    ada tes yang memakai contoh dari domain Anda.

## Kelebihan dan keterbatasan

**Kelebihan:** menjaga sinyal emosi yang tidak ada di kata; mudah dijelaskan.
**Keterbatasan:** kamus buatan tangan dan kecil; emoji ambigu; emoji
majemuk; makna emoji berubah menurut komunitas dan waktu; pada dataset
sintetis tidak ada bukti manfaat.

## Latihan bertahap

1. **Konseptual.** Apa beda emoji dan emotikon? Beri dua contoh tiap jenis.
2. **Membaca kode.** Berapa hasil `len(POLA_EMOJI.findall("🔥🔥 api besar 🚨"))`?
3. **Fill-in.** Lengkapi: `proses_emoji(":D T_T :-)", "kata")` menghasilkan ... .
4. **Debugging.** `proses_emoji("aman 👍🏽", "kata")` menghasilkan dua token. Tulis perbaikan sederhana.
5. **Mini-proyek.** Dari dataset Anda sendiri (data nyata bila ada), hitung 5 emoji paling sering dan usulkan pemetaan kata. Apa risiko memetakan hanya berdasarkan bentuk gambarnya?

## Kunci jawaban dan pembahasan

??? success "Jawaban 1"
    Emoji adalah karakter Unicode bergambar (🙏, 🔥). Emotikon adalah rangkaian karakter biasa yang membentuk wajah (`:(`, `T_T`). Pembahasan: emoji punya code point sendiri; emotikon hanyalah tanda baca sehingga bisa rusak bila tanda baca dibuang.

??? success "Jawaban 2"
    `3` (dua `🔥` dan satu `🚨`). Sudah diperiksa dengan eksekusi.

??? success "Jawaban 3"
    `emo_tertawa emo_menangis emo_senyum`. Hasil diperiksa dengan eksekusi; urutan sesuai kemunculan.

??? success "Jawaban 4"
    ```python
    import re
    MODIFIER_KULIT = re.compile("[\U0001F3FB-\U0001F3FF]")
    proses_emoji(MODIFIER_KULIT.sub("", "aman 👍🏽"), "kata")
    ```
    Hasil yang dijalankan: `aman emo_setuju`. Modifier dibuang sebelum pemetaan sehingga tinggal emoji dasar. Pembahasan: pola kita menganggap setiap code point sebagai emoji sendiri.

??? success "Jawaban 5"
    Contoh jawaban: tulis tabel frekuensi dengan `Counter`, lalu petakan hanya emoji yang punya makna stabil di komunitas data Anda. Risiko: makna dipengaruhi konteks (😭 sedih atau tertawa; 🙏 minta tolong atau terima kasih). Cara mengurangi: lihat 10–20 contoh nyata tiap emoji sebelum memetakan, dan ukur apakah pemetaan memperbaiki metrik pada data validasi.

## Kuis singkat

**1.** Mengapa emoji diproses sebelum tokenisasi?

??? success "Jawaban"
    Tokenizer regex hanya mengenal huruf dan angka, sehingga emoji akan hilang jika diproses setelahnya.

**2.** Mengapa `emo_menangis` pada dua teks berlabel berbeda menjadi masalah?

??? success "Jawaban"
    Satu token tidak membedakan konteks. Model perlu kata lain di sekitarnya, dan token tunggal ini tidak informatif jika dipakai sendirian.

**3.** Bolehkah menyimpulkan manfaat emoji dari dataset sintetis ini?

??? success "Jawaban"
    Tidak. Emoji ditambahkan acak dan independen terhadap label, sehingga data tidak mencerminkan pemakaian nyata.

## Ringkasan

- Emoji adalah karakter Unicode; emotikon adalah rangkaian tanda baca.
- Tiga strategi: pertahankan, hapus, ubah menjadi kata. Pilihan dibuktikan dengan eksperimen.
- Emoji majemuk, emoji tidak dikenal, dan ambiguitas adalah sumber galat.
- Pada dataset sintetis, emoji tidak berkorelasi dengan label karena dibangkitkan secara acak.

## Glosarium istilah baru

Emoji
:   Karakter Unicode bergambar.

Emotikon
:   Rangkaian karakter ASCII yang membentuk wajah, seperti `:(`.

Modifier warna kulit
:   Code point tambahan yang mengubah warna kulit pada emoji manusia.

Variation selector
:   Code point (U+FE0F) yang meminta tampilan gambar emoji.

## Referensi

- Unicode Consortium, *Unicode Emoji* (daftar dan aturan emoji): <https://unicode.org/emoji/> (standar).
- Dokumentasi Python, modul `re`: <https://docs.python.org/3/library/re.html>.

## Materi berikutnya

[Normalisasi Bahasa Informal, Huruf Berulang, dan Typo](normalisasi-informal.md)
