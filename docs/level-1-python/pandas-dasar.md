# Dasar pandas

!!! abstract "Info materi"
    **Tingkat kesulitan:** Menengah. **Estimasi waktu:** 120 menit.
    **Jenis kode:** snippet edukatif (`examples/level-1-python/13_pandas_dasar.py`) dengan data sintetis `data/laporan_contoh.csv`. Memerlukan `pandas` (versi pada mesin penulis: pandas 3.1; tampilan tipe berbeda pada pandas 2).

## Tujuan pembelajaran

- [ ] Membaca CSV menjadi `DataFrame` dan memeriksa `shape`, `dtypes`, dan `head`.
- [ ] Memilih kolom dan baris dengan `[]`, `loc`, `iloc`, dan penyaringan boolean.
- [ ] Membuat kolom baru dan memakai metode `.str`.
- [ ] Meringkas dengan `value_counts` dan `groupby`.
- [ ] Menjelaskan mengapa kolom bisa berubah tipe karena nilai kosong.

## Prasyarat

[NumPy dasar](numpy-dasar.md), [CSV dan JSON](csv-json.md), dan [Dictionary](list-tuple-set-dict.md).

## Pengantar dan motivasi

Dataset teks adalah tabel: satu baris per postingan, kolom untuk teks dan label. pandas menyediakan tabel
bernama kolom (`DataFrame`) dengan operasi tingkat tinggi: menyaring, mengelompokkan, dan menghitung tanpa
perulangan manual. Seluruh EDA di [Level 3](../level-3-representasi-teks/statistik-korpus.md) memakai pandas.

## Konsep dasar

- **`DataFrame`**: tabel dua dimensi dengan nama kolom dan indeks baris.
- **`Series`**: satu kolom (atau satu baris) dari `DataFrame`.

| Operasi | Fungsi |
|---|---|
| `pd.read_csv(path)` | Membaca CSV, menebak tipe kolom |
| `df.shape`, `df.dtypes` | Ukuran dan tipe kolom |
| `df.head(n)` | `n` baris pertama |
| `df["kolom"]` | Satu kolom (`Series`) |
| `df[["a", "b"]]` | Beberapa kolom (`DataFrame`) |
| `df[df["x"] == nilai]` | Penyaringan baris |
| `df.loc[baris, kolom]` | Akses berdasarkan **label** |
| `df.iloc[i, j]` | Akses berdasarkan **posisi** |
| `df.groupby(k)[v].mean()` | Ringkasan per kelompok |

## Penjelasan mendalam

### Tipe kolom ditebak, bukan dijamin

`read_csv` menebak tipe tiap kolom. Kolom `id` terbaca `int64` (berbeda dari modul `csv` yang menghasilkan string). Kolom
teks terbaca sebagai `str` (pandas 3) atau `object` (pandas 2). Jika kolom angka memiliki sel kosong, pandas
mengubahnya menjadi `float` karena nilai kosong (`NaN`) bertipe `float` (Bagian 3).

### `loc` versus `iloc`

`loc` memakai **label** (nama kolom, label indeks), `iloc` memakai **posisi** (nomor). Pada data baru keduanya sama
untuk baris, tetapi menjadi berbeda setelah menyaring atau mengurutkan; pilih yang sesuai maksud.

### Penyaringan boolean dan tanda kurung

Beberapa syarat digabung dengan `&` (dan), `|` (atau), `~` (tidak), dan **setiap syarat harus diberi tanda kurung**:
`(df["a"] == 1) & (df["b"] > 2)`. Memakai `and`/`or` Python menimbulkan galat atau hasil salah.

### Vektorisasi pada kolom

`df["teks"].str.split().str.len()` menerapkan operasi string ke **seluruh kolom** sekaligus; tidak perlu perulangan `for`.
Metode `.str` melewati nilai kosong dan menghasilkan `NaN` untuknya.

### Salinan dan tampilan

Penyaringan menghasilkan DataFrame baru; menugaskan kolom baru pada DataFrame hasil saringan dapat memicu peringatan
`SettingWithCopyWarning`. Bila ingin mengubah hasil saringan secara mandiri, buat salinan dengan `.copy()`.

## Cara kerja atau alur proses

```mermaid
flowchart LR
    C["laporan_contoh.csv"] -- "read_csv" --> D["DataFrame"]
    D -- "kolom baru" --> D2["+ jumlah_kata"]
    D2 -- "saring / groupby" --> H["ringkasan"]
```

## Contoh sederhana

```python
import pandas as pd
df = pd.DataFrame({"kata": ["air", "api"], "n": [3, 5]})
df[df["n"] > 4]          # baris dengan n > 4
```

## Contoh dalam konteks Twitter/X kebencanaan

Sepuluh laporan sintetis (id, teks, label, lokasi). Kita ingin tahu: berapa laporan per label, lokasi laporan
Emergency, dan apakah laporan Emergency lebih panjang daripada Non-Emergency.

## Praktik Python

Berkas: `examples/level-1-python/13_pandas_dasar.py`. Baris `pd.set_option(...)` hanya mengatur lebar tampilan agar tabel tidak terpotong.

### Bagian 1 — Membaca dan memeriksa

```python title="Bagian 1"
--8<-- "level-1-python/13_pandas_dasar.py:baca"
```

```text title="Output nyata"
(10, 4)
id        int64
teks        str
label       str
lokasi      str
dtype: object
   id                                     teks          label    lokasi
0   1  Banjir setinggi dada di Jl. Melati m...      Emergency   Jakarta
1   2  Pelatihan mitigasi gempa digelar bes...  Non-Emergency   Bandung
2   3  Rumah terbakar di RT 05 tolong kirim...      Emergency  Surabaya
```

Interpretasi: 10 baris dan 4 kolom. `id` bertipe `int64`; kolom teks tampil sebagai `str`. `head(3)` menampilkan tiga baris pertama; teks panjang dipotong dengan `...` (hanya tampilan, datanya utuh).

### Bagian 2 — Memilih kolom dan menghitung kategori

```python title="Bagian 2"
--8<-- "level-1-python/13_pandas_dasar.py:kolom"
```

```text title="Output nyata"
Series DataFrame
label
Emergency        5
Non-Emergency    5
Name: count, dtype: int64
```

Interpretasi: satu kolom dalam kurung siku tunggal adalah `Series`; daftar kolom menghasilkan `DataFrame`. `value_counts()` menunjukkan 5 laporan per label (seimbang pada data kecil ini).

### Bagian 3 — Kolom baru dan nilai kosong

```python title="Bagian 3"
--8<-- "level-1-python/13_pandas_dasar.py:kolom_baru"
```

`str.split()` memecah tiap teks menjadi daftar kata; `str.len()` menghitung panjang tiap daftar.

```text title="Output nyata"
   id  jumlah_kata
0   1          8.0
1   2          6.0
2   3          8.0
```

Interpretasi: jumlah kata sebenarnya bilangan bulat, tetapi tampil `8.0` (desimal). Penyebabnya: baris dengan id 9 memiliki teks **kosong** (`NaN`), sehingga jumlah katanya `NaN`, dan kolom `float` diperlukan untuk menampung `NaN`. Ini petunjuk bahwa ada nilai kosong yang harus ditangani (halaman berikutnya).

### Bagian 4 — Menyaring baris

```python title="Bagian 4"
--8<-- "level-1-python/13_pandas_dasar.py:saring"
```

```text title="Output nyata"
['Jakarta', 'Surabaya', 'Padang', 'Medan', 'Bekasi']
[1, 3, 5]
```

Interpretasi: baris pertama mengambil lokasi laporan Emergency. Baris kedua memakai dua syarat dengan tanda kurung dan `&`: laporan Emergency yang lebih dari 6 kata memiliki id 1, 3, 5.

### Bagian 5 — Mengelompokkan

```python title="Bagian 5"
--8<-- "level-1-python/13_pandas_dasar.py:groupby"
```

```text title="Output nyata"
label
Emergency        7.00
Non-Emergency    6.25
Name: jumlah_kata, dtype: float64
```

Interpretasi: rata-rata jumlah kata laporan Emergency 7,00 dan Non-Emergency 6,25. Baris dengan teks kosong tidak dihitung (rata-rata mengabaikan `NaN`), sehingga rata-rata Non-Emergency dihitung dari empat baris. Ini data sintetis kecil, tidak mewakili apa pun tentang pesan darurat nyata.

### Bagian 6 — Galat nama kolom dan `loc`/`iloc`

```python title="Bagian 6"
--8<-- "level-1-python/13_pandas_dasar.py:galat"
```

```text title="Output nyata"
KeyError: 'teks_laporan'
Banjir setinggi dada di Jl. Melati mohon evakuasi
True
```

Interpretasi: nama kolom yang salah menimbulkan `KeyError`. `df.loc[0, "teks"]` (label) dan `df.iloc[0, 1]` (posisi baris 0, kolom 1) mengambil sel yang sama.

### Skrip terpadu

Keenam bagian adalah satu skrip: `13_pandas_dasar.py`.

## Kesalahan umum dan debugging

| Gejala | Penyebab | Perbaikan |
|---|---|---|
| `KeyError: 'nama_kolom'` | Nama kolom salah (huruf besar, spasi) | `print(df.columns.tolist())` |
| `ValueError: The truth value of a Series is ambiguous` | Memakai `and`/`or` pada kolom | `&`, `\|` dengan tanda kurung |
| Kolom angka berubah menjadi `float` | Ada nilai kosong | Periksa `df.isna().sum()` |
| `SettingWithCopyWarning` | Mengubah hasil saringan | `.copy()` |
| Hasil `head()` terpotong tampilannya | Lebar tampilan terbatas | `pd.set_option("display.max_colwidth", ...)` |
| Hasil berbeda antar-versi pandas | Perilaku `str` vs `object` | Catat versi pandas |

## Kelebihan dan keterbatasan

**Kelebihan:** ekspresif dan ringkas untuk data tabular; ekosistem luas; terintegrasi dengan scikit-learn. **Keterbatasan:** memuat seluruh data
ke memori; perilaku berubah antarversi; operasi `.str` pada teks sangat besar bisa lambat dibanding pemrosesan khusus.

## Latihan bertahap

1. **Konseptual.** Apa beda `Series` dan `DataFrame`?
2. **Membaca kode.** Apa hasil `df["label"].value_counts()` pada data ini?
3. **Mengisi kode.** Lengkapi: `df[df["lokasi"] == ___]` agar memilih laporan dari Jakarta.
4. **Debugging.** `df[df["label"] == "Emergency" & df["jumlah_kata"] > 6]` menimbulkan galat. Mengapa, dan apa perbaikannya?
5. **Program kecil.** Hitung jumlah laporan per lokasi (`value_counts`) dan tampilkan lokasi yang muncul lebih dari sekali.

## Kunci jawaban dan pembahasan

??? success "Jawaban 1"
    `Series` adalah satu kolom (satu dimensi); `DataFrame` adalah tabel berisi beberapa `Series` berkolom nama.

??? success "Jawaban 2"
    `Emergency` 5 dan `Non-Emergency` 5.

??? success "Jawaban 3"
    `"Jakarta"`: `df[df["lokasi"] == "Jakarta"]` menghasilkan baris dengan id 1 dan 4.

??? success "Jawaban 4"
    Operator `&` memiliki prioritas lebih tinggi daripada `==` dan `>`, sehingga ekspresi dievaluasi dalam urutan keliru. Beri tanda kurung: `df[(df["label"] == "Emergency") & (df["jumlah_kata"] > 6)]`.

??? success "Jawaban 5"
    ```python
    hitung = df["lokasi"].value_counts()
    print(hitung[hitung > 1])
    ```
    Pada data ini `Jakarta` (id 1 dan 4) dan `Bandung` (id 2 dan 8) masing-masing muncul dua kali; lokasi lain sekali. Baris dengan lokasi kosong (id 6) tidak dihitung oleh `value_counts`.

## Kuis singkat

**1.** Apa fungsi `df.head(3)`?

??? success "Jawaban"
    Menampilkan tiga baris pertama.

**2.** Mengapa `jumlah_kata` tampil sebagai `8.0`?

??? success "Jawaban"
    Ada nilai kosong (`NaN`) di kolom itu, sehingga pandas memakai tipe `float`.

**3.** Apa beda `loc` dan `iloc`?

??? success "Jawaban"
    `loc` memakai label; `iloc` memakai posisi.

## Ringkasan

- `DataFrame` adalah tabel bernama kolom; `read_csv` menebak tipe.
- Pilih dengan `[]`, `loc`, `iloc`, dan saringan boolean (dengan tanda kurung).
- `.str` untuk operasi teks pada kolom; `value_counts` dan `groupby` untuk ringkasan.
- Nilai kosong mengubah tipe kolom menjadi `float`.

## Glosarium istilah baru

DataFrame
:   Tabel dua dimensi berkolom nama.

Series
:   Satu kolom atau baris dari DataFrame.

Indeks
:   Label baris DataFrame.

`NaN`
:   Nilai kosong numerik (*not a number*).

Penyaringan boolean
:   Memilih baris berdasarkan syarat `True/False`.

## Referensi

- Dokumentasi pandas, *10 minutes to pandas*: <https://pandas.pydata.org/docs/user_guide/10min.html> (dokumentasi resmi).
- Dokumentasi pandas, *Indexing and selecting data*: <https://pandas.pydata.org/docs/user_guide/indexing.html> (dokumentasi resmi).

## Materi selanjutnya

[Missing Values dan Duplikasi Data](missing-values-duplikasi.md)
