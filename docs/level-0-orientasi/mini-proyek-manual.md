# Mini Proyek: Mengelompokkan Teks Secara Manual

## Tujuan pembelajaran

- [ ] Menerapkan definisi dan aturan anotasi pada postingan nyata atau sintetis.
- [ ] Merasakan sendiri kasus ambigu dan ketidaksepakatan label.
- [ ] Menghitung kesepakatan sederhana antara dua anotator.

## Prasyarat

[Memahami Masalah Emergency vs Non-Emergency](masalah-emergency.md) dan [Teks Media Sosial](teks-media-sosial.md).

## Pengantar dan intuisi

Sebelum menyerahkan pekerjaan ke model, kerjakan dulu secara manual. Anotasi
manual mengungkap kelemahan definisi label, dan menghasilkan data kecil
berlabel yang nantinya dapat menjadi pembanding.

## Konsep

**Kesepakatan (agreement)** antara dua anotator pada sampel yang sama
menunjukkan seberapa jelas definisi label. Ukuran paling sederhana adalah
*persentase kesepakatan*:

$$
\text{agreement} = \frac{\text{jumlah label yang sama}}{\text{jumlah contoh}}
$$

Persentase ini belum memperhitungkan kesepakatan karena kebetulan. Ukuran
yang lebih baik, seperti Cohen's kappa, dibahas ringkas di Level 5.

## Tugas

Berikut 10 postingan **sintetis**. Beri label `E` (Emergency), `N`
(Non-Emergency), atau `U` (uncertain) menggunakan aturan di halaman
sebelumnya. Kerjakan sendiri **sebelum** melihat kunci.

| # | Postingan |
|---|---|
| 1 | "Banjir masuk rumah, air sudah selutut, tolong kirim perahu karet ke Gg. Mawar 3" |
| 2 | "Besok ada simulasi gempa di sekolah anak saya" |
| 3 | "Pohon tumbang menimpa mobil di depan kantor, pengemudi terjepit!!" |
| 4 | "Musim hujan begini selalu bikin deg-degan, semoga aman" |
| 5 | "BMKG: gempa M5,0 pukul 06.30, tidak berpotensi tsunami" |
| 6 | "Banjir tahun lalu parah banget, sekarang drainase sudah diperbaiki" |
| 7 | "Ada suara ledakan dan asap hitam dari arah pabrik, warga berhamburan" |
| 8 | "Tolong RT kami belum dapat bantuan sembako" |
| 9 | "Lagi asik nonton, tiba-tiba lampu mati. Pasti PLN lagi..." |
| 10 | "Jalan Merdeka tergenang, motor mogok, tapi masih bisa dilewati mobil" |

### Kunci pembahasan

??? success "Lihat kunci setelah melabeli sendiri"
    | # | Label | Catatan |
    |---|---|---|
    | 1 | E | Kejadian berlangsung + permintaan bantuan |
    | 2 | N | Kegiatan terjadwal |
    | 3 | E | Korban terjepit, kejadian baru |
    | 4 | N | Opini/kecemasan umum |
    | 5 | N | Berita resmi tanpa ancaman nyata |
    | 6 | N | Informasi lama |
    | 7 | E | Laporan kejadian berlangsung dengan ancaman |
    | 8 | U | Permintaan bantuan nyata, tetapi kebutuhan logistik, bukan keselamatan segera; **diskusikan** |
    | 9 | N | Keluhan tanpa ancaman jelas |
    | 10 | U | Banjir ada, tetapi tidak jelas ancaman; **diskusikan** |

    Perbedaan label pada #8 dan #10 adalah hal wajar dan justru bagian
    pembelajarannya: aturan perlu diperjelas, misalnya apakah kebutuhan
    logistik pascabencana termasuk Emergency.

## Contoh kode

Menghitung kesepakatan dua anotator dengan Python murni.

```python title="kesepakatan.py" linenums="1"
--8<-- "level-0-orientasi/kesepakatan.py"
```

### Penjelasan kode

1. `anotator_a` dan `anotator_b` adalah list label dengan urutan contoh yang sama. Pada contoh ini angkanya fiktif untuk mendemonstrasikan rumus.
2. `zip` memasangkan label kedua anotator per contoh.
3. `sum(a == b for ...)` menghitung jumlah pasangan yang sama; dibagi jumlah contoh.
4. Daftar `beda` menyimpan nomor contoh yang berbeda agar bisa didiskusikan.

### Output dan interpretasi

Output nyata:

```text
Kesepakatan: 8/10 = 80%
Contoh yang berbeda (nomor): [8, 10]
```

Angka ini milik data fiktif dua "anotator" pada tabel kecil, **bukan**
estimasi apa pun tentang kualitas dataset. Nilai yang berguna ada pada daftar
`beda`: itulah tempat definisi label perlu diperjelas.

## Kesalahan umum

- Berdiskusi dengan anotator lain sebelum selesai melabeli sehingga kesepakatan terlihat terlalu tinggi.
- Menyimpulkan kualitas dataset dari sampel sangat kecil.
- Memaksa konsensus tanpa mencatat alasan, padahal catatan adalah dokumentasi aturan.

## Latihan mandiri

1. Labeli 10 postingan sintetis buatan Anda, minta teman melabeli juga, hitung kesepakatannya.
2. Untuk setiap ketidaksepakatan, tulis revisi aturan yang menyelesaikannya.
3. Mengapa persentase kesepakatan 90% bisa menyesatkan bila 90% contoh adalah kelas yang sama?

## Kuis singkat

**1.** Apa kelemahan persentase kesepakatan sederhana?

??? success "Jawaban"
    Tidak memperhitungkan kesepakatan karena kebetulan, terutama saat kelas tidak seimbang.

**2.** Apa yang sebaiknya dilakukan dengan contoh berlabel `U`?

??? success "Jawaban"
    Ditinjau bersama untuk memperbaiki aturan; jangan dimasukkan sebagai data latih tanpa keputusan.

## Ringkasan

Anotasi manual mengungkap kelemahan definisi label. Kesepakatan antaranotator
adalah umpan balik untuk memperbaiki aturan, bukan sekadar angka.

## Referensi

- Imran, M., dkk. (2015). Processing social media messages in mass emergency: A survey. *ACM Computing Surveys*, 47(4).
- Dokumentasi scikit-learn: `cohen_kappa_score` (<https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html>).

## Materi selanjutnya

[Level 1: Fondasi Python untuk NLP](../level-1-python/index.md)
