# Dasar pandas

## Tujuan pembelajaran

- [ ] Memuat CSV ke `DataFrame` dan memeriksa bentuk serta tipenya.
- [ ] Memilih kolom, memfilter baris, dan menambah kolom turunan.
- [ ] Menghitung distribusi label dan statistik per kelompok.

## Prasyarat

[CSV dan JSON](csv-json.md) dan [Dasar NumPy](numpy-dasar.md).

## Pengantar dan intuisi

`pandas` adalah "spreadsheet yang diprogram". `DataFrame` adalah tabel
berkolom bernama; `Series` adalah satu kolom. Hampir seluruh analisis
dataset teks dimulai dengan `pd.read_csv` dan beberapa baris pemeriksaan.

## Konsep

| Operasi | Kode |
|---|---|
| Baca CSV | `pd.read_csv(jalur)` |
| Ukuran / tipe | `df.shape`, `df.dtypes` |
| Lihat awal | `df.head(n)` |
| Pilih kolom | `df["teks"]`, `df[["id", "label"]]` |
| Filter | `df[df["label"] == "Emergency"]` |
| Hitung kategori | `df["label"].value_counts()` |
| Operasi string | `df["teks"].str.split()`, `.str.lower()` |
| Kolom baru | `df["jumlah_kata"] = ...` |
| Per kelompok | `df.groupby("label")["jumlah_kata"].mean()` |

!!! note "Versi pandas"
    Output di bawah dari pandas 3.1.0, yang menampilkan kolom teks sebagai
    tipe `str`. Pada pandas 2.x kolom yang sama tampil sebagai `object`.
    Konsep dan kodenya sama.

## Contoh kontekstual kebencanaan

Memuat `laporan_contoh.csv` (10 laporan sintetis), menghitung distribusi
label, menambah jumlah kata per laporan, dan membandingkan rata-rata per kelas.

## Contoh kode

```python title="13_pandas_dasar.py" linenums="1"
--8<-- "level-1-python/13_pandas_dasar.py"
```

### Penjelasan kode

1. `pd.set_option` hanya mengatur lebar tampilan agar tabel tidak terpotong.
2. `read_csv` memuat berkas; `shape` dan `dtypes` memeriksa ukuran dan tipe.
3. `head(3)` menampilkan tiga baris pertama.
4. `value_counts()` menghitung jumlah per label.
5. `df["teks"].str.split().str.len()` memecah tiap teks menjadi kata dan menghitungnya; hasilnya kolom baru.
6. Filter boolean memilih lokasi laporan Emergency; `groupby` menghitung rata-rata per label.

### Output dan interpretasi

```text
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
label
Emergency        5
Non-Emergency    5
Name: count, dtype: int64
   id  jumlah_kata
0   1          8.0
1   2          6.0
2   3          8.0
['Jakarta', 'Surabaya', 'Padang', 'Medan', 'Bekasi']
label
Emergency        7.00
Non-Emergency    6.25
Name: jumlah_kata, dtype: float64
```

- `id` terbaca `int64`, tidak seperti `csv.DictReader` (string).
- Kelas seimbang (5 vs 5) hanya karena ini data demonstrasi; data nyata biasanya tidak seimbang.
- `jumlah_kata` bertipe **float** (`8.0`), bukan integer. Ini isyarat bahwa ada nilai kosong (`NaN`) di kolom `teks`: baris 9 tidak punya teks. Halaman berikutnya membahasnya.
- Rata-rata 7,00 vs 6,25 kata dihitung dari 10 baris saja; **tidak boleh** disimpulkan bahwa laporan darurat lebih panjang.

## Kesalahan umum

- `df[df["a"] == 1 and df["b"] == 2]` salah; gunakan `&` dengan tanda kurung: `df[(df["a"] == 1) & (df["b"] == 2)]`.
- Mengubah salinan sementara dan mengira `df` berubah.
- Mengabaikan `dtypes` yang menandakan masalah data.
- Menarik kesimpulan statistik dari sampel yang sangat kecil.

## Latihan mandiri

1. Tampilkan hanya `id` dan `teks` untuk laporan di `Jakarta`.
2. Tambahkan kolom `panjang_karakter` dan urutkan menurun dengan `sort_values`.
3. Hitung distribusi lokasi dengan `value_counts()`; apa yang terjadi pada nilai kosong?

## Kuis singkat

**1.** Mengapa kolom `jumlah_kata` bertipe float?

??? success "Jawaban"
    Karena ada `NaN` pada `teks`; integer biasa tidak dapat menyimpan nilai kosong, jadi pandas memakai float.

**2.** Bagaimana memilih dua kolom sekaligus?

??? success "Jawaban"
    Dengan daftar nama kolom: `df[["id", "label"]]`.

## Ringkasan

`DataFrame` memuat tabel dataset; kebiasaan awal: `shape`, `dtypes`, `head`,
`value_counts`. Tipe tak terduga sering menandakan data kosong.

## Referensi

- Dokumentasi pandas: *10 minutes to pandas* (<https://pandas.pydata.org/docs/user_guide/10min.html>).

## Materi selanjutnya

[Missing Values dan Duplikasi Data](missing-values-duplikasi.md)
