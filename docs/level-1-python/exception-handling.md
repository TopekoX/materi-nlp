# Exception Handling

## Tujuan pembelajaran

- [ ] Menangkap galat spesifik dengan `try/except`.
- [ ] Memakai `raise` untuk menolak masukan tidak valid.
- [ ] Menggunakan `finally` dan menghindari `except:` kosong.

## Prasyarat

[Import dan Modul](import-modul.md).

## Pengantar dan intuisi

Data nyata berantakan: file hilang, kolom kosong, angka yang ternyata teks.
*Exception* adalah cara Python menandai masalah. Menanganinya dengan baik
berarti program gagal **dengan pesan yang jelas** atau pulih secara sengaja,
bukan jatuh dengan jejak panjang atau, lebih buruk, diam-diam salah.

## Konsep

| Galat | Penyebab umum |
|---|---|
| `ValueError` | Nilai tak valid, mis. `int("abc")` |
| `TypeError` | Tipe salah, mis. `"a" + 1` |
| `KeyError` | Kunci dict tidak ada |
| `IndexError` | Indeks di luar rentang |
| `FileNotFoundError` | File tidak ditemukan |
| `ZeroDivisionError` | Pembagian nol |

Aturan praktis:

1. Tangkap **galat spesifik**, bukan `except Exception:` apalagi `except:` kosong.
2. Tangkap hanya bila Anda tahu cara menanganinya.
3. Gunakan `raise` untuk memvalidasi masukan di awal function.
4. `finally` selalu berjalan; cocok untuk pembersihan.

## Contoh kontekstual kebencanaan

Kolom `jumlah_korban` pada laporan kadang berisi "dua orang" alih-alih angka.
Fungsi konversi harus menanganinya tanpa menghentikan seluruh pemrosesan.

## Contoh kode

```python title="09_exception_handling.py" linenums="1"
--8<-- "level-1-python/09_exception_handling.py"
```

### Penjelasan kode

1. `ke_angka` mencoba `int(teks)` dan mengembalikan `None` bila `ValueError`.
2. Dua blok `try` memicu `KeyError` dan `ZeroDivisionError` dengan sengaja untuk memperlihatkan pesannya.
3. `finally` mencetak `selesai` apa pun hasilnya.
4. `rata_panjang` memakai `raise ValueError` bila daftar kosong, mencegah pembagian nol yang pesan galatnya kurang jelas.

### Output dan interpretasi

```text
12 None
KeyError: 'b'
ZeroDivisionError: division by zero
selesai
ValueError: daftar teks tidak boleh kosong
3.0
```

`dua belas` menjadi `None`: kita memutuskan sendiri nilai pengganti. Itu
keputusan desain, yang harus didokumentasikan; mengganti data tak valid
menjadi `None` tanpa jejak dapat menyembunyikan masalah data.

## Kesalahan umum

- `except:` kosong menelan semua galat, termasuk `KeyboardInterrupt`.
- Menangkap galat lalu `pass` tanpa mencatat.
- Menaruh terlalu banyak kode dalam `try` sehingga sumber galat tidak jelas.
- Mengembalikan nilai "ajaib" (-1, "") yang kemudian dianggap data valid.

## Latihan mandiri

1. Tulis `baca_angka_aman(teks, default=0)` yang mencatat (print) peringatan saat gagal.
2. Tangkap `FileNotFoundError` ketika membaca file yang tidak ada dan tampilkan pesan ramah.
3. Ganti `return None` pada `ke_angka` dengan `raise` bergaya Anda sendiri; kapan itu lebih baik?

## Kuis singkat

**1.** Mengapa `except:` kosong berbahaya?

??? success "Jawaban"
    Menelan semua galat, termasuk bug tak terduga, sehingga kegagalan tersembunyi.

**2.** Kapan blok `finally` dijalankan?

??? success "Jawaban"
    Selalu, baik ada galat maupun tidak.

## Ringkasan

Tangkap galat spesifik, validasi masukan dengan `raise`, dan jangan
menyembunyikan kegagalan data.

## Referensi

- Dokumentasi Python: *Errors and Exceptions* (<https://docs.python.org/3/tutorial/errors.html>).

## Materi selanjutnya

[Membaca dan Menulis File Teks](file-teks.md)
