# Indexing dan Slicing

## Tujuan pembelajaran

- [ ] Mengambil elemen tunggal dan irisan dari string dan list.
- [ ] Memakai indeks negatif dan `step`.
- [ ] Membedakan galat indexing dan perilaku slicing yang aman.

## Prasyarat

[String dan Operasi Teks](string-operasi-teks.md).

## Pengantar dan intuisi

Indeks Python mulai dari **0**. Bayangkan nomor di *antara* huruf: `[a:b]`
mengambil dari batas ke-`a` sampai batas ke-`b` (tidak termasuk `b`). Indeks
negatif menghitung dari belakang: `-1` adalah elemen terakhir.

## Konsep

```text
teks     =  b  a  n  j  i  r  _  b  a  n  d  a  n  g
indeks   =  0  1  2  3  4  5  6  7  8  9 10 11 12 13
negatif  = -14 ...                              -2 -1
```

(`_` melambangkan spasi.)

| Ekspresi | Arti |
|---|---|
| `s[0]` | elemen pertama |
| `s[-1]` | elemen terakhir |
| `s[a:b]` | dari `a` hingga sebelum `b` |
| `s[a:]`, `s[:b]` | dari `a` sampai akhir; dari awal sampai sebelum `b` |
| `s[::-1]` | dibalik |
| `s[::2]` | setiap elemen kedua |

Indexing di luar rentang menimbulkan `IndexError`, tetapi slicing di luar
rentang mengembalikan hasil kosong tanpa galat.

## Contoh kontekstual kebencanaan

Memotong teks panjang untuk pratinjau, mengambil kata pertama sebagai
kandidat kata kerja, atau membuang tanda `#` dari hashtag (`"#banjir"[1:]`).

## Contoh kode

```python title="03_indexing_slicing.py" linenums="1"
--8<-- "level-1-python/03_indexing_slicing.py"
```

### Penjelasan kode

1. `teks[0]` dan `teks[-1]` mengambil karakter pertama dan terakhir.
2. `teks[0:6]` mengambil enam karakter pertama, `teks[7:]` sisanya setelah spasi.
3. `teks[::-1]` membalik string.
4. `kata = teks.split()` membuat list; indexing berlaku sama pada list.
5. Blok `try/except` menangkap `IndexError`; slice di luar rentang aman.

### Output dan interpretasi

```text
b g
banjir
bandang
gnadnab rijnab
banjir bandang ['bandang', 'banjir']
ban...
IndexError: string index out of range
True
```

Slice `teks[100:105]` menghasilkan string kosong, sehingga perbandingan
dengan `""` benar. Sifat ini praktis, tetapi dapat menyembunyikan bug bila
Anda mengira slice pasti berisi.

## Kesalahan umum

- Lupa bahwa indeks akhir pada slice **tidak** diikutsertakan (off-by-one).
- Mengakses `s[len(s)]`; indeks valid terakhir adalah `len(s) - 1`.
- Mengindeks list kosong tanpa memeriksanya.

## Latihan mandiri

1. Ambil nama hashtag tanpa `#` dari `"#banjirJakarta"`.
2. Ambil tiga kata terakhir dari kalimat berisi lima kata.
3. Tulis fungsi yang mengembalikan 20 karakter pertama diikuti `...` hanya jika teks lebih panjang.

## Kuis singkat

**1.** Hasil `"gempa"[1:3]`?

??? success "Jawaban"
    `"em"` (indeks 1 dan 2).

**2.** Mengapa `"abc"[10:]` tidak error?

??? success "Jawaban"
    Slicing menangani rentang di luar batas dengan mengembalikan hasil kosong.

## Ringkasan

Indeks mulai dari 0, slice `[a:b]` tidak menyertakan `b`, indeks negatif
menghitung dari belakang, dan indexing tunggal di luar rentang menimbulkan
galat sedangkan slicing tidak.

## Referensi

- Dokumentasi Python: *Common Sequence Operations* (<https://docs.python.org/3/library/stdtypes.html#common-sequence-operations>).

## Materi selanjutnya

[List, Tuple, Set, dan Dictionary](list-tuple-set-dict.md)
