# Glosarium

Istilah dipakai secara konsisten di seluruh situs. Istilah bahasa Inggris yang
umum dipertahankan, disertai padanan atau penjelasan Indonesia. Glosarium
ditambah seiring materi baru ditulis.

## A–F

Artificial Intelligence (AI)
:   Bidang yang membuat sistem komputer melakukan tugas yang biasanya memerlukan kecerdasan manusia.

Baseline
:   Model atau aturan sederhana sebagai pembanding minimum. Model rumit hanya bermakna bila mengalahkan baseline.

Case folding
:   Menyeragamkan huruf besar/kecil (biasanya menjadi huruf kecil).

Class imbalance
:   Jumlah contoh antarkelas sangat tidak seimbang, misalnya Emergency jauh lebih sedikit daripada Non-Emergency.

Dataset
:   Kumpulan contoh data. Dalam proyek ini, tiap baris berisi satu postingan (`text`) dan labelnya (`label`).

Data leakage
:   Informasi dari data uji (atau masa depan) ikut memengaruhi pelatihan sehingga skor evaluasi terlalu optimistis.

Deep learning
:   Cabang machine learning yang memakai jaringan saraf berlapis banyak.

Document (dokumen)
:   Satu unit teks yang dianalisis. Di proyek ini: satu postingan.

Emergency
:   Label untuk postingan yang melaporkan kejadian darurat yang sedang atau baru terjadi, atau meminta bantuan. Definisi operasional lengkap ada di [Masalah Emergency](level-0-orientasi/masalah-emergency.md).

Fitur (feature)
:   Representasi numerik dari suatu contoh yang menjadi masukan model.

## I–N

Inference (inferensi)
:   Memakai model yang sudah dilatih untuk memprediksi data baru.

Label
:   Jawaban yang benar untuk suatu contoh (target `y`), misalnya `Emergency`.

Machine Learning (ML)
:   Pendekatan di mana model belajar pola dari data, bukan diprogram dengan aturan eksplisit.

Model
:   Fungsi yang dipelajari dari data untuk memetakan fitur ke prediksi.

Natural Language Processing (NLP)
:   Bidang yang memungkinkan komputer memproses dan memahami bahasa manusia.

Non-Emergency
:   Label untuk semua postingan lain: berita, opini, informasi lama, peringatan umum, dan topik tak terkait.

## P–Z

Preprocessing
:   Rangkaian transformasi teks sebelum dijadikan fitur, misalnya case folding dan pembersihan URL.

Recall
:   Dari semua contoh positif yang sebenarnya, berapa proporsi yang berhasil ditemukan model.

Precision
:   Dari semua yang diprediksi positif, berapa proporsi yang benar-benar positif.

Text mining
:   Proses menggali informasi dan pola dari kumpulan teks; beririsan dengan NLP.

Token
:   Satuan teks hasil pemecahan, biasanya kata, subkata, atau karakter.

Training (pelatihan)
:   Proses model menyesuaikan parameter berdasarkan data berlabel.

Virtual environment
:   Lingkungan Python terisolasi per proyek agar versi library tidak bertabrakan.
