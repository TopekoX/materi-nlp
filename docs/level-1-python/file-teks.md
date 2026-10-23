# Membaca dan Menulis File Teks

!!! abstract "Info materi"
    **Tingkat kesulitan:** Pemula. **Estimasi waktu:** 60–90 menit.
    **Jenis kode:** snippet edukatif (`examples/level-1-python/10_file_teks.py`). Berkas dibuat di folder sementara dan otomatis dihapus.

## Tujuan pembelajaran

- [ ] Membaca dan menulis berkas teks dengan `pathlib.Path` dan `open`.
- [ ] Memakai `with` agar berkas selalu tertutup.
- [ ] Selalu menyebut `encoding="utf-8"` dan menjelaskan alasannya.
- [ ] Mengenali `FileNotFoundError` dan `UnicodeDecodeError`.

## Prasyarat

[Exception Handling](exception-handling.md) dan [Karakter, Unicode, dan UTF-8](../level-2-fondasi-teks/karakter-unicode-encoding.md) (boleh dibaca sesudahnya).

## Pengantar dan motivasi

Data hampir selalu berasal dari berkas: kumpulan laporan, hasil unduhan, atau catatan relawan. Membaca dan
menulis berkas dengan benar menentukan apakah data utuh sampai ke model. Salah satu sumber kerusakan paling
umum pada teks Indonesia (dengan tanda "–", emoji, dan aksen) adalah **encoding** yang tidak dinyatakan.

## Konsep dasar

- **Jalur (path)**: lokasi berkas. `pathlib.Path` menyusun jalur lintas sistem operasi (`Path("a") / "b.txt"`).
- **Mode buka**: `"r"` baca (bawaan), `"w"` tulis (menimpa), `"a"` tambah di akhir.
- **`with open(...) as f:`** membuka berkas dan **menutupnya otomatis** setelah blok, bahkan jika terjadi galat.
- **Encoding**: aturan mengubah teks menjadi byte di berkas. Gunakan `utf-8`.

## Penjelasan mendalam

### Mengapa selalu menulis `encoding="utf-8"`

Tanpa `encoding`, Python memakai encoding **bawaan sistem** yang dapat berbeda (Windows lama memakai cp1252).
Berkas yang ditulis di satu mesin bisa rusak saat dibaca di mesin lain. Menyatakan `utf-8` secara eksplisit membuat
perilaku sama di mana pun.

### Dua cara membaca

- `Path.read_text()` membaca seluruh isi sekaligus sebagai satu string. Ringkas untuk berkas kecil.
- Iterasi `for baris in f:` membaca **satu baris per putaran** tanpa memuat seluruh berkas ke memori; cocok untuk
  berkas besar.

### `with` lebih baik daripada `f.close()` manual

Jika terjadi galat sebelum `f.close()`, berkas tidak tertutup dan data tulisan dapat hilang. `with` menjamin penutupan.

### Penulisan menimpa atau menambah

`write_text` dan mode `"w"` **menghapus isi lama**. Untuk menambah di akhir, pakai mode `"a"`. Periksa mode sebelum
menjalankan agar tidak menimpa data penting.

### Karakter dan byte

Jumlah karakter tidak sama dengan jumlah byte (Bagian 2): emoji memakai 4 byte di UTF-8.

## Cara kerja atau alur proses

```mermaid
flowchart LR
    S["string di memori"] -- "encode utf-8" --> B["byte di berkas"]
    B -- "decode utf-8" --> S2["string di memori"]
```

## Contoh sederhana

```python
from pathlib import Path
Path("catatan.txt").write_text("halo", encoding="utf-8")
Path("catatan.txt").read_text(encoding="utf-8")   # 'halo'
```

## Contoh dalam konteks Twitter/X kebencanaan

Catatan relawan berisi baris teks berisi emoji `🙏`. Bila dibaca dengan encoding yang salah, "tolong 🙏" menjadi
karakter rusak atau menimbulkan galat, dan model belajar dari kata yang bukan kata.

## Praktik Python

Berkas: `examples/level-1-python/10_file_teks.py`. Semua operasi berlangsung di folder sementara (`tempfile.TemporaryDirectory`) yang dihapus otomatis saat blok `with` selesai, sehingga tidak ada berkas tersisa. Variabel `p` adalah jalur berkas `catatan.txt` di folder sementara itu.

### Bagian 1 — Menulis

```python title="Bagian 1"
--8<-- "level-1-python/10_file_teks.py:tulis"
```

`write_text` menulis string ke berkas (menimpa). `\n` adalah baris baru; `\U0001F64F` adalah kode emoji 🙏.

```text title="Output nyata"
catatan.txt True
```

Interpretasi: berkas `catatan.txt` ada setelah ditulis.

### Bagian 2 — Membaca seluruh isi

```python title="Bagian 2"
--8<-- "level-1-python/10_file_teks.py:baca"
```

`ascii(isi)` menampilkan karakter non-ASCII sebagai kode (`\U0001f64f`) agar aman di semua terminal. `isi.encode("utf-8")` mengubah menjadi byte.

```text title="Output nyata"
'banjir naik\ntolong evakuasi \U0001f64f\n'
30 33
```

Interpretasi: isi sama dengan yang ditulis. Teks berisi 30 karakter tetapi 33 byte (selisih 3: emoji 1 karakter = 4 byte). **Karakter ≠ byte.**

### Bagian 3 — Membaca baris demi baris

```python title="Bagian 3"
--8<-- "level-1-python/10_file_teks.py:baris"
```

`with open(...) as f` membuka berkas; `enumerate(f, start=1)` memberi nomor baris; `rstrip("\n")` membuang baris baru di ujung.

```text title="Output nyata"
1 'banjir naik'
2 'tolong evakuasi \U0001f64f'
```

Interpretasi: dua baris terbaca. Tanpa `rstrip("\n")`, setiap baris membawa karakter baris baru di akhir.

### Bagian 4 — Menambah

```python title="Bagian 4"
--8<-- "level-1-python/10_file_teks.py:tambah"
```

```text title="Output nyata"
3
```

Interpretasi: mode `"a"` menambahkan baris ketiga tanpa menghapus yang lama; `splitlines()` memecah menjadi daftar baris dan `len` = 3.

### Bagian 5 — Encoding yang salah

```python title="Bagian 5"
--8<-- "level-1-python/10_file_teks.py:encoding_salah"
```

```text title="Output nyata"
UnicodeDecodeError: ordinal not in range(128)
b'banjir n'
```

Interpretasi: membaca berkas berisi emoji sebagai `ascii` gagal, karena byte emoji di luar rentang 0–127. Pesan `UnicodeDecodeError` menandai ketidakcocokan encoding. `read_bytes()` menunjukkan byte mentah (huruf Latin tetap sama di UTF-8 dan ASCII). Perbaikannya: baca dengan `encoding="utf-8"` (encoding yang dipakai saat menulis).

### Bagian 6 — Berkas tidak ada

```python title="Bagian 6"
--8<-- "level-1-python/10_file_teks.py:tidak_ada"
```

```text title="Output nyata"
FileNotFoundError
```

Interpretasi: membaca berkas yang tidak ada menimbulkan `FileNotFoundError`, yang ditangkap di sini. Penyebab umum: salah ketik nama, atau jalur relatif terhadap folder kerja yang berbeda.

### Skrip terpadu

Keenam bagian adalah satu skrip: `10_file_teks.py`.

## Kesalahan umum dan debugging

| Gejala | Penyebab | Perbaikan |
|---|---|---|
| `FileNotFoundError` | Jalur salah atau folder kerja berbeda | Cetak `Path.cwd()`; pakai jalur relatif terhadap skrip: `Path(__file__).parent` |
| `UnicodeDecodeError` | Encoding baca berbeda dari encoding tulis | Gunakan `encoding="utf-8"` (atau encoding sebenarnya berkas) |
| `UnicodeEncodeError` saat menulis atau mencetak | Encoding tujuan tidak mendukung karakter | `encoding="utf-8"`; di konsol Windows `python -X utf8` |
| Data lama hilang | Membuka dengan mode `"w"` | Gunakan `"a"` bila ingin menambah |
| Baris punya karakter baris baru ekstra | Tidak memakai `rstrip("\n")` | `baris.rstrip("\n")` atau `splitlines()` |
| Berkas terkunci atau tidak tersimpan | Tidak ditutup | Selalu pakai `with` |

## Kelebihan dan keterbatasan

**Kelebihan:** `pathlib` dan `with` ringkas dan aman; UTF-8 eksplisit membuat data portabel. **Keterbatasan:** membaca seluruh isi
berkas besar memakai banyak memori; format terstruktur (CSV, JSON) lebih baik dibaca dengan pustaka khusus (halaman berikutnya).

## Latihan bertahap

1. **Konseptual.** Mengapa `encoding="utf-8"` sebaiknya selalu ditulis?
2. **Membaca kode.** Apa beda `open(p, "w")` dan `open(p, "a")`?
3. **Mengisi kode.** Lengkapi: `with open(p, ___, encoding="utf-8") as f:` agar membaca berkas baris demi baris.
4. **Debugging.** `UnicodeDecodeError: 'charmap' codec can't decode byte ...` muncul saat membaca CSV. Dua hal yang diperiksa?
5. **Program kecil.** Tulis kode yang menulis tiga laporan ke `laporan.txt`, membacanya kembali, dan mencetak jumlah baris dan jumlah kata total.

## Kunci jawaban dan pembahasan

??? success "Jawaban 1"
    Encoding bawaan berbeda antar sistem; menyebut `utf-8` secara eksplisit membuat baca-tulis konsisten dan melindungi karakter non-ASCII (emoji, aksen).

??? success "Jawaban 2"
    `"w"` menimpa seluruh isi berkas; `"a"` menambah di akhir tanpa menghapus isi lama.

??? success "Jawaban 3"
    `"r"` (mode baca; juga bawaan): `with open(p, "r", encoding="utf-8") as f:`.

??? success "Jawaban 4"
    (1) Encoding berkas sebenarnya; mungkin bukan UTF-8 (mis. cp1252 dari Excel lama), sehingga coba `encoding="cp1252"` atau simpan ulang sebagai UTF-8. (2) Apakah `encoding` disebut pada `open`; tanpa itu Python memakai encoding sistem.

??? success "Jawaban 5"
    ```python
    from pathlib import Path
    p = Path("laporan.txt")
    p.write_text("banjir naik\ngempa terasa\npos dibuka\n", encoding="utf-8")
    baris = p.read_text(encoding="utf-8").splitlines()
    print(len(baris), sum(len(b.split()) for b in baris))   # 3 6
    ```
    Tiga baris, masing-masing dua kata, total enam kata.

## Kuis singkat

**1.** Apa keuntungan `with open(...)`?

??? success "Jawaban"
    Berkas otomatis ditutup, bahkan bila terjadi galat.

**2.** Mengapa jumlah karakter dan jumlah byte berbeda?

??? success "Jawaban"
    UTF-8 memakai 1–4 byte per karakter; emoji dan karakter non-ASCII memakai lebih dari satu byte.

**3.** Mode apa yang menambah tanpa menghapus isi?

??? success "Jawaban"
    `"a"` (*append*).

## Ringkasan

- Gunakan `pathlib.Path` untuk jalur dan `with open(...)` untuk berkas yang selalu tertutup.
- Selalu sebut `encoding="utf-8"`; karakter ≠ byte.
- Mode `"w"` menimpa, `"a"` menambah; periksa `FileNotFoundError` dan `UnicodeDecodeError`.

## Glosarium istilah baru

Path (jalur)
:   Lokasi berkas atau folder.

Encoding
:   Aturan mengubah teks menjadi byte dan sebaliknya.

Context manager (`with`)
:   Konstruksi yang menyiapkan dan membersihkan sumber daya otomatis.

Mode buka
:   Cara membuka berkas: `"r"`, `"w"`, `"a"`.

## Referensi

- Dokumentasi Python, *Reading and Writing Files* (tutorial): <https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files> (dokumentasi resmi).
- Dokumentasi Python, `pathlib`: <https://docs.python.org/3/library/pathlib.html> (dokumentasi resmi).

## Materi selanjutnya

[CSV dan JSON](csv-json.md)
