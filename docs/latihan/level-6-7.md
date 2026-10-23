# Latihan Level 6–7: Deep Learning dan Deployment

!!! abstract "Info latihan"
    **Tingkat kesulitan:** Menengah–lanjut. **Estimasi waktu:** 240 menit.
    **Cakupan:** [Level 6](../level-6-deep-learning/index.md) dan [Level 7](../level-7-advanced-nlp/index.md). Kode kunci: `examples/latihan/solusi_level_6_7.py` (ringan; tanpa PyTorch). Soal bertanda **[berat]** membutuhkan `requirements-dl.txt`.

## Soal

Tingkat: ★ konseptual, ★★ membaca/mengisi kode, ★★★ menulis/mendebug, ★★★★ mini-proyek.

**1. (★ Konseptual)** Sebutkan dua hal yang dikerjakan manusia pada pipeline TF-IDF yang dipelajari model pada deep learning. Kapan model klasik masih pilihan yang masuk akal?

**2. (★★ Hitungan)** Hitung kosinus $a=(1,1)$ dan $b=(2,0)$ serta sudutnya. Hitung juga softmax dari $(0,\ \ln2,\ \ln3)$.

**3. (★★ Attention)** Dengan $Q=[1,0]$, $K=\{[1,0],[0,1]\}$, $V=\{[10,0],[0,10]\}$, hitung bobot attention dan keluarannya dengan tangan.

**4. (★★★ Gradient check)** Mengapa gradient check memakai selisih relatif berbasis norma per tensor? Apa yang terjadi bila kita merusak satu bobot sebelum memeriksa?

**5. (★★★ Drift)** Hitung PSI untuk $p=(0{,}5;0{,}3;0{,}2)$ dan $q=(0{,}3;0{,}3;0{,}4)$. Lalu jelaskan mengapa PSI 0,142 pada dua sampel dari distribusi yang sama bukan bukti drift.

**6. (★★★ Tes API)** Tulis tes yang memastikan: teks tanpa kejadian ("pembangunan tanggul") berlabel Non-Emergency dan teks 1.001 karakter ditolak dengan 422.

**7. (★★★ Debugging)** [berat] `12_finetune_indobert.py` mengeluarkan peringatan "`num_labels=2` incompatible with the `id2label` map of length 5". Apakah ini kesalahan? Bagaimana skrip menanganinya, dan apa risikonya jika tidak ditangani?

**8. (★★★★ Mini-proyek)** [berat] Jalankan `13_ulang_seed.py` untuk lima seed, lalu tulis paragraf perbandingan IndoBERT dan Linear SVM yang jujur: sertakan rentang, ukuran set, dan apa yang **tidak** dapat disimpulkan.

## Kunci jawaban dan pembahasan

??? success "Jawaban 1"
    Manusia merancang fitur: pembersihan, tokenisasi, pembobotan TF-IDF. Deep learning mempelajari embedding dan lapisan tersembunyi dari data. Model klasik tetap masuk akal bila data kecil dan bertemplat, bila kata kunci/frasa sudah memisahkan kelas, bila komputasi terbatas, atau bila penjelasan sederhana (koefisien kata) dibutuhkan. Keputusan akhir harus berdasarkan pengukuran dengan protokol yang sama.

??? success "Jawaban 2"
    ```python title="Kunci"
    --8<-- "latihan/solusi_level_6_7.py:vektor"
    ```

    ```text title="Output nyata"
    kosinus: 0.7071 | sudut (derajat): 45.0
    softmax(0, ln2, ln3): [0.167 0.333 0.5  ]
    ```

    $a\cdot b=1\cdot2+1\cdot0=2$, $\lVert a\rVert=\sqrt2$, $\lVert b\rVert=2$, kosinus $=2/(2\sqrt2)=0{,}7071$, sudut 45°. Softmax: $e^0=1$, $e^{\ln2}=2$, $e^{\ln3}=3$, jumlah 6, hasil $(1/6;2/6;3/6)=(0{,}167;0{,}333;0{,}5)$.

??? success "Jawaban 3"
    ```python title="Kunci"
    --8<-- "latihan/solusi_level_6_7.py:atensi"
    ```

    ```text title="Output nyata"
    bobot: [[0.67 0.33]] | keluaran: [[6.698 3.302]]
    ```

    Skor $QK^\top=(1,0)$, dibagi $\sqrt{d_k}=\sqrt2$: $(0{,}707;0)$. Softmax: $e^{0{,}707}/(e^{0{,}707}+1)=2{,}028/3{,}028=0{,}670$ dan $0{,}330$. Keluaran $=0{,}670\cdot[10,0]+0{,}330\cdot[0,10]=[6{,}70;3{,}30]$. Query condong ke key pertama sehingga value pertama mendominasi, tetapi tidak 100% karena softmax.

??? success "Jawaban 4"
    ```python title="Kunci"
    --8<-- "latihan/solusi_level_6_7.py:gradien"
    ```

    ```text title="Output nyata"
    selisih gradien: 1.4e-11
    setelah bobot diubah, turunan tetap benar: True
    ```

    Rasio per elemen menjadi berisik pada gradien yang hampir nol (mis. neuron ReLU mati: kedua sisi ≈ 1e-11, rasionya bisa besar). Norma per tensor menimbang elemen besar lebih dominan dan stabil. Mengubah satu **bobot** (nilai parameter) tidak merusak pemeriksaan, karena turunan tetap benar untuk titik parameter yang baru; yang merusak pemeriksaan adalah menulis **turunan** yang salah (misalnya lupa mengalikan dengan turunan ReLU). Tes `test_gradien_analitik_cocok_dengan_numerik` menjaga ini.

??? success "Jawaban 5"
    ```python title="Kunci"
    --8<-- "latihan/solusi_level_6_7.py:psi"
    ```

    ```text title="Output nyata"
    PSI (0,5/0,3/0,2 -> 0,3/0,3/0,4) ≈ 0.241
    PSI sampel sama distribusi: 0.02 | geser +1 simpangan baku: 1.011
    ```

    PSI contoh = 0,241 (hitungan di [Pemantauan Drift](../level-7-advanced-nlp/pemantauan-drift.md)). Dua sampel dari distribusi yang sama tetap berbeda sedikit karena pengambilan sampel acak; semakin kecil sampel, semakin besar PSI derau. Pada 1000 titik nilainya 0,020; pada jendela 48 teks, persentil ke-95 derau mencapai 0,792. Geseran +1 simpangan baku memberi PSI 1,011, jauh di atas derau. Ambang dari konvensi (0,1/0,25) harus diuji pada ukuran jendela yang dipakai.

??? success "Jawaban 6"
    ```python title="Kunci"
    --8<-- "latihan/solusi_level_6_7.py:api"
    ```

    ```text title="Output nyata"
    200 Non-Emergency | skor negatif: True
    teks 1001 karakter -> 422
    ```

    `TestClient` memanggil aplikasi di proses yang sama (tanpa port). `pastikan_artefak(folder)` membuat artefak di folder sementara agar tes tidak bergantung pada berkas lokal. Skor Non-Emergency negatif karena ambang bawaan 0. Teks 1.001 karakter melanggar `max_length=1000` sehingga 422.

??? success "Jawaban 7"
    Bukan kesalahan; peringatan itu jinak. Konfigurasi bawaan IndoBERT p1 memuat `id2label` generik untuk 5 kelas (`LABEL_0` … `LABEL_4`), sedangkan kita meminta 2 kelas. Diperiksa langsung dengan `AutoConfig`: dengan `num_labels=2` hasilnya `{0: 'LABEL_0', 1: 'LABEL_1'}` dan `num_labels` = 2, jadi model dibangun dengan 2 keluaran seperti yang kita mau. Skrip lalu menimpa `id2label`/`label2id` menjadi `Non-Emergency`/`Emergency` agar model yang disimpan terbaca manusia. Jika tidak ditimpa, bobot tetap benar, tetapi keluaran seperti pipeline Hugging Face menampilkan `LABEL_1` alih-alih `Emergency`, yang mudah disalahartikan. Peringatan lain ("classifier ... MISSING/newly initialized") juga normal: kepala klasifikasi baru dan akan dilatih.

??? success "Jawaban 8"
    Tidak ada kunci angka tunggal karena hasil bergantung pada mesin. Kerangka paragraf yang jujur ada di [Fine-tuning dan Transfer Learning](../level-6-deep-learning/fine-tuning-transfer-learning.md) dan hasil penulis ada di halaman yang sama. Wajib memuat: rata-rata dan rentang antar seed; 24 Emergency di tulis-tangan; satu pelabel; SVM dilatih pada data latih yang sama; tidak ada klaim operasional.

## Kuis gabungan

**1.** Mengapa attention dibagi $\sqrt{d_k}$?

??? success "Jawaban"
    Agar skala hasil kali titik tidak tumbuh dengan dimensi dan softmax tidak terlalu tajam.

**2.** Mengapa API mengembalikan `skor` bukan `probabilitas`?

??? success "Jawaban"
    Skor keputusan SVM bukan probabilitas terkalibrasi; menamainya probabilitas adalah klaim yang tidak valid.

**3.** Apa yang tidak dibuktikan checksum model?

??? success "Jawaban"
    Bahwa berkas aman; hanya bahwa ia tidak berubah sejak checksum dibuat.

## Checkpoint praktis Level 6–7

- [ ] Saya dapat menghitung kosinus, softmax, dan satu langkah attention dengan tangan.
- [ ] Saya dapat menjelaskan gradien menghilang dan peran gerbang LSTM.
- [ ] Saya dapat menjelaskan fine-tuning, seed, dan mengapa melaporkan rentang.
- [ ] Saya dapat menulis tes API dengan `TestClient`.
- [ ] Saya dapat menjelaskan PSI dan batasnya pada sampel kecil.
- [ ] Saya dapat menyebut tiga syarat sebelum model boleh dipakai di luar pembelajaran.

## Materi berikutnya

[Latihan dan kuis proyek](proyek.md)
