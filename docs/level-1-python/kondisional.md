# Kondisional

## Tujuan pembelajaran

- [ ] Menulis `if`/`elif`/`else` dengan urutan kondisi yang benar.
- [ ] Menggabungkan kondisi dengan `and`, `or`, `not`.
- [ ] Menjelaskan nilai *truthy* dan *falsy*.

## Prasyarat

[List, Tuple, Set, dan Dictionary](list-tuple-set-dict.md).

## Pengantar dan intuisi

Kondisional memungkinkan program memilih jalur. Dalam NLP: "jika teks kosong,
lewati", "jika mengandung URL, tandai". Python memeriksa kondisi dari atas ke
bawah dan menjalankan **cabang pertama** yang benar.

## Konsep

- Operator perbandingan: `==`, `!=`, `<`, `<=`, `>`, `>=`, `in`, `is`.
- `and`, `or`, `not` menggabungkan kondisi; `and` dan `or` berhenti lebih awal (*short-circuit*).
- Falsy: `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`. Lainnya truthy.
- Ekspresi satu baris: `nilai_a if kondisi else nilai_b`.

!!! warning "Urutan kondisi penting"
    Pada rantai `elif`, periksa kondisi yang **lebih spesifik/ketat lebih dulu**.
    Jika `>= 50` ditaruh sebelum `>= 100`, nilai 120 tidak pernah mencapai
    cabang `>= 100`.

## Contoh kontekstual kebencanaan

Mengubah tinggi air (cm) menjadi status peringatan sederhana, dan memberi
label sementara pada teks berdasarkan kata kunci. Aturan kata kunci ini hanya
ilustrasi, bukan klasifikator yang layak.

## Contoh kode

```python title="05_kondisional.py" linenums="1"
--8<-- "level-1-python/05_kondisional.py"
```

### Penjelasan kode

1. `tingkat` memeriksa ambang dari yang tertinggi ke terendah.
2. Perulangan menguji empat nilai. Perhatikan `50` jatuh ke `siaga 2` karena memakai `>=`.
3. `if ... and ...` memeriksa dua kata sekaligus.
4. Ekspresi kondisional memilih label dalam satu baris.
5. Baris terakhir memperlihatkan nilai truthy/falsy.

### Output dan interpretasi

```text
0 -> aman
20 -> waspada
50 -> siaga 2
120 -> siaga 1
mengandung permintaan bantuan banjir
Emergency
False True False False False
```

Ambang `>=` vs `>` menentukan nasib nilai batas (50). Pada keputusan nyata,
nilai batas harus dispesifikasikan secara eksplisit. `bool("")` adalah `False`,
sehingga `if teks:` aman untuk menyaring teks kosong.

## Kesalahan umum

- `=` (penugasan) tertukar dengan `==` (perbandingan).
- Memakai `is` untuk membandingkan string/angka; gunakan `==`. `is` untuk `None`.
- Urutan `elif` yang salah.
- `if x == True:` alih-alih `if x:`.

## Latihan mandiri

1. Buat fungsi yang mengembalikan `"kosong"`, `"pendek"` (< 5 kata), atau `"panjang"` untuk sebuah teks.
2. Jelaskan mengapa `if "tolong" or "banjir" in teks` selalu benar.
3. Perbaiki urutan `elif` yang sengaja salah pada `tingkat`.

## Kuis singkat

**1.** Nilai `bool([])`?

??? success "Jawaban"
    `False`; list kosong falsy.

**2.** Mengapa ekspresi pada latihan 2 selalu benar?

??? success "Jawaban"
    `"tolong"` (string tak kosong) selalu truthy, jadi `or` tidak pernah salah. Tulis `"tolong" in teks or "banjir" in teks`.

## Ringkasan

Kondisional memilih cabang pertama yang benar; urutan dan operator
perbandingan menentukan hasil. Pahami truthy/falsy agar kode ringkas dan benar.

## Referensi

- Dokumentasi Python: *More Control Flow Tools* (<https://docs.python.org/3/tutorial/controlflow.html>).

## Materi selanjutnya

[Perulangan](perulangan.md)
