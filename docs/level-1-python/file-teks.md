# Membaca dan Menulis File Teks

## Tujuan pembelajaran

- [ ] Membaca dan menulis file teks dengan encoding UTF-8 yang eksplisit.
- [ ] Memakai `with` agar file tertutup otomatis.
- [ ] Memakai `pathlib.Path` untuk jalur yang portabel.

## Prasyarat

[Exception Handling](exception-handling.md).

## Pengantar dan intuisi

Teks tersimpan di file sebagai **byte**; encoding menentukan bagaimana byte
dipetakan ke karakter. Jika encoding tidak disebutkan, Python memakai
default sistem, yang berbeda-beda (Windows sering tidak UTF-8). Hasilnya:
file yang sama terbaca benar di satu komputer dan rusak di komputer lain.
Selalu tulis `encoding="utf-8"`.

## Konsep

| Mode | Arti |
|---|---|
| `"r"` | baca (default) |
| `"w"` | tulis, **menimpa** isi lama |
| `"a"` | tambah di akhir |
| `"rb"`, `"wb"` | biner |

- `with open(...) as f:` menutup file otomatis walau terjadi galat.
- `Path.read_text(encoding=...)` dan `Path.write_text(...)` untuk file kecil.
- Iterasi `for baris in f` membaca baris demi baris, hemat memori untuk file besar.
- `newline=""` direkomendasikan saat membuka file CSV.

!!! danger "Mode `w` menghapus isi"
    Membuka file dengan `"w"` langsung mengosongkannya. Periksa jalur sebelum menulis.

## Contoh kontekstual kebencanaan

Menyimpan catatan posko dan membaca kembali per baris. Contoh menyertakan
emoji agar terlihat dampak encoding.

## Contoh kode

```python title="10_file_teks.py" linenums="1"
--8<-- "level-1-python/10_file_teks.py"
```

### Penjelasan kode

1. Folder sementara (`tempfile`) dipakai agar tidak membuat file permanen.
2. `write_text` menulis dua baris, `read_text` membacanya kembali.
3. Perulangan `for` membaca per baris; `rstrip("\n")` membuang pemisah baris.
4. Mode `"a"` menambah baris ketiga; `splitlines()` menghitung baris.
5. Membaca file yang tidak ada ditangkap sebagai `FileNotFoundError`.
6. `ascii(...)` dipakai agar emoji tampil sebagai kode (`\U0001f64f`) dan terminal mana pun dapat menampilkannya.

### Output dan interpretasi

```text
'banjir naik\ntolong evakuasi \U0001f64f\n'
1 'banjir naik'
2 'tolong evakuasi \U0001f64f'
3
FileNotFoundError
```

Emoji dibaca utuh karena membaca dan menulis memakai UTF-8 yang sama. Jika
menulis memakai UTF-8 tetapi membaca memakai encoding lain (mis. `cp1252`
di Windows), Anda akan mendapat `UnicodeDecodeError` atau karakter rusak
(*mojibake*).

## Kesalahan umum

- Tidak menyebut `encoding`.
- Memakai `"w"` pada file penting.
- Membaca file sangat besar sekaligus (`read()`); iterasi per baris lebih aman.
- Jalur absolut milik komputer sendiri, tidak portabel.

## Latihan mandiri

1. Tulis lima kalimat ke file, lalu baca dan cetak jumlah kata tiap baris.
2. Sengaja baca file UTF-8 berisi emoji dengan `encoding="ascii"` dan amati galatnya.
3. Gunakan `Path` untuk membuat folder `keluaran/` jika belum ada (`mkdir(exist_ok=True)`).

## Kuis singkat

**1.** Mengapa menyebut `encoding="utf-8"` secara eksplisit?

??? success "Jawaban"
    Agar perilaku tidak bergantung pada default sistem dan teks Indonesia/emoji aman lintas komputer.

**2.** Apa risiko mode `"w"`?

??? success "Jawaban"
    Isi file lama langsung terhapus.

## Ringkasan

Gunakan `with`, UTF-8 eksplisit, dan `Path`. Berhati-hatilah dengan mode tulis.

## Referensi

- Dokumentasi Python: *Reading and Writing Files* (<https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files>) dan modul `pathlib`.

## Materi selanjutnya

[CSV dan JSON](csv-json.md)
