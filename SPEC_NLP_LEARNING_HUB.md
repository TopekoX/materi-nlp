# MASTER SPECIFICATION — NLP LEARNING HUB

> Dokumen spesifikasi proyek. Aturan kerja yang stabil ada di [`CLAUDE.md`](CLAUDE.md);
> kondisi dan status implementasi ada di [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md).
> Bila ada pertentangan aturan pedagogis, `CLAUDE.md` yang lebih rinci menang
> (lihat bagian "Hubungan dengan CLAUDE.md" di bawah).
>
> Dokumen ini berada di akar repository dan **tidak** dipublikasikan oleh MkDocs.

## Hubungan dengan CLAUDE.md

- Spesifikasi ini mendefinisikan **apa** yang dibangun: kurikulum, proyek, struktur, dan tahapan.
- `CLAUDE.md` mendefinisikan **bagaimana** bekerja: filosofi mengajar, aturan penjelasan kode,
  struktur halaman, integritas data, dan definisi selesai.
- Format halaman pada bagian 7 di bawah adalah minimum. `CLAUDE.md` bagian 5 memperluasnya
  (misalnya tingkat kesulitan, kunci jawaban, dan glosarium istilah baru per halaman).

## 1. Peran dan tujuan

Bertindak sebagai Senior NLP Engineer, Python Educator, Machine Learning Researcher, Technical Writer, dan MkDocs Documentation Engineer.

Bangun sebuah website pembelajaran berjudul:

**NLP Learning Hub: Natural Language Processing dengan Python**

Bahasa seluruh materi adalah Bahasa Indonesia. Istilah teknis yang umum digunakan secara internasional boleh dipertahankan dalam bahasa Inggris, disertai penjelasan dalam bahasa Indonesia ketika pertama kali muncul.

Website harus ditujukan kepada pemula yang belum memiliki pengetahuan NLP dan membawa pembelajar secara bertahap hingga mampu mengembangkan, mengevaluasi, dan melakukan deployment model NLP.

Gunakan studi kasus utama:

**Klasifikasi Teks Twitter/X untuk Identifikasi Pesan Kebencanaan: Emergency vs Non-Emergency.**

Gunakan Python sebagai bahasa pemrograman utama. Gunakan Jupyter Notebook untuk eksperimen dan MkDocs sebagai platform dokumentasi.

Repository MkDocs dan template sudah tersedia. Jangan membuat proyek baru sebelum memeriksa repository yang ada.

## 2. Aturan sebelum implementasi

Lakukan audit repository terlebih dahulu.

1. Periksa struktur direktori, `mkdocs.yml`, `requirements.txt` atau `pyproject.toml`, theme, plugin, CSS, JavaScript, navigation, dan seluruh konfigurasi yang relevan.
2. Identifikasi versi MkDocs dan theme yang benar-benar digunakan.
3. Pertahankan identitas dan komponen template yang masih relevan.
4. Jangan menghapus, mengganti, atau menimpa konfigurasi dan materi yang sudah ada tanpa alasan teknis yang jelas.
5. Tentukan direktori konten yang sesuai dengan konfigurasi aktual repository.
6. Buat `docs/IMPLEMENTATION_PLAN.md` atau lokasi dokumentasi rencana yang sesuai dengan struktur repository. Catat kondisi awal, perubahan yang direncanakan, dan tahapan implementasi.
7. Jika repository memiliki perubahan Git yang belum di-commit, jangan menimpa perubahan tersebut.
8. Jangan menginstal dependensi baru secara massal jika belum diperlukan.
9. Setelah audit, lanjutkan implementasi secara bertahap. Jangan berhenti hanya pada laporan audit.

Jika ada keputusan kecil yang tidak memerlukan konfirmasi, gunakan pilihan yang paling sederhana, konsisten, dan mudah dipelihara.

## 3. Prinsip pedagogis

Semua materi wajib mengikuti prinsip berikut.

- Asumsikan pembaca adalah pemula.
- Jelaskan pengertian, tujuan, intuisi, cara kerja, kelebihan, keterbatasan, dan kapan suatu teknik digunakan.
- Jelaskan istilah teknis sebelum menggunakannya dalam pembahasan.
- Gunakan contoh teks berbahasa Indonesia yang realistis.
- Mulai dari contoh sederhana, lalu tingkatkan kompleksitas secara bertahap.
- Setiap contoh kode Python harus disertai penjelasan kode, input, output yang diharapkan, dan interpretasi hasil.
- Hindari kode yang terlalu panjang sebelum konsep dasarnya dipahami.
- Gunakan library standar Python sebelum memperkenalkan library khusus ketika pendekatan tersebut membantu pemahaman.
- Bedakan contoh ilustratif, eksperimen, dan implementasi yang siap digunakan.
- Jangan mengklaim suatu kode sudah diuji jika belum benar-benar menjalankannya.
- Jelaskan kesalahan umum, debugging, dan cara memperbaikinya.
- Jangan mengasumsikan hasil eksperimen, skor model, atau jumlah dataset yang belum dihitung.
- Gunakan istilah dan definisi secara konsisten di seluruh website.

## 4. Struktur direktori materi

Sesuaikan lokasi berikut dengan direktori dokumentasi yang ditemukan pada repository. Nama di bawah adalah struktur konten yang direkomendasikan, bukan perintah untuk mengganti konfigurasi template.

```text
materi-nlp/
├── index.md
├── panduan-belajar.md
├── glosarium.md
├── referensi.md
├── level-0-orientasi/
├── level-1-python/
├── level-2-fondasi-teks/
├── level-3-representasi-teks/
├── level-4-machine-learning/
├── level-5-evaluasi/
├── level-6-deep-learning/
├── level-7-advanced-nlp/
├── proyek-klasifikasi-bencana/
├── latihan/
└── lampiran/
```

Setiap direktori level berisi `index.md` dan halaman materi yang relevan.

Gunakan nama file dan URL yang konsisten, singkat, deskriptif, serta menggunakan huruf kecil dan tanda hubung.

Jangan membuat satu file Markdown yang berisi seluruh kurikulum. Setiap konsep utama harus memiliki halaman tersendiri.

## 5. Kurikulum wajib

### Level 0 — Orientasi NLP

Buat materi:

1. Apa itu Artificial Intelligence, Machine Learning, Deep Learning, NLP, dan Text Mining?
2. Hubungan NLP dengan Machine Learning.
3. Contoh penerapan NLP dalam kehidupan nyata.
4. Cara kerja sistem klasifikasi teks.
5. Memahami masalah klasifikasi Emergency dan Non-Emergency.
6. Mengenal teks media sosial, bahasa informal, singkatan, emoji, hashtag, URL, dan mention.
7. Pengantar dataset, fitur, label, model, training, dan inference.
8. Persiapan Python, virtual environment, pip, Jupyter Notebook, dan Git.
9. Instalasi dan verifikasi lingkungan pengembangan.
10. Proyek mini pertama: memahami dan mengelompokkan contoh teks secara manual.

### Level 1 — Fondasi Python untuk NLP

Materi wajib:

1. Variabel dan tipe data.
2. String dan operasi teks.
3. Indexing dan slicing.
4. List, tuple, set, dan dictionary.
5. Kondisional.
6. Perulangan.
7. Function dan parameter.
8. Import dan modul.
9. Exception handling.
10. Membaca dan menulis file teks.
11. CSV dan JSON.
12. Dasar NumPy.
13. Dasar pandas.
14. Missing values dan duplikasi data.
15. Dasar regex menggunakan `re`.
16. Debugging dan pengujian kode sederhana.

Setiap materi menyertakan contoh yang berkaitan dengan teks laporan kebencanaan.

### Level 2 — Fondasi Teks dan Text Preprocessing

Materi wajib:

1. Struktur teks dan karakter.
2. Unicode dan encoding UTF-8.
3. Token, kalimat, kata, dan dokumen.
4. Sentence segmentation.
5. Word tokenization.
6. Case folding.
7. Pembersihan URL, mention, hashtag, dan karakter khusus.
8. Penanganan emoji dan emotikon.
9. Normalisasi bahasa informal Indonesia.
10. Stopwords dan keterbatasannya.
11. Stemming menggunakan Sastrawi.
12. Lemmatization dan perbedaannya dengan stemming.
13. Penanganan tanda baca.
14. Negasi seperti "tidak", "belum", "bukan", dan "jangan".
15. Pengulangan huruf dan kata.
16. Typographical errors dan variasi ejaan.
17. Normalisasi angka, waktu, dan lokasi.
18. Perbandingan pipeline preprocessing.
19. Data leakage akibat preprocessing yang keliru.
20. Membuat pipeline preprocessing yang dapat diuji.

Jangan menganggap seluruh tanda baca, angka, emoji, hashtag, URL, atau kata umum harus selalu dihapus. Jelaskan bahwa keputusan preprocessing bergantung pada tujuan klasifikasi dan evaluasi empiris.

### Level 3 — Exploratory Text Analysis dan Representasi Fitur

Materi wajib:

1. Statistik dasar korpus.
2. Distribusi panjang teks.
3. Frekuensi kata.
4. Vocabulary dan document frequency.
5. Word n-gram dan character n-gram.
6. Bag of Words.
7. TF-IDF dan intuisi matematisnya.
8. Sparse matrix.
9. One-hot encoding dan keterbatasannya.
10. Feature engineering untuk teks kebencanaan.
11. Representasi teks dengan scikit-learn.
12. Perbandingan fitur sebelum dan sesudah preprocessing.
13. Menghindari vocabulary leakage.
14. Latihan analisis dataset.

### Level 4 — Machine Learning untuk Klasifikasi Teks

Materi wajib:

1. Supervised learning.
2. Definisi fitur X dan target y.
3. Label encoding.
4. Train-validation-test split.
5. Stratified splitting.
6. Pipeline scikit-learn.
7. Multinomial Naive Bayes.
8. Logistic Regression.
9. Linear Support Vector Machine.
10. Perbandingan algoritma.
11. Hyperparameter dan tuning.
12. GridSearchCV.
13. Cross-validation.
14. Random seed dan reproducibility.
15. Model serialization.
16. Prediksi teks baru.
17. Kesalahan umum dalam training.
18. Membandingkan model menggunakan eksperimen yang adil.

Gunakan TF-IDF sebagai representasi fitur awal dan ketiga algoritma tersebut sebagai baseline utama. Jelaskan bahwa pemilihan model terbaik harus didasarkan pada eksperimen, bukan asumsi.

### Level 5 — Evaluasi, Error Analysis, dan Eksperimen

Materi wajib:

1. Confusion matrix.
2. True Positive, True Negative, False Positive, dan False Negative.
3. Accuracy.
4. Precision.
5. Recall.
6. F1-score.
7. Macro, micro, dan weighted averaging.
8. Class imbalance.
9. Baseline sederhana.
10. Threshold dan trade-off precision-recall.
11. ROC curve dan AUC: pengertian, kapan relevan, dan keterbatasannya.
12. Precision-recall curve.
13. Error analysis.
14. Analisis false positive dan false negative.
15. Ablation study.
16. Evaluasi robustness terhadap variasi bahasa.
17. Data leakage.
18. Ketidakpastian hasil dan reproducibility.
19. Penyusunan tabel perbandingan eksperimen.
20. Penulisan laporan eksperimen ilmiah.

Jelaskan secara khusus bahwa recall kelas Emergency dapat menjadi prioritas karena pesan darurat yang terlewat dapat berdampak serius. Namun, false positive juga harus diukur karena sumber daya respons terbatas. Jangan menetapkan threshold produksi tanpa evaluasi dan validasi yang sesuai.

### Level 6 — Deep Learning untuk NLP

Materi wajib:

1. Perbedaan machine learning klasik dan deep learning.
2. Vektor dan embedding kata.
3. Word2Vec.
4. GloVe.
5. FastText.
6. OOV dan subword.
7. Neural network dasar.
8. Forward propagation dan backpropagation.
9. Loss function dan optimizer.
10. RNN.
11. LSTM.
12. GRU.
13. Attention mechanism.
14. Transformer.
15. Positional encoding.
16. Self-attention.
17. Tokenizer modern.
18. Encoder dan decoder.
19. BERT.
20. IndoBERT.
21. Fine-tuning untuk klasifikasi teks.
22. Transfer learning.
23. Overfitting dan regularisasi.
24. Penggunaan GPU dan CPU.
25. Evaluasi model deep learning.

Gunakan PyTorch untuk menjelaskan dasar neural network dan Hugging Face Transformers untuk praktik model bahasa modern. Jelaskan dependensi dan kebutuhan komputasi sebelum contoh implementasi yang lebih berat.

### Level 7 — Advanced NLP dan Deployment

Materi wajib:

1. Arsitektur pipeline NLP untuk aplikasi nyata.
2. Optimasi preprocessing dan inference.
3. Model calibration dan threshold selection.
4. Explainable NLP dan interpretabilitas.
5. Analisis bias dan fairness.
6. Robustness dan out-of-distribution data.
7. Model versioning dan eksperimen.
8. Penyimpanan model dan tokenizer.
9. REST API menggunakan FastAPI.
10. Validasi request dan response.
11. Logging dan penanganan error.
12. Batch inference.
13. Dashboard riwayat prediksi.
14. Monitoring performa dan data drift.
15. Pengujian otomatis.
16. Deployment lokal dan pengantar deployment server.
17. Keamanan dataset dan kredensial.
18. Dokumentasi model dan model card.
19. Keterbatasan sistem klasifikasi darurat.
20. Evaluasi akhir dan roadmap pengembangan.

Jangan menyatakan model sebagai sistem penentuan keadaan darurat yang sepenuhnya otomatis atau sistem yang siap menggantikan verifikasi manusia.

## 6. Proyek utama: klasifikasi kebencanaan Twitter/X

Buat satu proyek yang berkembang dari baseline sederhana menjadi sistem NLP yang lebih lengkap.

### Tahap A — Definisi masalah

Jelaskan:

- Tujuan klasifikasi.
- Definisi operasional Emergency dan Non-Emergency.
- Unit analisis berupa satu postingan.
- Kriteria inklusi dan eksklusi.
- Contoh kasus ambigu.
- Aturan anotasi dan penanganan label yang tidak pasti.
- Perbedaan antara laporan kejadian, permintaan bantuan, berita, opini, informasi lama, dan peringatan umum.

Definisi label harus eksplisit dan dapat diterapkan oleh anotator yang berbeda. Jangan menyamakan semua postingan yang mengandung kata "gempa", "banjir", atau "tolong" sebagai Emergency.

### Tahap B — Dataset

Gunakan CSV dengan skema minimal:

- `text`: isi teks.
- `label`: Emergency atau Non-Emergency.

Kolom metadata seperti `source_id`, `event_id`, `created_at`, dan `split_group` boleh digunakan bila tersedia, sah untuk digunakan, dan memang diperlukan. Jangan mewajibkan pengungkapan identitas pengguna.

Sediakan dataset sintetis kecil untuk latihan awal, dengan label yang jelas bersifat ilustratif dan bukan ground truth untuk evaluasi ilmiah.

Untuk dataset penelitian nyata, gunakan dataset yang disediakan pengguna atau sumber yang penggunaannya telah diperiksa. Jangan melakukan scraping Twitter/X atau mengunduh dataset eksternal secara otomatis tanpa instruksi dan pemeriksaan yang sesuai.

Jelaskan provenance, kualitas label, dokumentasi sumber, batasan penggunaan, privasi, dan risiko kebocoran data. Jangan memasukkan kredensial atau data pribadi ke repository.

### Tahap C — Exploratory Data Analysis

Buat notebook untuk:

- Membaca dataset.
- Memeriksa struktur dan tipe data.
- Memeriksa missing values dan duplikasi.
- Menghitung distribusi label.
- Menganalisis panjang teks.
- Menampilkan contoh teks secara aman.
- Memeriksa ketidakseimbangan kelas.
- Mengidentifikasi kemungkinan data leakage.

### Tahap D — Preprocessing

Buat fungsi preprocessing yang modular dan dapat diuji.

Bandingkan beberapa strategi preprocessing secara empiris. Jangan menetapkan satu strategi sebagai yang terbaik sebelum eksperimen.

Pastikan preprocessing yang mempelajari statistik korpus, vocabulary, atau parameter lain dilakukan di dalam pipeline training agar tidak membocorkan informasi dari test set.

### Tahap E — Modeling

Bangun baseline menggunakan:

- TF-IDF + Multinomial Naive Bayes.
- TF-IDF + Logistic Regression.
- TF-IDF + Linear SVM.

Gunakan split yang konsisten dan evaluasi yang sama untuk perbandingan model.

Jika metadata memungkinkan, jelaskan pembagian berbasis kelompok atau waktu untuk mengurangi kebocoran antarpostingan dari kejadian yang sama.

### Tahap F — Evaluasi

Buat tabel perbandingan aktual yang dihasilkan dari kode, berisi:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Macro F1.
- Waktu training bila diukur.
- Catatan kesalahan penting.

Jangan mengarang angka hasil eksperimen.

Lakukan error analysis khusus untuk false negative pada kelas Emergency dan false positive pada kelas Non-Emergency.

### Tahap G — Advanced modeling

Kembangkan proyek dengan embedding atau IndoBERT. Jelaskan perbedaan kebutuhan data, komputasi, preprocessing, training, dan evaluasinya dibandingkan baseline klasik.

Tidak wajib mengunduh model besar saat membangun dokumentasi awal. Berikan instruksi terpisah untuk eksperimen yang membutuhkan akses jaringan atau GPU.

### Tahap H — Deployment

Buat contoh aplikasi FastAPI yang menerima teks dan mengembalikan:

- Prediksi label.
- Skor model bila tersedia.
- Model version.
- Waktu prediksi bila diukur.

Jelaskan bahwa skor probabilitas hanya tersedia jika model mendukungnya secara valid. Jangan menyebut skor decision function sebagai probabilitas.

Sediakan pengujian endpoint, validasi input, penanganan error, dan contoh request-response.

## 7. Format wajib setiap halaman materi

Setiap halaman pembelajaran, dengan penyesuaian untuk halaman referensi atau lampiran, menggunakan struktur:

1. Judul materi.
2. Tujuan pembelajaran.
3. Prasyarat.
4. Pengantar dan intuisi.
5. Penjelasan konsep.
6. Contoh kontekstual kebencanaan.
7. Contoh kode Python jika relevan.
8. Penjelasan kode secara bertahap.
9. Contoh output dan interpretasi.
10. Kesalahan umum.
11. Latihan mandiri.
12. Kuis singkat beserta jawaban dan penjelasan.
13. Ringkasan.
14. Referensi yang relevan.
15. Materi selanjutnya.

Jangan mengisi bagian dengan paragraf generik hanya untuk memenuhi format. Untuk materi konseptual tanpa kode, berikan contoh, analisis kasus, atau latihan yang sesuai.

## 8. Notebook dan source code

Sediakan struktur eksperimen yang konsisten, misalnya:

```text
examples/
├── level-1-python/
├── level-2-preprocessing/
├── level-3-feature-engineering/
├── level-4-classification/
├── level-5-evaluation/
├── level-6-deep-learning/
└── disaster-classification/
```

Notebook dan script harus:

- Menggunakan nama yang deskriptif.
- Memiliki markdown penjelasan.
- Dapat dijalankan secara berurutan.
- Menggunakan relative path atau konfigurasi yang terdokumentasi.
- Memisahkan data mentah, data hasil preprocessing, dan model.
- Tidak bergantung pada path lokal yang hanya berlaku di komputer pembuat.
- Tidak mengunduh data atau model besar secara diam-diam.
- Memiliki instruksi instalasi dan cara menjalankan.

Tambahkan `requirements.txt` atau konfigurasi dependensi yang sesuai dengan pola repository. Pisahkan dependensi dasar dari dependensi deep learning jika diperlukan.

## 9. Navigasi dan tampilan MkDocs

Pertahankan theme dan identitas template yang sudah digunakan.

Buat navigasi yang mudah dipahami pemula:

- Beranda.
- Panduan Belajar.
- Level 0 sampai Level 7.
- Proyek Klasifikasi Kebencanaan.
- Latihan dan Kuis.
- Glosarium.
- Referensi.

Tambahkan landing page yang memuat deskripsi kurikulum, prasyarat, urutan belajar, capaian pembelajaran, dan tautan ke materi awal.

Gunakan komponen yang sudah tersedia di theme sebelum menambahkan plugin baru.

Periksa konsistensi heading, internal links, code blocks, tabel, gambar, dan navigasi. Jika dukungan LaTeX atau Mermaid sudah tersedia, pertahankan dan uji; jika belum, tambahkan hanya bila benar-benar diperlukan.

Jangan mengubah theme, CSS global, struktur URL, atau konfigurasi deployment secara luas tanpa kebutuhan yang jelas.

## 10. Referensi ilmiah dan dokumentasi

Gunakan dokumentasi resmi yang relevan, termasuk:

- Python.
- pandas dan NumPy.
- scikit-learn.
- NLTK atau spaCy bila digunakan.
- Sastrawi.
- PyTorch.
- Hugging Face Transformers.
- FastAPI.
- Dokumentasi MkDocs dan theme aktif.

Untuk materi ilmiah, sertakan referensi primer yang relevan ketika membahas algoritma atau arsitektur penting. Bedakan referensi akademik, dokumentasi library, dan tutorial.

Jangan mengarang judul paper, DOI, tautan, hasil penelitian, atau kutipan. Pastikan setiap referensi yang ditambahkan relevan dengan klaim yang didukungnya.

## 11. Pengujian dan quality assurance

Setelah implementasi setiap tahap:

1. Jalankan pemeriksaan build MkDocs sesuai versi dan konfigurasi aktual.
2. Perbaiki kesalahan konfigurasi, navigation, dan tautan internal.
3. Periksa snippet Python untuk sintaks dan konsistensi API.
4. Jalankan unit test untuk fungsi preprocessing dan kode yang dapat diuji.
5. Jalankan eksperimen baseline pada dataset sintetis jika sudah tersedia.
6. Pastikan angka evaluasi berasal dari eksekusi nyata.
7. Pastikan file dataset, model, dan kredensial tidak ikut terpublikasi tanpa sengaja.
8. Catat pemeriksaan yang berhasil, gagal, atau belum dilakukan.

Jangan mengklaim seluruh website telah lolos pengujian jika hanya sebagian yang diperiksa.

## 12. Dokumentasi proyek

Buat atau lengkapi:

- README.md dalam Bahasa Indonesia.
- Panduan instalasi.
- Panduan menjalankan MkDocs secara lokal.
- Panduan menjalankan notebook.
- Panduan menambahkan materi baru.
- Panduan menambahkan eksperimen.
- Peta kurikulum.
- Glosarium NLP.
- Catatan keputusan teknis yang penting.

Jelaskan perintah yang sesuai dengan konfigurasi repository aktual. Jangan mengasumsikan bahwa direktori konten selalu bernama `docs`.

## 13. Urutan implementasi

Kerjakan secara bertahap agar perubahan mudah diperiksa dan tidak menghasilkan satu perubahan besar yang sulit di-debug.

Tahap 1: Audit repository dan susun rencana implementasi.

Tahap 2: Siapkan struktur kurikulum, landing page, navigation, dan glosarium.

Tahap 3: Implementasikan Level 0 dan Level 1 beserta contoh Python.

Tahap 4: Implementasikan Level 2 dan notebook preprocessing.

Tahap 5: Implementasikan Level 3 sampai Level 5 dan baseline klasifikasi kebencanaan.

Tahap 6: Implementasikan Level 6 dan Level 7 secara bertahap.

Tahap 7: Lengkapi proyek utama, dokumentasi, referensi, latihan, dan kuis.

Tahap 8: Jalankan build, pemeriksaan tautan, tes kode, dan audit akhir.

Selesaikan setiap tahap secara fungsional sebelum beralih ke tahap berikutnya. Jangan membuat seluruh halaman sekaligus dengan konten dangkal.

Setelah setiap tahap, ringkas file yang dibuat atau diubah, pemeriksaan yang telah dijalankan, masalah yang ditemukan, dan langkah berikutnya.

Pertahankan perubahan pengguna yang sudah ada dan jangan melakukan operasi destruktif.
