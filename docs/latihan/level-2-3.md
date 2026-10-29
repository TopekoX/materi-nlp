# Latihan Level 2–3: Fondasi Teks dan Representasi

!!! abstract "Info latihan"
    **Tingkat kesulitan:** Pemula–menengah. **Estimasi waktu:** 150 menit.
    **Cakupan:** [Level 2](../level-2-fondasi-teks/index.md) dan [Level 3](../level-3-representasi-teks/index.md). Kode kunci: `examples/latihan/solusi_level_2_3.py` (diuji oleh `tests/test_latihan.py`).

## Soal

Tingkat: ★ konseptual, ★★ membaca/mengisi kode, ★★★ menulis/mendebug, ★★★★ mini-proyek.

**1. (★ Konseptual)** Mengapa "Toloooong" dan "tolong" sebaiknya menjadi token yang sama sebelum dihitung, tetapi "tidak" dan "ada" tidak boleh digabung?

**2. (★★ Membaca kode)** Apa keluaran `praproses("TOLOOONG!! Air udh masuk rmh kami 😭 https://contoh.example/1 #BanjirParah")`? Urutkan langkah yang berperan.

**3. (★★ Negasi)** Apa keluaran `praproses_token("Tidak ada korban jiwa", KonfigurasiPraproses(negasi=True))`, dan mengapa `neg_ada` membantu klasifikasi?

**4. (★★ Stopword)** Apakah `tidak` ada di daftar stopword Sastrawi? Apa akibatnya bila kita memakainya mentah-mentah untuk kalimat "tidak ada korban"?

**5. (★★★ Bag of Words dengan tangan)** Untuk korpus `["air masuk rumah", "tolong air naik", "tolong tolong kirim bantuan"]`, tulis kosakata (urut abjad) dan matriks hitungan, lalu cocokkan dengan `CountVectorizer`.

**6. (★★★ TF-IDF)** Dengan rumus IDF scikit-learn $\ln\frac{1+n}{1+\mathrm{df}}+1$, hitung IDF `tolong` pada korpus di soal 5 dan nilai TF-IDF `tolong` di dokumen ke-3 (tanpa normalisasi). Tulis fungsi `idf_tangan` dan bandingkan dengan `TfidfVectorizer`.

**7. (★★★ N-gram)** Tulis semua unigram dan bigram untuk `["tidak ada korban", "ada korban jiwa"]`. Mengapa bigram `tidak ada` lebih informatif daripada unigram `ada`?

**8. (★★★★ Mini-proyek)** Rancang dua strategi preprocessing untuk pos Twitter/X kebencanaan (satu minimal, satu lengkap). Jelaskan hipotesis, cara mengujinya tanpa kebocoran data, dan apa yang akan Anda lakukan bila hasilnya sama.

## Kunci jawaban dan pembahasan

??? success "Jawaban 1"
    Huruf yang berulang adalah variasi tulisan kata yang sama, sehingga digabung (normalisasi) agar jumlah kata berbeda berkurang. "tidak" dan "ada" adalah dua kata berbeda dengan makna berbeda; menggabungkannya membuang informasi. Kalau perlu, negasi ditangani secara khusus (soal 3).

??? success "Jawaban 2"
    ```text title="Output nyata"
    tolong air sudah masuk rumah kami emo_menangis tok_url banjir parah
    ```

    Langkah yang berperan: huruf kecil (*case folding*), `kurangi_huruf_berulang` (`TOLOOONG` → `tolong`), normalisasi informal dari kamus (`udh` → `sudah`, `rmh` → `rumah`), emoji → kata (`😭` → `emo_menangis`), URL → `tok_url`, hashtag → kata terpisah (`BanjirParah` → `banjir parah`), dan tanda baca dibuang saat tokenisasi.

??? success "Jawaban 3"
    ```text title="Output nyata"
    ['tidak', 'neg_ada', 'korban', 'jiwa']
    ```

    Kata sesudah `tidak` diberi awalan `neg_`. Fitur `neg_ada` berbeda dari `ada`, sehingga model dapat membedakan "ada korban" dari "tidak ada korban". Pada data ini efeknya kecil dan belum terbukti ([Tahap D](../proyek-klasifikasi-bencana/tahap-d-preprocessing.md)).

??? success "Jawaban 4"
    ```text title="Output nyata"
    'tidak' dibuang stopword Sastrawi? True
    ```

    Ya (`True`). Membuang `tidak` dari "tidak ada korban" menghasilkan "ada korban", yang artinya berlawanan. Sebab itu proyek memakai daftar stopword konservatif atau tidak membuang negasi.

??? success "Jawaban 5"
    ```text title="Output nyata"
    kosakata: ['air', 'bantuan', 'kirim', 'masuk', 'naik', 'rumah', 'tolong']
    [[1 0 0 1 0 1 0]
     [1 0 0 0 1 0 1]
     [0 1 1 0 0 0 2]]
    ```

    Kosakata terurut abjad: `air, bantuan, kirim, masuk, naik, rumah, tolong` (7 kata). Baris dokumen ke-3 `[0 1 1 0 0 0 2]`: `tolong` muncul dua kali. Matriks berbentuk (3 dokumen × 7 kata), sebagian besar nol: itu sebabnya disimpan sebagai matriks jarang pada korpus besar.

??? success "Jawaban 6"
    ```python title="Kunci"
    --8<-- "latihan/solusi_level_2_3.py:idf_tangan"
    ```

    ```text title="Output nyata"
    IDF 'tolong' dengan tangan : 1.2877
    IDF 'tolong' dari sklearn  : 1.2877
    IDF 'air' dengan tangan    : 1.2877
    TF-IDF dokumen 3, kata 'tolong' (tf=2): 2.5754 = 2 x IDF
    ```

    $n=3$ dokumen; `tolong` muncul di 2 dokumen ($\mathrm{df}=2$): $\ln\frac{1+3}{1+2}+1=\ln1{,}333+1=1{,}2877$. Hasil dengan tangan sama dengan `TfidfVectorizer.idf_`. TF-IDF dokumen ke-3 = TF × IDF = $2\times1{,}2877=2{,}5754$. `air` juga df=2, sehingga IDF-nya sama dengan `tolong`: IDF hanya bergantung pada **jumlah dokumen yang memuat kata**, bukan pada seberapa sering dalam satu dokumen. Perhatikan bahwa scikit-learn secara bawaan menormalkan tiap baris (norma L2); kita mematikannya dengan `norm=None` agar angka sama dengan hitungan tangan.

??? success "Jawaban 7"
    ```text title="Output nyata"
    ['ada', 'ada korban', 'jiwa', 'korban', 'korban jiwa', 'tidak', 'tidak ada']
    ```

    Unigram: `tidak, ada, korban, jiwa`. Bigram: `tidak ada, ada korban, korban jiwa`. Unigram `ada` muncul di kedua kalimat dan tidak membedakannya; bigram `tidak ada` hanya muncul pada kalimat pertama dan membawa negasi. Harganya: kosakata membesar dengan cepat dan matriks makin jarang.

??? success "Jawaban 8"
    Tidak ada kunci tunggal. Jawaban yang baik memuat: (a) hipotesis spesifik ("normalisasi informal menaikkan recall pada pos bergaya informal"), (b) pembagian per kejadian/kelompok dan transformasi korpus di dalam pipeline, (c) metrik kelas Emergency dan selang ketidakpastian, (d) rencana bila hasil sama: laporkan "tidak terbukti berbeda", pilih yang lebih sederhana, dan uji pada data bergaya lain. Contoh nyata hasil sama ada di Tahap D: "minimal" dan "dasar" identik.

## Kuis gabungan

**1.** Mengapa IDF `tolong` sama dengan IDF `air` pada korpus soal 5?

??? success "Jawaban"
    Keduanya muncul di 2 dari 3 dokumen; IDF hanya bergantung pada jumlah dokumen yang memuat kata.

**2.** Bahaya apa dari memakai stopword Sastrawi tanpa pemeriksaan?

??? success "Jawaban"
    Daftar itu memuat `tidak`, sehingga makna negasi hilang.

**3.** Apa itu *data leakage* pada TF-IDF?

??? success "Jawaban"
    `fit` kosakata/IDF pada data yang mencakup data uji, sehingga statistik uji ikut memengaruhi fitur latih.

## Checkpoint praktis Level 2–3

- [ ] Saya dapat menelusuri satu pos melalui langkah preprocessing dan menjelaskan tiap langkah.
- [ ] Saya dapat menghitung IDF dan TF-IDF dengan tangan dan mencocokkannya dengan scikit-learn.
- [ ] Saya dapat menjelaskan mengapa `tidak` tidak boleh dibuang sembarangan.
- [ ] Saya dapat menyebut risiko kebocoran dari langkah yang mempelajari korpus.
- [ ] Saya dapat menjelaskan trade-off n-gram.

## Materi berikutnya

[Latihan Level 4–5](level-4-5.md)
