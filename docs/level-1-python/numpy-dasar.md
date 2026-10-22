# Dasar NumPy

## Tujuan pembelajaran

- [ ] Membuat array NumPy dan membaca `shape`, `dtype`.
- [ ] Melakukan operasi vektor, agregasi per sumbu, dan penyaringan boolean.
- [ ] Menghubungkan array dengan representasi teks (vektor dan matriks fitur).

## Prasyarat

[Perulangan](perulangan.md) dan `numpy` terpasang (`pip install -r requirements-ml.txt`).

## Pengantar dan intuisi

Model ML bekerja pada angka, dan NumPy adalah fondasi komputasi numerik di
Python. Sebuah dokumen akan menjadi **vektor** (array 1 dimensi), dan seluruh
korpus menjadi **matriks** (baris = dokumen, kolom = fitur). NumPy
melakukan operasi pada seluruh array sekaligus (*vectorized*), jauh lebih
cepat daripada perulangan Python.

## Konsep

| Konsep | Arti |
|---|---|
| `ndarray` | Array berdimensi banyak dengan satu tipe data |
| `shape` | Ukuran tiap dimensi, mis. `(2, 3)` = 2 baris, 3 kolom |
| `dtype` | Tipe elemen (`int64`, `float64`, ...) |
| *broadcasting* | Operasi skalar/array kecil diterapkan ke seluruh array |
| `axis=0` / `axis=1` | Agregasi sepanjang kolom / baris |
| `a @ b` | Perkalian matriks / dot product |

Operasi `panjang * 2` berlaku untuk tiap elemen. Penyaringan boolean
`panjang[panjang > 4]` mengambil elemen yang memenuhi syarat.

## Contoh kontekstual kebencanaan

Panjang empat postingan (dalam kata) menjadi vektor. Matriks kecil `m`
mewakili 2 dokumen × 3 kata (jumlah kemunculan), persis bentuk *bag of
words* di Level 3. Dot product dua vektor biner menghitung jumlah kata yang
sama.

## Contoh kode

```python title="12_numpy_dasar.py" linenums="1"
--8<-- "level-1-python/12_numpy_dasar.py"
```

### Penjelasan kode

1. `np.array([...])` membuat vektor; `.dtype` dan `.shape` menjelaskan isinya.
2. `mean`, `max`, `std` adalah agregasi; `panjang * 2` dan `panjang[panjang > 4]` memakai broadcasting dan penyaringan boolean.
3. `m.sum(axis=0)` menjumlah tiap kolom, `axis=1` tiap baris. `m.T` transpos. `(m == 0).mean()` adalah proporsi elemen nol, intuisi dasar **sparsity**.
4. `a @ b` adalah dot product; `np.linalg.norm(a)` panjang vektor.
5. `np.arange` dan `np.zeros` membuat array.

### Output dan interpretasi

Output nyata (NumPy 2.5.4):

```text
[6 5 4 3] int64 (4,)
4.5 6 1.118
[12 10  8  6] [6 5]
(2, 3) [1 3 2] [3 3]
(3, 2) 0.5
1 1.414
[0.   0.25 0.5  0.75] [[0 0]
 [0 0]]
```

- Rata-rata panjang 4,5 kata; simpangan baku populasi 1,118.
- Jumlah per kolom `[1 3 2]` dan per baris `[3 3]`.
- Setengah elemen matriks bernilai nol (`0.5`). Pada korpus nyata dengan puluhan ribu kata, proporsi nol bisa >99%, itulah alasan *sparse matrix* dipakai.
- `a @ b = 1`: kedua vektor sama-sama 1 hanya pada posisi pertama. `norm(a) = √2 ≈ 1.414`.

## Kesalahan umum

- Mencampur `axis=0` dan `axis=1`.
- Mengira `a * b` adalah perkalian matriks (itu perkalian per elemen; matriks memakai `@`).
- Mengubah tampilan (*view*) array dan tak sengaja mengubah aslinya.
- Menyimpulkan `std` sampel: NumPy default memakai `ddof=0` (populasi).

## Latihan mandiri

1. Buat array panjang 5 postingan dan hitung rata-rata serta persentase yang lebih panjang dari rata-rata.
2. Untuk `m` di atas, hitung jumlah kata per dokumen (`axis=1`) dan dokumen mana yang paling banyak kata.
3. Hitung *cosine similarity* dua vektor `a` dan `b`: `(a @ b) / (norm(a) * norm(b))`.

## Kuis singkat

**1.** `shape` dari `np.zeros((2, 3))`?

??? success "Jawaban"
    `(2, 3)`.

**2.** Apa arti `axis=0` pada `sum`?

??? success "Jawaban"
    Menjumlahkan sepanjang baris, menghasilkan satu nilai per kolom.

## Ringkasan

NumPy menyediakan array bertipe tunggal dan operasi vektor. Matriks
dokumen×fitur dan ukuran seperti jarak/kemiripan semuanya dibangun di atasnya.

## Referensi

- Dokumentasi NumPy: *NumPy quickstart* (<https://numpy.org/doc/stable/user/quickstart.html>).

## Materi selanjutnya

[Dasar pandas](pandas-dasar.md)
