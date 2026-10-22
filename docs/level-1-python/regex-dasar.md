# Dasar Regex dengan `re`

## Tujuan pembelajaran

- [ ] Membaca dan menulis pola regex sederhana.
- [ ] Memakai `re.findall`, `re.search`, `re.sub`, dan `re.compile`.
- [ ] Mengenali batas regex dan jebakan umumnya.

## Prasyarat

[CSV dan JSON](csv-json.md) dan [String dan Operasi Teks](string-operasi-teks.md).

## Pengantar dan intuisi

*Regular expression* (regex) adalah bahasa kecil untuk mendeskripsikan **pola
teks**: "dua digit diikuti titik dua digit" (jam), "kata yang diawali #"
(hashtag). Ia sangat berguna untuk membersihkan URL, mention, dan angka,
tetapi regex menangkap *bentuk*, bukan *makna*.

## Konsep

| Pola | Arti |
|---|---|
| `\d` | satu digit |
| `\w` | huruf, digit, atau `_` |
| `\s` | spasi/tab/baris baru |
| `.` | karakter apa saja (kecuali baris baru) |
| `+` | satu atau lebih |
| `*` | nol atau lebih |
| `?` | opsional |
| `{2,}` | dua kali atau lebih |
| `[abc]` | salah satu dari a, b, c |
| `( )` | grup penangkap |
| `\1` | rujukan ke grup 1 |
| `\b` | batas kata |

Gunakan **raw string** (`r"..."`) agar `\d` tidak diartikan sebagai escape Python.

| Fungsi | Kegunaan |
|---|---|
| `re.findall(p, s)` | semua kecocokan sebagai list |
| `re.search(p, s)` | kecocokan pertama di mana pun |
| `re.match(p, s)` | kecocokan hanya di **awal** string |
| `re.sub(p, pengganti, s)` | mengganti semua kecocokan |
| `re.compile(p)` | kompilasi pola untuk dipakai ulang |

## Contoh kontekstual kebencanaan

Dari satu postingan kita ingin mengambil RT/RW, jam, hashtag, mention, serta
mengganti URL. Pola ini muncul kembali pada pipeline preprocessing Level 2.

## Contoh kode

```python title="15_regex_dasar.py" linenums="1"
--8<-- "level-1-python/15_regex_dasar.py"
```

### Penjelasan kode

1. `\d+` mengambil semua rangkaian digit; `#\w+` dan `@\w+` mengambil hashtag dan mention.
2. `https?://\S+` mencocokkan URL (`s` opsional, lalu karakter non-spasi); `re.sub` menggantinya dengan `<URL>`.
3. `RT (\d+)/RW (\d+)` memiliki dua grup; `.groups()` mengembalikan keduanya.
4. `\b\d{1,2}\.\d{2}\b` mencocokkan jam seperti `06.30`.
5. `\s+` → satu spasi merapikan spasi berlebih.
6. `re.match` hanya cocok di awal sehingga `"ada banjir"` menghasilkan `None`, padahal `search` menemukannya.
7. `(\w)\1{2,}` menangkap satu karakter lalu mengulangi karakter sama dua kali lebih; diganti dengan satu karakter (`\1`) sehingga `TOLOOONG` menjadi `TOLONG`.

### Output dan interpretasi

```text
['05', '12', '06', '30', '120']
['#banjir'] ['@bpbd']
@bpbd Banjir di RT 05/RW 12 sejak 06.30, tinggi 120 cm <URL> #banjir
('05', '12')
['06.30']
banjir naik cepat
None True
TOLONG
```

- `\d+` memecah `06.30` menjadi `06` dan `30`; pola terlalu umum memberi hasil yang tak diinginkan.
- Pola khusus jam (`\b\d{1,2}\.\d{2}\b`) menangkap `06.30` utuh.
- `TOLOOONG` menjadi `TOLONG` karena tiga `O` dipadatkan menjadi satu. Pola ini hanya menyentuh tiga huruf kembar atau lebih, sehingga kata sah seperti `saat` tidak berubah. Jika batasnya diturunkan menjadi dua huruf kembar, `saat` akan menjadi `sat`. Pemadatan huruf berulang dibahas lebih lanjut di Level 2.

## Kesalahan umum

- Lupa raw string.
- Pola serakah (`.*`) yang menelan terlalu banyak.
- Memakai `match` padahal maksudnya `search`.
- Mengira regex mampu memahami konteks. "Banjir" di "bukan banjir" tetap cocok.
- Pola sangat rumit tanpa tes; sulit dipelihara.

## Latihan mandiri

1. Tulis regex yang menangkap nomor telepon berformat `08xx-xxxx-xxxx` pada kalimat contoh.
2. Ganti semua angka dengan `<ANGKA>`.
3. Ubah pola huruf berulang agar hanya menormalkan pengulangan **tiga atau lebih** menjadi **dua** huruf (hasil `TOLOONG`).

## Kuis singkat

**1.** Beda `re.search` dan `re.match`?

??? success "Jawaban"
    `match` hanya mencocokkan di awal string; `search` mencari di mana saja.

**2.** Mengapa memakai raw string untuk pola?

??? success "Jawaban"
    Agar backslash dibaca regex, bukan sebagai escape Python.

## Ringkasan

Regex efektif untuk pola berbentuk tetap seperti URL, mention, dan jam.
Mulai dari pola sederhana, uji pada contoh, dan sadari bahwa regex tidak
memahami makna.

## Referensi

- Dokumentasi Python: modul `re` dan *Regular Expression HOWTO* (<https://docs.python.org/3/howto/regex.html>).

## Materi selanjutnya

[Debugging dan Pengujian Kode Sederhana](debugging-pengujian.md)
