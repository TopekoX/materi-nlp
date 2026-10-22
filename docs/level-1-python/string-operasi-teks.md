# String dan Operasi Teks

## Tujuan pembelajaran

- [ ] Memakai metode string yang paling sering muncul pada NLP.
- [ ] Menjelaskan bahwa string bersifat immutable.
- [ ] Membangun string dengan f-string dan `join`.

## Prasyarat

[Variabel dan Tipe Data](variabel-tipe-data.md).

## Pengantar dan intuisi

NLP dimulai dari string. Hampir semua preprocessing (menghapus spasi,
menyeragamkan huruf, memecah kata) adalah rangkaian operasi string. Memahami
metode bawaannya menghemat banyak kode.

## Konsep

| Operasi | Metode | Catatan |
|---|---|---|
| Huruf kecil / besar | `lower()`, `upper()` | Basis *case folding* |
| Hapus spasi tepi | `strip()` | `lstrip`, `rstrip` untuk satu sisi |
| Pecah kata | `split()` | Tanpa argumen: pecah di spasi apa pun |
| Gabung | `" ".join(daftar)` | Kebalikan `split` |
| Ganti | `replace(a, b)` | Mengembalikan string **baru** |
| Cek | `in`, `startswith`, `endswith`, `find` | `find` mengembalikan `-1` bila tak ada |

String tidak bisa diubah: setiap metode menghasilkan string baru, sedangkan
yang lama tetap. Karena itu hasilnya harus ditampung: `teks = teks.lower()`.

## Contoh kontekstual kebencanaan

Postingan `"  TOLONG!! Banjir di Jl. Melati, air naik cepat  "` memiliki spasi
tepi, huruf kapital, dan tanda seru berulang. Setiap operasi di bawah
menghilangkan satu sumber variasi.

## Contoh kode

```python title="02_string_operasi_teks.py" linenums="1"
--8<-- "level-1-python/02_string_operasi_teks.py"
```

### Penjelasan kode

1. `strip()` menghapus spasi di awal dan akhir. `repr` menampilkan tanda kutipnya.
2. `lower().strip()` merangkai dua operasi.
3. `split()` memecah menjadi list kata; tanda baca ikut menempel pada kata.
4. `replace("!!", "!")` mengganti substring.
5. `len` sebelum dan sesudah `strip` membandingkan panjang.
6. `" ".join(kata)` menyatukan list menjadi satu string; f-string menyisipkan nilai.

### Output dan interpretasi

```text
'TOLONG!! Banjir di Jl. Melati, air naik cepat'
tolong!! banjir di jl. melati, air naik cepat
['TOLONG!!', 'Banjir', 'di', 'Jl.', 'Melati,', 'air', 'naik', 'cepat']
True
TOLONG! Banjir di Jl. Melati, air naik cepat
49 45
banjir naik cepat
Lokasi: 'Melati', panjang nama: 6
True True 3
```

Perhatikan token `'TOLONG!!'` dan `'Melati,'`: `split()` tidak memisahkan
tanda baca. Inilah alasan tokenisasi yang layak (Level 2) butuh lebih dari
`split()`. Selisih panjang 49 vs 45 adalah 4 spasi di tepi.

## Kesalahan umum

- Memanggil `teks.lower()` tanpa menampung hasilnya.
- Menggunakan `split(" ")` sehingga spasi ganda menghasilkan elemen kosong.
- Membangun string panjang dengan `+` di dalam perulangan; gunakan `join`.
- Mengira `find` mengembalikan boolean.

## Latihan mandiri

1. Tulis kode yang mengubah `"  GEMPA!!  terasa  kuat  "` menjadi `"gempa!! terasa kuat"`.
2. Bandingkan `"a  b".split()` dengan `"a  b".split(" ")`.
3. Hitung berapa kali `"banjir"` muncul dalam kalimat dengan dua cara.

## Kuis singkat

**1.** Mengapa `teks.upper()` saja tidak mengubah `teks`?

??? success "Jawaban"
    String immutable; metode mengembalikan string baru yang harus ditampung.

**2.** Apa hasil `"-".join(["a", "b"])`?

??? success "Jawaban"
    `"a-b"`.

## Ringkasan

Metode string adalah alat utama preprocessing dasar. `split()` sederhana tetapi
tidak memisahkan tanda baca.

## Referensi

- Dokumentasi Python: *String Methods* (<https://docs.python.org/3/library/stdtypes.html#string-methods>).

## Materi selanjutnya

[Indexing dan Slicing](indexing-slicing.md)
