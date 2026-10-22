# Import dan Modul

## Tujuan pembelajaran

- [ ] Memakai `import`, `from ... import`, dan alias.
- [ ] Menjelaskan perbedaan modul, paket, dan pustaka pihak ketiga.
- [ ] Membuat modul sendiri dan mengimpornya.

## Prasyarat

[Function dan Parameter](function-parameter.md).

## Pengantar dan intuisi

Python hadir dengan "baterai": pustaka standar yang besar (`re`, `csv`,
`json`, `collections`, `pathlib`). Selain itu ada pustaka pihak ketiga yang
dipasang dengan `pip`. Pola yang baik: pakai pustaka standar dahulu, pasang
pustaka tambahan bila memang menambah nilai.

## Konsep

| Bentuk | Contoh | Catatan |
|---|---|---|
| Impor modul | `import math` | Pakai sebagai `math.sqrt` |
| Impor nama | `from collections import Counter` | Pakai langsung `Counter` |
| Alias | `import numpy as np` | Konvensi umum |
| Modul sendiri | `from preprocessing import bersihkan` | Berkas `preprocessing.py` |

Bila modul sendiri tidak ditemukan, penyebab umum: berkas tidak berada di
folder yang sama / tidak ada di `sys.path`, atau nama berkas bentrok dengan
pustaka (jangan menamai berkas `re.py` atau `csv.py`).

Idiom `if __name__ == "__main__":` membuat blok hanya berjalan saat berkas
dijalankan langsung, bukan saat diimpor.

## Contoh kontekstual kebencanaan

Proyek memiliki `preprocessing.py` berisi function pembersih teks, dan notebook
mengimpornya. Dengan begitu fungsi dapat diuji terpisah (Level 2).

## Contoh kode

```python title="08_import_modul.py" linenums="1"
--8<-- "level-1-python/08_import_modul.py"
```

### Penjelasan kode

1. Lima impor: modul, alias (`re as regex`), dan nama spesifik (`Counter`, `Path`).
2. `Counter(...).most_common(1)` mengembalikan kata terbanyak.
3. `Path("examples") / "level-1-python"` menyusun jalur lintas-OS memakai operator `/`.
4. `sys.modules["math"]` menunjukkan bahwa modul yang diimpor adalah objek bertipe `module`.

### Output dan interpretasi

```text
4.0 0.0
[('tolong', 2)]
examples\level-1-python
['05', '12']
module
```

Pemisah jalur `\` muncul karena dijalankan di Windows; di macOS/Linux menjadi
`/`. Memakai `Path` membuat kode portabel.

## Kesalahan umum

- `from modul import *` mengotori namespace dan menyulitkan penelusuran.
- Menamai berkas sama dengan modul standar.
- Impor melingkar (A mengimpor B, B mengimpor A).
- Memasang paket ke Python global alih-alih `.venv`.

## Latihan mandiri

1. Buat `alat_teks.py` berisi function `hapus_spasi_ganda`, lalu impor dari berkas lain.
2. Gunakan `Path.cwd()` untuk menampilkan folder kerja saat ini.
3. Jelaskan fungsi `if __name__ == "__main__":` dengan kata-kata Anda.

## Kuis singkat

**1.** Mengapa jangan menamai berkas `json.py`?

??? success "Jawaban"
    Berkas itu dapat menimpa modul standar `json` pada impor, menyebabkan galat membingungkan.

**2.** Apa kegunaan alias `import numpy as np`?

??? success "Jawaban"
    Penyingkatan nama agar kode lebih ringkas; konvensi komunitas.

## Ringkasan

Gunakan impor eksplisit, utamakan pustaka standar, hindari nama bentrok, dan
manfaatkan `Path` serta `__main__` untuk kode portabel.

## Referensi

- Dokumentasi Python: *Modules* (<https://docs.python.org/3/tutorial/modules.html>).

## Materi selanjutnya

[Exception Handling](exception-handling.md)
