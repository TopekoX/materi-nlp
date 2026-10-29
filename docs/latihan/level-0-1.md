# Latihan Level 0–1: Orientasi dan Python Dasar

!!! abstract "Info latihan"
    **Tingkat kesulitan:** Pemula. **Estimasi waktu:** 120 menit.
    **Cakupan:** [Level 0](../level-0-orientasi/index.md) dan [Level 1](../level-1-python/index.md). Kode kunci jawaban: `examples/latihan/solusi_level_0_1.py` (diuji oleh `tests/test_latihan.py`). Kerjakan dulu sendiri, baru buka kunci.

## Cara memakai halaman ini

1. Baca soal, tulis jawaban atau kode Anda **sebelum** membuka kunci.
2. Jalankan kode Anda; bandingkan dengan keluaran kunci.
3. Bila berbeda, cari tahu **mengapa**: perbedaan sering lebih mengajarkan daripada kecocokan.

Tingkat: ★ konseptual, ★★ membaca/mengisi kode, ★★★ menulis/mendebug, ★★★★ mini-proyek.

## Soal

**1. (★ Konseptual)** Urutkan dari yang paling luas: NLP, kecerdasan buatan, pembelajaran mesin, *deep learning*. Mana yang bukan himpunan bagian dari yang lain?

**2. (★ Konseptual)** Mengapa postingan yang memuat kata "banjir" tidak otomatis Emergency? Berikan satu contoh pasangan teks dengan kata sama tetapi label berbeda.

**3. (★★ Membaca kode)** Apa keluaran kode berikut, dan mengapa `"tolong,"` dan `"Tolong"` dihitung sama?

```python
hitung_kata("Tolong, air masuk rumah! Tolong kirim bantuan.")
```

**4. (★★ Melengkapi kode)** Lengkapi fungsi agar menghitung frekuensi kata (huruf kecil, tanda baca di tepi dibuang):

```python
def hitung_kata(teks):
    hasil = {}
    for kata in teks.______().split():
        kata = kata.strip(".,!?;:")
        if kata:
            hasil[kata] = hasil.______(kata, 0) + 1
    return hasil
```

**5. (★★★ Debugging)** Kode berikut menimbulkan galat. Apa nama galat, mengapa terjadi, dan bagaimana memperbaikinya tanpa `try/except`?

```python
hasil = {}
for kata in ["air", "naik", "air"]:
    hasil[kata] += 1
```

**6. (★★★ Regex)** Tulis fungsi `ekstrak_penanda(teks)` yang mengembalikan daftar hashtag dan daftar mention (tanpa `#` dan `@`) dan **tidak** menganggap bagian setelah `@` pada alamat email sebagai mention. Uji pada: `"Banjir di Jl. Melati #SiagaBencana #banjir cc @posko_contoh, bukan a@b.com"`.

**7. (★★★ Program kecil)** Buat pengklasifikasi kata kunci: Emergency bila teks memuat salah satu dari `tolong, banjir, gempa, kebakaran, longsor, evakuasi, bantuan`. Terapkan pada `handwritten_challenge_id.csv` (48 teks) dan laporkan akurasi, jumlah alarm palsu, dan jumlah pesan darurat yang terlewat. **Tebak dahulu** akurasinya sebelum menjalankan.

**8. (★★★★ Mini-proyek)** Tulis 10 postingan sintetis (empat Emergency, dua `uncertain`, empat Non-Emergency) dan alasan tiap label berdasarkan dua syarat definisi. Minta satu orang melabeli tanpa melihat kunci Anda, lalu hitung kesepakatan mentah dan (opsional) kappa. Lihat [Tahap A](../proyek-klasifikasi-bencana/tahap-a-definisi-masalah.md).

## Kunci jawaban dan pembahasan

??? success "Jawaban 1"
    Kecerdasan buatan (AI) ⊃ pembelajaran mesin (ML) ⊃ *deep learning*. NLP bukan himpunan bagian murni: ia adalah **bidang aplikasi** yang memakai AI/ML (dan teknik non-ML seperti aturan linguistik) untuk bahasa manusia. Pembahasan lebih rinci ada di [AI, ML, DL, NLP](../level-0-orientasi/ai-ml-dl-nlp.md).

??? success "Jawaban 2"
    Emergency memerlukan **dua syarat**: kejadian berlangsung/baru dan laporan atau permintaan bantuan. Pasangan contoh: "Banjir setinggi dada, mohon evakuasi!" (Emergency) vs "Banjir tahun lalu merusak banyak rumah." (Non-Emergency). Kata kunci "banjir" ada di keduanya.

??? success "Jawaban 3"
    Keluaran (nyata):

    ```text title="Output nyata"
    {'tolong': 2, 'air': 1, 'masuk': 1, 'rumah': 1, 'kirim': 1, 'bantuan': 1}
    ```

    `.lower()` menyeragamkan huruf besar-kecil, dan `.strip(".,!?;:")` membuang tanda baca di tepi kata, sehingga `"Tolong,"` dan `"Tolong"` menjadi `"tolong"` yang sama (dihitung 2). Jika `.lower()` dilupakan, `Tolong` dan `tolong` akan terhitung sebagai dua kata berbeda.

??? success "Jawaban 4"
    ```python title="Kunci"
    --8<-- "latihan/solusi_level_0_1.py:hitung_kata"
    ```

    Bagian kosong: `lower` dan `get`. `dict.get(kunci, 0)` mengembalikan 0 bila kunci belum ada, sehingga penambahan pertama tidak menimbulkan `KeyError`. Pemeriksaan `if kata:` melewati token yang hanya berisi tanda baca (misalnya `"..."`), yang setelah `strip` menjadi string kosong.

??? success "Jawaban 5"
    `KeyError: 'air'`. Pada iterasi pertama `hasil["air"]` belum ada, sehingga operasi `+= 1` (yang membaca nilai lama) gagal. Perbaikan tanpa `try/except`: `hasil[kata] = hasil.get(kata, 0) + 1`, atau `collections.Counter(kata_kata)`. Galat itu bukan bug pada Python; ia memberi tahu bahwa kita membaca sesuatu yang belum ada.

??? success "Jawaban 6"
    ```python title="Kunci"
    --8<-- "latihan/solusi_level_0_1.py:ekstrak"
    ```

    ```text title="Output nyata"
    (['SiagaBencana', 'banjir'], ['posko_contoh'])
    ```

    Pola `(?<![\w.])@(\w+)` memakai *lookbehind negatif*: `@` hanya dihitung bila **tidak** didahului huruf, angka, garis bawah, atau titik. Pada `a@b.com`, `@` didahului `a` sehingga tidak dihitung. Keluaran: hashtag `['SiagaBencana', 'banjir']`, mention `['posko_contoh']`. Tanda kurung `(\w+)` menangkap kata tanpa awalan `#`/`@`.

??? success "Jawaban 7"
    ```python title="Kunci"
    --8<-- "latihan/solusi_level_0_1.py:kata_kunci"
    ```

    ```text title="Output nyata"
    distribusi label: {'Emergency': 24, 'Non-Emergency': 24}
    akurasi kata kunci: 0.354
    alarm palsu: 16 | darurat terlewat: 15
      FP: Alhamdulillah rumah kami aman semua setelah gempa tadi pagi, cuma gelas pec
      FP: BNPB merilis laporan tahunan jumlah kejadian bencana, banjir masih mendomin
      FN: Astaga dapur tetangga meledak, apinya udah ngejalar ke atap. Siapa punya AP
      FN: air di lorong rumah gue udh sepinggang dan masih nambah, listrik gue matiin
    ```

    Akurasi kata kunci hanya **0,354**, **lebih buruk daripada menebak** (0,5 pada data seimbang ini). Alarm palsu 16: pesan seperti "Alhamdulillah rumah kami aman semua setelah gempa tadi pagi" memuat `gempa` tetapi tidak darurat. Terlewat 15: pesan darurat seperti "air di lorong rumah gue udh sepinggang ... " tidak memakai satu pun kata kunci. Pelajaran: kata kunci tidak sama dengan definisi (lihat [Level 0](../level-0-orientasi/masalah-emergency.md)). Catatan: daftar kata kunci ini tidak disetel; daftar yang disetel pada set ini akan tampak lebih baik, tetapi itu menyetel pada data uji.

??? success "Jawaban 8"
    Tidak ada kunci tunggal. Yang dinilai: setiap alasan menyebut dua syarat; ada kasus `uncertain` dengan alasan yang masuk akal; kesepakatan dan kappa dihitung dengan benar (rumus di Tahap A). Bila kappa rendah, temukan aturan mana yang kurang jelas.

## Kuis gabungan

**1.** Apa fungsi `dict.get(k, 0)`?

??? success "Jawaban"
    Mengembalikan nilai untuk kunci `k`, atau 0 bila belum ada; menghindari `KeyError`.

**2.** Mengapa baseline kata kunci mendapat akurasi di bawah 0,5 pada tulis-tangan?

??? success "Jawaban"
    Banyak Non-Emergency memuat kata bencana (alarm palsu) dan banyak Emergency tidak memuat kata kunci itu (terlewat).

**3.** Apa arti `(?<![\w.])` pada regex?

??? success "Jawaban"
    "Tidak didahului huruf/angka/garis bawah/titik": lookbehind negatif.

## Checkpoint praktis Level 0–1

- [ ] Saya dapat menjelaskan dua syarat Emergency dan memberi pasangan contoh.
- [ ] Saya dapat menghitung frekuensi kata dengan dict dan `get`.
- [ ] Saya dapat mengenali dan memperbaiki `KeyError`.
- [ ] Saya dapat menulis regex sederhana dengan grup tangkap.
- [ ] Saya dapat menjelaskan mengapa kata kunci bukan klasifikasi yang baik.

## Materi berikutnya

[Latihan Level 2–3](level-2-3.md)
