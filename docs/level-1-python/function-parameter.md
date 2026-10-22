# Function dan Parameter

## Tujuan pembelajaran

- [ ] Mendefinisikan function dengan parameter posisi, kata kunci, dan nilai default.
- [ ] Mengembalikan beberapa nilai dan membongkarnya.
- [ ] Menghindari jebakan *mutable default argument*.

## Prasyarat

[Perulangan](perulangan.md).

## Pengantar dan intuisi

Function membungkus langkah yang dipakai berulang menjadi satu nama. Pada
NLP, setiap langkah preprocessing sebaiknya berupa function kecil yang
melakukan satu hal, sehingga dapat diuji dan dirangkai (Level 2).

## Konsep

- `def nama(parameter): ... return nilai`.
- Parameter **posisi**: `f(a, b)`; **kata kunci**: `f(a=1)`; **default**: `def f(a, b=2)`.
- Tanda `*` di daftar parameter memaksa parameter sesudahnya diberikan dengan nama (*keyword-only*).
- `return` tanpa nilai atau tanpa `return` menghasilkan `None`.
- Beberapa nilai dikembalikan sebagai tuple dan dapat dibongkar.
- Docstring (string tiga kutip di awal function) mendokumentasikan tujuannya.

!!! danger "Jangan memakai list/dict kosong sebagai default"
    `def f(item, daftar=[])` membuat satu list yang **dipakai bersama** di
    semua pemanggilan. Gunakan `daftar=None` lalu buat list baru di dalam function.

## Contoh kontekstual kebencanaan

Menghitung kemunculan kata di postingan, meringkas teks panjang untuk
pratinjau, dan menghitung statistik panjang teks.

## Contoh kode

```python title="07_function_parameter.py" linenums="1"
--8<-- "level-1-python/07_function_parameter.py"
```

### Penjelasan kode

1. `hitung_kemunculan` memiliki parameter default `huruf_kecil=True` dan docstring.
2. `ringkas` memakai `*` sehingga `maks` hanya bisa dipanggil sebagai `maks=10`.
3. `statistik` mengembalikan tuple tiga nilai yang dibongkar saat dipanggil.
4. `tambah` memperlihatkan pola yang benar untuk argumen default berupa list.

### Output dan interpretasi

```text
3
1
Banjir setinggi dada...
Banjir set...
3 5 4.0
[1] [2]
```

Dengan `huruf_kecil=True`, `"Banjir banjir BANJIR"` menghasilkan 3 kemunculan;
dengan `False`, hanya 1 yang persis `banjir`. Satu parameter mengubah hasil
secara bermakna, alasan mengapa pilihan *case folding* harus dicatat dalam
eksperimen. `tambah(1)` dan `tambah(2)` masing-masing mendapat list baru
(`[1]`, `[2]`); dengan default `[]` hasil kedua akan menjadi `[1, 2]`.

## Kesalahan umum

- Lupa `return` sehingga hasilnya `None`.
- Default mutable.
- Function melakukan terlalu banyak hal (membersihkan, menghitung, dan mencetak sekaligus).
- Mengubah argumen masukan tanpa memberi tahu pemanggil.

## Latihan mandiri

1. Tulis `hapus_url(teks)` yang mengganti URL dengan `"<URL>"` (petunjuk: halaman regex).
2. Tambahkan docstring dan nilai default pada function buatan Anda.
3. Tulis function yang mengembalikan `(jumlah_kata, jumlah_karakter)`.

## Kuis singkat

**1.** Apa hasil function tanpa pernyataan `return`?

??? success "Jawaban"
    `None`.

**2.** Mengapa `daftar=None` lebih aman daripada `daftar=[]` sebagai default?

??? success "Jawaban"
    Default dievaluasi sekali saat definisi; list bersama akan terakumulasi lintas pemanggilan.

## Ringkasan

Function kecil, bernama jelas, dengan docstring dan default yang aman adalah
fondasi pipeline NLP yang dapat diuji.

## Referensi

- Dokumentasi Python: *Defining Functions* (<https://docs.python.org/3/tutorial/controlflow.html#defining-functions>).

## Materi selanjutnya

[Import dan Modul](import-modul.md)
