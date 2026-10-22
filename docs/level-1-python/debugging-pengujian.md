# Debugging dan Pengujian Kode Sederhana

## Tujuan pembelajaran

- [ ] Membaca *traceback* dari bawah ke atas.
- [ ] Menemukan bug dengan `print`, `assert`, dan debugger.
- [ ] Menulis tes sederhana dengan `assert` dan `pytest`.

## Prasyarat

[Dasar Regex](regex-dasar.md) dan [Function dan Parameter](function-parameter.md).

## Pengantar dan intuisi

Bug tidak dapat dihindari, tetapi dapat ditemukan lebih cepat dengan
kebiasaan baik: baca pesan galat, kecilkan masalah, dan tulis tes yang
membuktikan perbaikan. Pada pipeline preprocessing, tes kecil mencegah
perubahan satu aturan merusak aturan lain secara diam-diam.

## Konsep

### Membaca traceback

```text
Traceback (most recent call last):
  File "proyek.py", line 12, in <module>
    hasil = rata_panjang([])
  File "proyek.py", line 5, in rata_panjang
    return sum(...) / len(daftar)
ZeroDivisionError: division by zero
```

Baca **baris terakhir** (jenis dan pesan galat) dulu, lalu naik ke baris kode
yang menyebabkannya.

### Strategi debugging

1. **Reproduksi** galat dengan contoh sekecil mungkin.
2. **Hipotesis**: apa yang Anda kira terjadi?
3. **Periksa**: `print(repr(nilai))`, `type(nilai)`, atau `breakpoint()`.
4. **Perbaiki** satu hal, jalankan ulang.
5. **Tulis tes** agar bug tidak kembali.

### Pengujian

- `assert kondisi, "pesan"` menghentikan program bila kondisi salah.
- `pytest` menjalankan semua function berawalan `test_` dan melaporkan ringkasannya.
- Uji kasus normal, kasus tepi (string kosong, spasi ganda), dan kasus galat.

## Contoh kontekstual kebencanaan

`hitung_kata` kelihatan sepele, tetapi bagaimana dengan teks kosong atau
spasi berlebih? Tes pertama menjawabnya dan melindungi saat fungsi diubah.

## Contoh kode

```python title="16_debugging_pengujian.py" linenums="1"
--8<-- "level-1-python/16_debugging_pengujian.py"
```

### Penjelasan kode

1. `tes_hitung_kata` berisi tiga `assert`: kasus normal, string kosong, dan spasi berlebih.
2. Blok `__main__` menjalankan tes dan mencetak keberhasilan.
3. `assert ... == 3, "seharusnya 2 kata"` sengaja salah untuk memperlihatkan `AssertionError` dengan pesan.

### Output dan interpretasi

```text
semua tes lolos
AssertionError: seharusnya 2 kata
```

Tiga tes lolos berarti function benar untuk **tiga kasus itu saja**, bukan
terbukti benar untuk semua masukan. Tes memperkecil risiko, bukan
menghilangkannya. Untuk tes dengan `pytest`, pindahkan function ke berkas
`test_*.py`, lalu jalankan `pytest`.

## Kesalahan umum

- Mengabaikan pesan galat dan langsung menebak.
- Mengubah banyak hal sekaligus sehingga tidak tahu perubahan mana yang menolong.
- Memakai `print` tanpa `repr` sehingga spasi/karakter tak terlihat tersembunyi.
- Hanya menguji kasus yang mudah.

## Latihan mandiri

1. Buat bug sengaja di `hitung_kata` (mis. `split(" ")`) dan lihat tes mana yang gagal.
2. Tambah tes untuk teks berisi tab dan baris baru.
3. Pindahkan tes ke `test_hitung.py`, pasang `pytest`, dan jalankan.

## Kuis singkat

**1.** Bagian traceback mana yang dibaca lebih dulu?

??? success "Jawaban"
    Baris terakhir, karena menyebut jenis dan pesan galat.

**2.** Mengapa menguji teks kosong?

??? success "Jawaban"
    Kasus tepi sering memicu bug yang tidak terlihat pada kasus normal.

## Ringkasan

Debugging = reproduksi, hipotesis, periksa, perbaiki, uji. Tes kecil dengan
kasus tepi menjaga kode tetap benar saat berubah.

## Referensi

- Dokumentasi Python: *Debugging and profiling* dan `unittest`.
- Dokumentasi pytest: <https://docs.pytest.org/>.

## Materi selanjutnya

Setelah halaman NumPy, pandas, dan missing values selesai, lanjut ke [Level 2](../level-2-fondasi-teks/index.md).
