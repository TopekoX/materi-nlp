# Perulangan

## Tujuan pembelajaran

- [ ] Memakai `for`, `while`, `enumerate`, dan `zip`.
- [ ] Mengontrol perulangan dengan `break` dan `continue`.
- [ ] Menulis list/set comprehension yang mudah dibaca.

## Prasyarat

[Kondisional](kondisional.md).

## Pengantar dan intuisi

Hampir setiap pekerjaan NLP adalah "lakukan hal yang sama untuk setiap
dokumen/kata". `for` mengiterasi koleksi yang sudah ada; `while` mengulang
selama kondisi benar dan harus punya akhir.

## Konsep

| Konstruksi | Fungsi |
|---|---|
| `for x in koleksi` | iterasi tiap elemen |
| `enumerate(koleksi, start=1)` | elemen beserta nomor urutnya |
| `zip(a, b)` | memasangkan dua koleksi |
| `break` / `continue` | berhenti / lompat ke iterasi berikutnya |
| `[ekspresi for x in k if kondisi]` | list comprehension |
| `{ekspresi for x in k}` | set comprehension |

Comprehension bagus untuk transformasi sederhana. Jika memerlukan banyak
kondisi bertingkat, gunakan `for` biasa agar terbaca.

## Contoh kontekstual kebencanaan

Mengiterasi tiga laporan pendek untuk menghitung panjang kata, melewati
laporan bertanda "besok", dan mengumpulkan laporan yang cukup panjang.

## Contoh kode

```python title="06_perulangan.py" linenums="1"
--8<-- "level-1-python/06_perulangan.py"
```

### Penjelasan kode

1. `enumerate(..., start=1)` memberi nomor mulai 1.
2. `continue` melewati laporan yang mengandung "besok"; `jumlah` menghitung sisanya.
3. List comprehension `panjang` membuat list jumlah kata; set comprehension `panjang_teks` menyaring teks berdasarkan panjang karakter.
4. `while` mengurangi `n` sampai tidak positif.
5. `zip` memasangkan dua list.

### Output dan interpretasi

```text
1 banjir naik 2
2 gempa terasa 2
3 pelatihan besok 2
tanpa 'besok': 2
[2, 2, 2]
['gempa terasa', 'pelatihan besok']
n akhir: -1
a 1
b 2
```

Setiap laporan kebetulan bernilai 2 kata sehingga `[2, 2, 2]` tidak
informatif; pada data sungguhan panjangnya bervariasi. `n` berakhir `-1`
(5 → 3 → 1 → -1), bukan 0, karena langkah 2 melompati 0: contoh mengapa kondisi
berhenti `while` harus dipikirkan.

## Kesalahan umum

- `while` tanpa perubahan pada kondisi (perulangan tak berujung).
- Mengubah list yang sedang diiterasi.
- Memakai `range(len(x))` padahal `for item in x` atau `enumerate` lebih jelas.
- `zip` berhenti di koleksi terpendek tanpa peringatan.

## Latihan mandiri

1. Hitung total kata dari seluruh daftar teks dengan `for` lalu dengan `sum` dan comprehension.
2. Cetak hanya teks yang panjangnya lebih dari rata-rata.
3. Ubah `while` agar berhenti tepat saat `n <= 0` dan cetak setiap nilai `n`.

## Kuis singkat

**1.** Beda `break` dan `continue`?

??? success "Jawaban"
    `break` keluar dari perulangan sepenuhnya; `continue` hanya melewati iterasi saat ini.

**2.** Berapa panjang hasil `zip([1,2,3], ["a"])`?

??? success "Jawaban"
    1, karena `zip` berhenti pada koleksi terpendek.

## Ringkasan

`for` untuk iterasi koleksi, `while` dengan kondisi berhenti yang jelas,
`enumerate`/`zip` untuk kenyamanan, dan comprehension untuk transformasi sederhana.

## Referensi

- Dokumentasi Python: *for Statements* dan *List Comprehensions* di tutorial resmi.

## Materi selanjutnya

[Function dan Parameter](function-parameter.md)
