# Latihan Level 4–5: Model dan Evaluasi

!!! abstract "Info latihan"
    **Tingkat kesulitan:** Menengah. **Estimasi waktu:** 180 menit.
    **Cakupan:** [Level 4](../level-4-machine-learning/index.md) dan [Level 5](../level-5-evaluasi/index.md). Kode kunci: `examples/latihan/solusi_level_4_5.py` (diuji oleh `tests/test_latihan.py`). Data: sintetis.

## Soal

Tingkat: ★ konseptual, ★★ membaca/mengisi kode, ★★★ menulis/mendebug, ★★★★ mini-proyek.

**1. (★ Konseptual)** Mengapa data dibagi menjadi latih, validasi, dan uji? Apa yang salah bila kita memilih model terbaik menurut skor uji?

**2. (★★ Hitungan)** Sebuah model pada tulis-tangan menghasilkan TP = 15, FP = 0, FN = 9, TN = 24. Hitung akurasi, presisi, recall, dan F1 kelas Emergency.

**3. (★★ Baseline)** Data 1.000 pos dengan 5% Emergency. Model "selalu Non-Emergency" mendapat akurasi berapa, dan presisi/recall Emergency berapa? Apa pelajaran untuk memilih metrik?

**4. (★★★ Menulis fungsi)** Tulis `hitung_metrik(tp, fp, fn, tn)` yang tidak melempar galat saat pembagi nol. Uji pada soal 2, 3, dan kasus semua nol.

**5. (★★★ Kebocoran)** Bandingkan Linear SVM dengan pembagian acak per baris (80/20) dan pembagian per `event_id`. Mana yang lebih tinggi dan mengapa? Apakah selisih yang kecil berarti tidak ada kebocoran?

**6. (★★★ Ambang)** Dengan SVM pada tulis-tangan, hitung recall dan presisi Emergency serta jumlah FP untuk ambang 0, −0,2, −0,4. Apakah boleh memilih −0,2 sebagai ambang produksi karena tampak terbaik?

**7. (★★★ Debugging)** Rekan Anda melaporkan "F1 makro 1,000" dari `TfidfVectorizer().fit_transform(semua_teks)` lalu `train_test_split`. Temukan dua masalah.

**8. (★★★★ Mini-proyek)** Tulis ringkasan satu halaman evaluasi baseline: tabel metrik dengan selang ketidakpastian, tiga FN dan tiga FP yang dianalisis, dan paragraf "apa yang tidak dapat disimpulkan".

## Kunci jawaban dan pembahasan

??? success "Jawaban 1"
    Latih untuk mempelajari parameter; validasi untuk memilih model/hyperparameter/ambang; uji untuk menaksir performa akhir **sekali**. Memilih model terbaik menurut skor uji membuat uji ikut dipakai dalam seleksi (*data snooping*): skornya menjadi terlalu optimistis dan tidak lagi menaksir performa pada data baru.

??? success "Jawaban 2"
    ```python title="Kunci"
    --8<-- "latihan/solusi_level_4_5.py:metrik"
    ```

    ```text title="Output nyata"
    {'akurasi': 0.812, 'presisi': 1.0, 'recall': 0.625, 'f1': 0.769}
    ```

    Presisi $=15/(15+0)=1{,}0$; recall $=15/(15+9)=0{,}625$; akurasi $=(15+24)/48=0{,}8125$; F1 $=2\cdot1{,}0\cdot0{,}625/(1{,}0+0{,}625)=0{,}769$. Presisi sempurna dengan recall 0,625 berarti semua yang ditandai benar, tetapi 9 pesan darurat terlewat. Itulah yang dilaporkan Level 5.

??? success "Jawaban 3"
    ```text title="Output nyata"
    {'akurasi': 0.95, 'presisi': 0.0, 'recall': 0.0, 'f1': 0.0}
    ```

    Akurasi **0,95** (950 dari 1.000) tanpa menemukan satu pun Emergency (recall 0, presisi 0 karena tidak ada prediksi positif; konvensi kita mengembalikan 0). Akurasi menipu pada kelas timpang; gunakan presisi/recall/F1 kelas Emergency dan bandingkan dengan baseline.

??? success "Jawaban 4"
    Lihat fungsi pada Jawaban 2: `bagi = lambda a, b: a / b if b else 0.0` mengembalikan 0.0 bila pembagi 0. Uji `hitung_metrik(0, 0, 0, 0)` menghasilkan semua 0 tanpa `ZeroDivisionError`. Catatan desain: mengembalikan 0.0 untuk presisi tak terdefinisi adalah konvensi (scikit-learn menyebutnya `zero_division`); laporan harus menyebut konvensi itu.

??? success "Jawaban 5"
    ```text title="Output nyata"
    pembagian acak per baris : F1 makro 1.000, recall E 1.000
    pembagian per event_id   : F1 makro 0.980, recall E 1.000
    ```

    Pembagian acak per baris mendapat F1 makro **1,000** vs **0,980** per `event_id`. Pembagian acak lebih tinggi karena pos dari kejadian yang sama (hampir identik) tersebar di latih dan uji sehingga model "mengenali" bukan "menggeneralisasi". Selisih yang kecil **tidak** berarti tidak ada kebocoran: pembagian per `event_id` pun masih meninggalkan 59 dari 61 templat di kedua sisi ([Tahap C](../proyek-klasifikasi-bencana/tahap-c-eda.md)). Satu pembagian dan satu seed juga tidak cukup untuk menaksir selisih.

??? success "Jawaban 6"
    ```python title="Kunci (kode)"
    --8<-- "latihan/solusi_level_4_5.py:ambang"
    ```

    ```text title="Output nyata"
    ambang +0.0: recall E 0.625 | presisi E 1.000 | FP 0
    ambang -0.2: recall E 0.917 | presisi E 1.000 | FP 0
    ambang -0.4: recall E 0.917 | presisi E 0.880 | FP 3
    ```

    Ambang −0,2 menaikkan recall dari 0,625 menjadi 0,917 tanpa FP, dan −0,4 mempertahankan recall 0,917 dengan 3 FP (presisi 0,880). **Tidak boleh** memilih −0,2 sebagai ambang produksi: kita memilihnya dengan melihat set evaluasi yang sama (*data snooping*), dan set itu kecil (24 Emergency) dan dilabeli satu orang. Ambang harus dipilih pada data validasi yang mewakili penggunaan nyata dan diuji pada data terpisah ([Kalibrasi dan Threshold](../level-7-advanced-nlp/kalibrasi-threshold.md) menunjukkan ambang dari validasi gagal pada gaya berbeda).

??? success "Jawaban 7"
    (1) `fit_transform` pada **semua** teks mempelajari kosakata dan IDF dari data uji sebelum pemisahan: kebocoran. Letakkan TF-IDF di dalam `Pipeline` dan `fit` hanya pada data latih. (2) `train_test_split` acak per baris pada data yang pos-posnya berkelompok per kejadian menaruh pos mirip di kedua sisi: kebocoran antarpostingan. Gunakan pembagian berkelompok. F1 makro 1,000 pada data seperti ini adalah tanda bahaya, bukan prestasi.

??? success "Jawaban 8"
    Tidak ada kunci tunggal. Periksa: tabel dihasilkan dari kode; ada selang bootstrap; FN dan FP dibaca dan dikelompokkan dengan hipotesis; paragraf batas klaim menyebut data sintetis, 48 teks tulis-tangan, satu pelabel, satu seed, dan tidak adanya ambang produksi. Contoh format ada di [Tahap F](../proyek-klasifikasi-bencana/tahap-f-evaluasi.md).

## Kuis gabungan

**1.** Mengapa recall Emergency diprioritaskan, tetapi presisi tetap dilaporkan?

??? success "Jawaban"
    FN (pesan darurat terlewat) berdampak serius, tetapi FP menghabiskan sumber daya peninjau yang terbatas.

**2.** Apa risiko `TfidfVectorizer().fit_transform` pada seluruh data?

??? success "Jawaban"
    Kebocoran statistik uji ke fitur latih.

**3.** Apakah ambang yang tampak terbaik pada set evaluasi boleh dipakai di produksi?

??? success "Jawaban"
    Tidak; itu data snooping dan set evaluasi tidak mewakili penggunaan nyata.

## Checkpoint praktis Level 4–5

- [ ] Saya dapat menghitung presisi, recall, F1, dan akurasi dari confusion matrix.
- [ ] Saya dapat menjelaskan mengapa akurasi menipu pada kelas timpang.
- [ ] Saya dapat menjelaskan dua jenis kebocoran dan cara mencegahnya.
- [ ] Saya dapat menjelaskan trade-off ambang dan mengapa tidak memilihnya dari set evaluasi.
- [ ] Saya dapat menulis paragraf "yang tidak dapat disimpulkan".

## Materi berikutnya

[Latihan Level 6–7](level-6-7.md)
