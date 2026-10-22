# Missing Values dan Duplikasi Data

## Tujuan pembelajaran

- [ ] Mendeteksi nilai kosong dan duplikat pada dataset teks.
- [ ] Memilih antara menghapus, mengisi, atau menyelidiki data bermasalah.
- [ ] Menjelaskan mengapa duplikat dapat menyebabkan kebocoran data.

## Prasyarat

[Dasar pandas](pandas-dasar.md).

## Pengantar dan intuisi

Dataset nyata kotor: teks kosong, lokasi hilang, postingan yang sama masuk
berkali-kali (retweet, salinan). Dua masalah ini berdampak langsung pada
evaluasi: jika postingan yang sama ada di data latih dan data uji, skor
terlihat bagus padahal model hanya "menghafal" (kebocoran data).

## Konsep

| Masalah | Deteksi | Opsi penanganan |
|---|---|---|
| Nilai kosong | `df.isna().sum()` | Hapus baris, isi nilai, atau biarkan bila bermakna |
| Duplikat persis | `df.duplicated()` | `drop_duplicates()` |
| Duplikat teks | `df["teks"].duplicated()` | Hapus, tapi periksa labelnya dulu |
| Hampir duplikat | Normalisasi lalu bandingkan | Dibahas di Level 2/5 |

Aturan: **jangan hapus tanpa melihat**. Tanyakan mengapa kosong dan apakah
duplikat memiliki label yang berbeda (konflik label).

## Contoh kontekstual kebencanaan

Pada `laporan_contoh.csv`: baris 9 tidak punya `teks`, baris 6 tidak punya
`lokasi`, dan baris 2 dan 8 berisi teks sama persis.

## Contoh kode

```python title="14_missing_duplikasi.py" linenums="1"
--8<-- "level-1-python/14_missing_duplikasi.py"
```

### Penjelasan kode

1. `df.isna().sum()` menghitung nilai kosong per kolom.
2. `duplicated().sum()` menghitung baris teks yang muncul ulang; `keep=False` menandai **semua** anggota kelompok duplikat agar dapat ditinjau.
3. `dropna(subset=["teks"])` membuang baris tanpa teks; `drop_duplicates(subset="teks", keep="first")` mempertahankan kemunculan pertama.
4. `fillna("tidak diketahui")` mengisi lokasi kosong tanpa menghapus baris.

### Output dan interpretasi

```text
id        0
teks      1
label     0
lokasi    1
dtype: int64
duplikat teks: 1
   id                                         teks
1   2  Pelatihan mitigasi gempa digelar besok pagi
7   8  Pelatihan mitigasi gempa digelar besok pagi
(10, 4) -> (8, 4)
['Jakarta', 'Bandung', 'Surabaya', 'Jakarta', 'Padang', 'tidak diketahui']
```

Satu `teks` kosong dan satu `lokasi` kosong. Satu teks duplikat (baris 8).
Dari 10 baris tersisa 8 setelah membuang baris kosong dan duplikat.
Pada contoh ini label kedua duplikat sama (`Non-Emergency`); jika berbeda,
itu *konflik label* yang harus diselesaikan, bukan sekadar dibuang.

## Kesalahan umum

- Mengisi teks kosong dengan `"nan"` atau `""` lalu melatih model pada "dokumen" kosong.
- Menghapus duplikat **setelah** pembagian train/test; duplikat sudah terlanjur menyebar. Bersihkan sebelum split.
- Menghapus duplikat tanpa memeriksa konflik label.
- Menganggap `NaN == NaN` benar; gunakan `isna()`.

## Latihan mandiri

1. Tambahkan dua baris duplikat dengan label berbeda ke salinan CSV dan deteksi konfliknya dengan `groupby("teks")["label"].nunique()`.
2. Bandingkan hasil `dropna()` tanpa `subset` dengan yang memakai `subset=["teks"]`.
3. Mengapa mengisi `lokasi` kosong dengan "tidak diketahui" aman, sedangkan mengisi `teks` kosong tidak?

## Kuis singkat

**1.** Mengapa duplikat berbahaya untuk evaluasi?

??? success "Jawaban"
    Salinan yang sama dapat berada di data latih dan uji, sehingga skor uji terlalu optimistis.

**2.** Apa fungsi `keep=False` pada `duplicated`?

??? success "Jawaban"
    Menandai semua anggota kelompok duplikat, bukan hanya kemunculan berikutnya.

## Ringkasan

Periksa kosong dan duplikat sebelum apa pun. Selidiki penyebab dan konflik
label, lalu bersihkan **sebelum** membagi data.

## Referensi

- Dokumentasi pandas: *Working with missing data* (<https://pandas.pydata.org/docs/user_guide/missing_data.html>).
- Kaufman, S., dkk. (2012). Leakage in data mining. *ACM TKDD*, 6(4).

## Materi selanjutnya

[Dasar Regex](regex-dasar.md)
