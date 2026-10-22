# CSV dan JSON

## Tujuan pembelajaran

- [ ] Membaca CSV sebagai list of dict dengan `csv.DictReader`.
- [ ] Menyimpan dan membaca JSON dengan benar, termasuk karakter non-ASCII.
- [ ] Memilih format yang sesuai: CSV untuk tabel, JSON untuk struktur bersarang.

## Prasyarat

[Membaca dan Menulis File Teks](file-teks.md).

## Pengantar dan intuisi

Dataset teks umumnya berupa **CSV** (tabel datar: baris = dokumen) dan
konfigurasi/respons API berupa **JSON** (kamus bersarang). Python standar
sudah cukup untuk keduanya.

## Konsep

| Format | Bentuk | Kelebihan | Kelemahan |
|---|---|---|---|
| CSV | Baris dan kolom, dipisah koma | Ringan, dibuka di spreadsheet | Semua nilai berupa teks; koma di dalam teks perlu tanda kutip |
| JSON | Objek `{}` dan array `[]` | Bersarang, tipe dasar jelas | Kurang cocok untuk tabel besar |

Catatan penting:

- `csv.DictReader` membaca setiap nilai sebagai **string**. `"1"` bukan `1`.
- Teks yang mengandung koma atau baris baru harus dikutip; modul `csv` menanganinya.
- `json.dumps` secara default menulis karakter non-ASCII sebagai `\uXXXX`. Gunakan `ensure_ascii=False` agar terbaca.

## Contoh kontekstual kebencanaan

File `laporan_contoh.csv` (sintetis, 10 baris) berisi `id`, `teks`, `label`,
`lokasi`. Kita memuatnya, memfilter yang Emergency, dan mengekspor satu
laporan sebagai JSON.

## Contoh kode

```python title="11_csv_json.py" linenums="1"
--8<-- "level-1-python/11_csv_json.py"
```

### Penjelasan kode

1. `Path(__file__).parent / "data" / ...` membuat jalur relatif terhadap lokasi skrip, sehingga skrip dapat dijalankan dari folder mana pun.
2. `csv.DictReader` mengubah tiap baris menjadi dictionary berkunci nama kolom; `list(...)` memuat semuanya.
3. Set comprehension mengumpulkan label unik, lalu `sorted` agar keluaran stabil.
4. List comprehension menyaring baris Emergency.
5. `json.dumps(..., ensure_ascii=False)` mengubah dict menjadi string JSON; `json.loads` membalikkannya.
6. Dua baris terakhir membandingkan keluaran JSON dengan dan tanpa `ensure_ascii=False` untuk emoji.

### Output dan interpretasi

```text
10 {'id': '1', 'teks': 'Banjir setinggi dada di Jl. Melati mohon evakuasi', 'label': 'Emergency', 'lokasi': 'Jakarta'}
['Emergency', 'Non-Emergency']
5
{"id": "1", "teks": "Banjir setinggi dada di Jl. Melati mohon evakuasi", "label": "Emergency", "lokasi": "Jakarta"}
Jakarta
{"teks": "tolong 🙏"}
'{"teks": "tolong \U0001f64f"}'
```

Perhatikan `'id': '1'`: nilainya string, bukan angka. Untuk analisis numerik,
`pandas` (halaman berikutnya) menebak tipe secara otomatis. Baris terakhir
menunjukkan emoji tersimpan sebagai pasangan *surrogate* (`🙏`) bila
`ensure_ascii` default dipakai: valid, tetapi tidak terbaca manusia.
(Ditampilkan dengan `ascii(...)` agar aman di semua terminal.)

## Kesalahan umum

- Membuka CSV tanpa `newline=""` dan `encoding="utf-8"`.
- Lupa bahwa semua nilai CSV adalah string.
- Memecah CSV dengan `baris.split(",")` sehingga koma di dalam teks merusak kolom.
- Menyimpan data pribadi dalam contoh yang dipublikasikan.

## Latihan mandiri

1. Hitung jumlah laporan per lokasi dengan `Counter` dari hasil `DictReader`.
2. Tulis laporan berlabel Emergency ke file `darurat.json` (isi list of dict).
3. Tulis CSV baru dengan `csv.DictWriter` yang berisi kolom `id` dan `teks` saja.

## Kuis singkat

**1.** Tipe nilai yang dibaca `csv.DictReader`?

??? success "Jawaban"
    Selalu `str`.

**2.** Mengapa tidak memakai `split(",")` untuk membaca CSV?

??? success "Jawaban"
    Teks dapat memuat koma yang berada di dalam tanda kutip; modul `csv` menanganinya dengan benar.

## Ringkasan

CSV untuk tabel datar, JSON untuk struktur bersarang. Gunakan modul standar,
UTF-8, dan perhatikan bahwa nilai CSV bertipe string.

## Referensi

- Dokumentasi Python: modul `csv` dan `json`.

## Materi selanjutnya

[Dasar NumPy](numpy-dasar.md)
