# Variabel dan Tipe Data

## Tujuan pembelajaran

- [ ] Membuat variabel dan memilih tipe data yang sesuai (`str`, `int`, `float`, `bool`, `None`).
- [ ] Mengonversi antartipe dengan aman.
- [ ] Menjelaskan jebakan ketelitian bilangan desimal.

## Prasyarat

[Persiapan Python](../level-0-orientasi/persiapan-python.md) selesai dan Python dapat dijalankan.

## Pengantar dan intuisi

Variabel adalah **nama** yang menunjuk ke sebuah nilai. Tipe data menentukan
operasi yang boleh dilakukan: `"3" + "1"` menyambung teks, sedangkan `3 + 1`
menjumlah angka. Pada NLP, kesalahan tipe adalah galat sehari-hari, misalnya
kolom angka yang terbaca sebagai teks saat membaca CSV.

## Konsep

| Tipe | Contoh | Catatan |
|---|---|---|
| `str` | `"Jl. Melati"` | Teks; tak dapat diubah (immutable) |
| `int` | `3` | Bilangan bulat |
| `float` | `1.2` | Bilangan desimal, tidak selalu tepat |
| `bool` | `True` | Hasil perbandingan |
| `NoneType` | `None` | Menandai "tidak ada nilai" |

Nama variabel memakai `huruf_kecil_dengan_garis_bawah` dan sebaiknya
deskriptif: `jumlah_korban`, bukan `x`.

## Contoh kontekstual kebencanaan

Satu laporan: lokasi (teks), jumlah korban (bulat), tinggi air (desimal),
status darurat (boolean), dan catatan yang belum ada (`None`).

## Contoh kode

```python title="01_variabel_tipe_data.py" linenums="1"
--8<-- "level-1-python/01_variabel_tipe_data.py"
```

### Penjelasan kode

1. Lima variabel dibuat dengan tipe berbeda.
2. Perulangan `for` mencetak nama, nilai (`!r` menampilkan bentuk `repr`, jadi string diberi tanda kutip), dan nama tipe.
3. `int("12") + 1` mengonversi teks menjadi angka; `str(12) + "1"` menyambung dua teks.
4. `/` pembagian desimal, `//` pembagian bulat, `%` sisa bagi.
5. Baris terakhir membandingkan `0.1 + 0.2` dengan `0.3`.

### Output dan interpretasi

```text
lokasi         'Jl. Melati'   str
jumlah_korban  3              int
tinggi_air_m   1.2            float
darurat        True           bool
catatan        None           NoneType
13
121
3.5 3 1
False True
```

`0.1 + 0.2 == 0.3` bernilai `False` karena bilangan desimal disimpan dalam
biner dan hanya mendekati. Karena itu bandingkan `float` dengan pembulatan
atau toleransi (`math.isclose`), jangan dengan `==`.

## Kesalahan umum

- `"5" + 5` menimbulkan `TypeError`; konversi dulu salah satunya.
- Mengira `None` sama dengan `0` atau `""`; ketiganya berbeda.
- Memakai nama bawaan seperti `list` atau `str` sebagai nama variabel sehingga fungsi bawaan tertimpa.

## Latihan mandiri

1. Buat variabel untuk satu laporan banjir yang Anda karang, cetak tipenya.
2. Ubah `"120"` menjadi `int`, lalu bagi dua dengan `/` dan `//`. Apa bedanya?
3. Gunakan `math.isclose(0.1 + 0.2, 0.3)` dan jelaskan hasilnya.

## Kuis singkat

**1.** Tipe apa `None`, dan kapan dipakai?

??? success "Jawaban"
    `NoneType`; dipakai untuk menandai nilai yang belum ada atau tidak diketahui.

**2.** Mengapa `0.1 + 0.2 == 0.3` salah?

??? success "Jawaban"
    Representasi biner bilangan desimal tidak tepat; hasil penjumlahan hanya sangat dekat dengan 0.3.

## Ringkasan

Variabel menunjuk nilai bertipe. Pilih tipe yang benar, konversi dengan sadar,
dan jangan membandingkan `float` dengan `==`.

## Referensi

- Dokumentasi Python: *Built-in Types* (<https://docs.python.org/3/library/stdtypes.html>).

## Materi selanjutnya

[String dan Operasi Teks](string-operasi-teks.md)
