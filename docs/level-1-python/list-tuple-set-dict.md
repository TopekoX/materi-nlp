# List, Tuple, Set, dan Dictionary

## Tujuan pembelajaran

- [ ] Memilih struktur data yang tepat untuk kasus tertentu.
- [ ] Menghitung frekuensi kata dengan dictionary.
- [ ] Menggunakan set untuk mencari kata unik dan irisan.

## Prasyarat

[Indexing dan Slicing](indexing-slicing.md).

## Pengantar dan intuisi

Teks jarang berdiri sendiri. Kita mengelola **kumpulan**: daftar kata, himpunan
kosakata, kamus normalisasi. Empat struktur data bawaan Python menutup
hampir semua kebutuhan awal.

## Konsep

| Struktur | Berurutan | Bisa diubah | Duplikat | Cocok untuk |
|---|---|---|---|---|
| `list` | ya | ya | boleh | Urutan token, kumpulan dokumen |
| `tuple` | ya | tidak | boleh | Pasangan tetap, mis. `(teks, label)` |
| `set` | tidak | ya | tidak | Kosakata unik, uji keanggotaan cepat |
| `dict` | ya (urutan sisip) | ya | kunci unik | Pemetaan, mis. kata → frekuensi |

`dict.get(kunci, default)` menghindari `KeyError`. Uji `x in set` jauh lebih
cepat daripada `x in list` untuk koleksi besar, alasan stopwords biasanya
disimpan sebagai set.

## Contoh kontekstual kebencanaan

Membuat kosakata unik dari kumpulan laporan, menghitung kata paling sering,
dan menyimpan satu laporan sebagai dictionary berisi `teks`, `label`,
`korban`.

## Contoh kode

```python title="04_koleksi.py" linenums="1"
--8<-- "level-1-python/04_koleksi.py"
```

### Penjelasan kode

1. List `kata` berisi duplikat; `append` menambah elemen di akhir.
2. Tuple `koordinat` dibongkar menjadi `lat, lon` (*unpacking*).
3. `set(kata)` membuang duplikat; `sorted` membuat urutan tampil stabil karena set tak berurutan. Operator `&` adalah irisan dua set.
4. Dictionary `laporan` diakses dengan kunci; `get` memberi nilai default.
5. Perulangan terakhir membangun kamus frekuensi.

### Output dan interpretasi

```text
['banjir', 'tolong', 'banjir', 'evakuasi'] 4
['banjir', 'tolong', 'banjir', 'evakuasi', 'air']
-6.2 106.8
['air', 'banjir', 'evakuasi', 'tolong'] 4
{'banjir'}
Emergency tidak diketahui
['teks', 'label', 'korban', 'lokasi']
{'banjir': 2, 'tolong': 1, 'evakuasi': 1, 'air': 1}
```

Lima elemen list menjadi empat anggota set karena `banjir` muncul dua kali.
Pola `frekuensi[k] = frekuensi.get(k, 0) + 1` adalah dasar *bag of words*.
Pada praktiknya `collections.Counter` melakukannya dalam satu baris.

## Kesalahan umum

- Mengharapkan set mempertahankan urutan.
- Memakai list sebagai kunci dictionary (list tidak *hashable*); gunakan tuple.
- Mengubah list saat sedang diiterasi.
- Menyalin list dengan `b = a`; keduanya menunjuk objek sama. Gunakan `a.copy()`.

## Latihan mandiri

1. Dari `["tolong", "banjir", "tolong"]` buat kamus frekuensi tanpa `Counter`, lalu dengan `Counter`.
2. Cari kata yang muncul di kedua laporan `"banjir naik"` dan `"banjir surut"` dengan set.
3. Simpan tiga laporan sebagai list of dict, lalu cetak hanya yang berlabel Emergency.

## Kuis singkat

**1.** Struktur apa untuk menyimpan stopwords demi pencarian cepat?

??? success "Jawaban"
    `set`, karena uji keanggotaannya rata-rata O(1).

**2.** Mengapa `sorted(set(...))` dipakai saat mencetak?

??? success "Jawaban"
    Set tidak berurutan; `sorted` membuat keluaran deterministik.

## Ringkasan

List untuk urutan, tuple untuk pasangan tetap, set untuk keunikan dan uji
keanggotaan, dict untuk pemetaan seperti frekuensi kata.

## Referensi

- Dokumentasi Python: *Data Structures* (<https://docs.python.org/3/tutorial/datastructures.html>).

## Materi selanjutnya

[Kondisional](kondisional.md)
