# Glosarium

Istilah dipakai secara konsisten di seluruh situs. Istilah bahasa Inggris yang
umum dipertahankan, disertai padanan atau penjelasan Indonesia. Glosarium
ditambah seiring materi baru ditulis.

## A–F

Ablation
:   Menambah atau mencabut komponen untuk mengukur kontribusinya. ([tahap-d-preprocessing](proyek-klasifikasi-bencana/tahap-d-preprocessing.md))

Ablation study
:   Eksperimen yang mencabut satu komponen pipeline untuk mengukur kontribusinya ([Ablation](level-5-evaluasi/ablation-robustness.md)).

Adam
:   Optimizer dengan langkah adaptif per parameter. ([neural-network-dasar](level-6-deep-learning/neural-network-dasar.md))

AdamW
:   Adam dengan peluruhan bobot yang dipisahkan. ([fine-tuning-transfer-learning](level-6-deep-learning/fine-tuning-transfer-learning.md))

Akurasi
:   Proporsi tebakan yang benar: (TP+TN)/N. Menyesatkan pada kelas tidak seimbang.

Aliasing
:   Dua nama yang menunjuk ke objek yang sama.

Analisis irisan
:   Menghitung metrik per subkelompok. ([bias-robustness-ood](level-7-advanced-nlp/bias-robustness-ood.md))

Anonimisasi
:   Menghilangkan atau mengganti identitas pengguna.

Anotasi
:   Proses manusia memberi label pada data.

Anotasi tipe
:   Petunjuk tipe (`x: int`, `-> str`) yang tidak dipaksakan saat berjalan.

Anotator
:   Orang yang memberi label pada data.

Array (`ndarray`)
:   Tabel angka bertipe seragam berukuran tetap.

Artefak
:   Berkas hasil pelatihan yang dipakai saat inferensi. ([arsitektur-pipeline](level-7-advanced-nlp/arsitektur-pipeline.md))

Artefak data
:   Pola pada data yang berasal dari cara data dibuat, bukan dari fenomena sebenarnya (mis. alamat selalu ada pada templat laporan).

Artificial Intelligence (AI)
:   Bidang yang membuat sistem komputer melakukan tugas yang biasanya memerlukan kecerdasan manusia.

Atomik
:   Semua atau tidak sama sekali. ([fastapi-batch-riwayat-tes](level-7-advanced-nlp/fastapi-batch-riwayat-tes.md))

Backpropagation
:   Penerapan aturan rantai untuk menghitung gradien semua parameter. ([neural-network-dasar](level-6-deep-learning/neural-network-dasar.md))

Bag of Words (BoW)
:   Representasi teks sebagai hitungan kata dari kosakata, tanpa urutan ([Bag of Words](level-3-representasi-teks/bag-of-words.md)).

Baseline
:   Model atau aturan sederhana sebagai pembanding minimum. Model rumit hanya bermakna bila mengalahkan baseline.

Bootstrap
:   Resampling dengan pengembalian untuk memperkirakan sebaran sebuah statistik, mis. selang kepercayaan metrik.

BPE
:   Algoritma pembentuk kosakata subword dengan menggabungkan pasangan simbol tersering. ([tokenizer-bert-indobert](level-6-deep-learning/tokenizer-bert-indobert.md))

Cakupan kosakata
:   Proporsi token yang dikenal kosakata model. ([pemantauan-drift](level-7-advanced-nlp/pemantauan-drift.md))

Case folding
:   Menyeragamkan huruf besar/kecil (biasanya menjadi huruf kecil).

Celah generalisasi
:   Selisih performa latih dan validasi. ([overfitting-evaluasi-dl](level-6-deep-learning/overfitting-evaluasi-dl.md))

Checksum (SHA-256)
:   Sidik jari berkas untuk mendeteksi perubahan; dipakai untuk memeriksa data dan model.

Checksum / SHA-256
:   Sidik jari berkas. ([arsitektur-pipeline](level-7-advanced-nlp/arsitektur-pipeline.md))

Cherry-picking
:   Melaporkan hasil terbaik dari beberapa percobaan tanpa menyebut sisanya. ([tahap-f-evaluasi](proyek-klasifikasi-bencana/tahap-f-evaluasi.md))

Class imbalance
:   Jumlah contoh antarkelas sangat tidak seimbang, misalnya Emergency jauh lebih sedikit daripada Non-Emergency.

Code point
:   Nomor sebuah karakter dalam Unicode, ditulis misalnya U+1F64F.

Cohen's kappa
:   Ukuran kesepakatan dua anotator yang memperhitungkan kesepakatan karena kebetulan.

Commit
:   Satu titik simpan riwayat perubahan di Git.

Comprehension
:   Sintaks ringkas membuat list/set dari perulangan.

Concept drift
:   Perubahan hubungan masukan–label. ([pemantauan-drift](level-7-advanced-nlp/pemantauan-drift.md))

Confusion matrix
:   Tabel hitungan TP, TN, FP, FN ([Confusion Matrix](level-5-evaluasi/confusion-matrix.md)).

Context manager (`with`)
:   Konstruksi yang menyiapkan dan membersihkan sumber daya otomatis.

CSV
:   Format tabel teks dengan kolom dipisah koma.

Data card
:   Dokumen yang menjelaskan dataset. ([tahap-b-dataset](proyek-klasifikasi-bencana/tahap-b-dataset.md))

Data drift
:   Perubahan distribusi masukan. ([pemantauan-drift](level-7-advanced-nlp/pemantauan-drift.md))

Data leakage
:   Informasi dari data uji (atau masa depan) ikut memengaruhi pelatihan sehingga skor evaluasi terlalu optimistis.

Data snooping
:   Memakai data evaluasi untuk memilih sesuatu (model, ambang) lalu melaporkan skor dari data yang sama.

Data uji
:   Data untuk estimasi akhir performa, dipakai sekali.

Data validasi
:   Data untuk memilih hyperparameter atau model.

DataFrame
:   Tabel dua dimensi berkolom nama.

Dataset
:   Kumpulan contoh data. Dalam proyek ini, tiap baris berisi satu postingan (`text`) dan labelnya (`label`).

Debugging
:   Menemukan dan memperbaiki penyebab perilaku salah.

Deep learning
:   Cabang machine learning yang memakai jaringan saraf berlapis banyak.

Definisi operasional
:   Definisi yang cukup jelas sehingga dua orang dapat menerapkannya dan sampai pada label yang sama.

Dictionary
:   Wadah pasangan kunci → nilai.

Docstring
:   String penjelas pertama di dalam function.

Document (dokumen)
:   Satu unit teks yang dianalisis. Di proyek ini: satu postingan.

Document frequency (DF)
:   Jumlah dokumen yang memuat suatu kata minimal sekali.

Dropout
:   Mematikan neuron acak saat latihan. ([overfitting-evaluasi-dl](level-6-deep-learning/overfitting-evaluasi-dl.md))

Duplikat
:   Baris yang isinya sama dengan baris lain.

Early stopping
:   Menghentikan pelatihan ketika loss validasi tidak membaik. ([overfitting-evaluasi-dl](level-6-deep-learning/overfitting-evaluasi-dl.md))

ECE
:   Selisih tertimbang antara prediksi dan frekuensi nyata per bin. ([kalibrasi-threshold](level-7-advanced-nlp/kalibrasi-threshold.md))

EDA
:   *Exploratory data analysis*: pemeriksaan data (struktur, duplikat, distribusi) untuk memahaminya sebelum modeling.

Ekspresi kondisional (ternary)
:   `x if syarat else y`: memilih satu dari dua nilai.

Embedding
:   Vektor padat yang mewakili kata (atau kalimat) dan dipelajari dari data. ([embedding-kata](level-6-deep-learning/embedding-kata.md))

Emergency
:   Label untuk postingan yang melaporkan kejadian darurat yang sedang atau baru terjadi, atau meminta bantuan. Definisi operasional lengkap ada di [Masalah Emergency](level-0-orientasi/masalah-emergency.md).

Emoji dan emotikon
:   Emoji: karakter Unicode bergambar. Emotikon: rangkaian tanda baca yang membentuk wajah, mis. `:(`.

Encoder / Decoder
:   Tumpukan blok Transformer dua arah / satu arah. ([attention-transformer](level-6-deep-learning/attention-transformer.md))

Encoding
:   Aturan mengubah karakter (code point) menjadi byte; UTF-8 yang paling umum.

Error analysis
:   Pemeriksaan sistematis terhadap kesalahan model untuk menemukan pola dan penyebabnya.

Exception
:   Objek galat yang dibangkitkan saat sesuatu tidak mungkin dilakukan.

f-string
:   String berawalan `f` yang menyisipkan hasil ekspresi di dalam `{}`.

F1 dan F-beta
:   F1 = rata-rata harmonik presisi dan recall; F-beta menekankan recall ($\beta>1$) atau presisi ($\beta<1$).

Factory
:   Fungsi yang membuat aplikasi. ([fastapi-dasar](level-7-advanced-nlp/fastapi-dasar.md))

Faithfulness
:   Kesetiaan penjelasan terhadap perilaku model. ([interpretabilitas](level-7-advanced-nlp/interpretabilitas.md))

False negative (FN)
:   Kasus positif yang terlewat; pada proyek ini, pesan Emergency yang ditebak Non-Emergency.

False positive (FP)
:   Kasus negatif yang salah ditandai positif; pada proyek ini, Non-Emergency yang ditebak Emergency (alarm palsu).

False positive / false negative
:   Ditandai positif padahal bukan / tidak ditandai padahal positif.

*False positive rate*
:   Bagian contoh negatif yang salah ditandai positif.

Feature engineering
:   Merancang fitur numerik dari data mentah dengan pengetahuan domain.

`fillna` / `dropna`
:   Mengisi / membuang nilai kosong.

`finally`
:   Blok yang selalu berjalan setelah `try`.

Fine-tuning
:   Melanjutkan pelatihan model pra-latih pada tugas dan data berlabel khusus. ([fine-tuning-transfer-learning](level-6-deep-learning/fine-tuning-transfer-learning.md))

Fitur (feature)
:   Representasi numerik dari suatu contoh yang menjadi masukan model.

Fixture
:   Fungsi pytest yang menyiapkan sumber daya tes. ([fastapi-batch-riwayat-tes](level-7-advanced-nlp/fastapi-batch-riwayat-tes.md))

*Frozen dataclass*
:   Objek data yang tidak dapat diubah setelah dibuat; dipakai untuk konfigurasi. ([tahap-d-preprocessing](proyek-klasifikasi-bencana/tahap-d-preprocessing.md))

Function
:   Blok kode bernama yang dapat dipanggil berulang.

## G–N

Gazetteer
:   Daftar nama tempat yang dipakai untuk mengenali lokasi dalam teks.

Gerbang (*gate*)
:   Nilai 0–1 yang mengatur seberapa banyak informasi lewat. ([rnn-lstm-gru](level-6-deep-learning/rnn-lstm-gru.md))

Git
:   Sistem pelacak riwayat perubahan berkas.

GPU
:   Prosesor paralel yang mempercepat perkalian matriks. ([ml-klasik-vs-dl-komputasi](level-6-deep-learning/ml-klasik-vs-dl-komputasi.md))

Gradien menghilang
:   Gradien yang mengecil eksponensial saat dirambatkan melintasi banyak langkah. ([rnn-lstm-gru](level-6-deep-learning/rnn-lstm-gru.md))

*Gradient check*
:   Memeriksa gradien analitik dengan beda hingga. ([neural-network-dasar](level-6-deep-learning/neural-network-dasar.md))

Greedy / non-greedy
:   Mengambil sebanyak / sesedikit mungkin.

Grid search
:   Pencarian semua kombinasi nilai hyperparameter dari daftar (`GridSearchCV`).

Ground truth
:   Label yang dianggap benar sebagai acuan evaluasi. ([tahap-b-dataset](proyek-klasifikasi-bencana/tahap-b-dataset.md))

Hapax
:   Kata yang muncul tepat sekali di korpus.

Hashable
:   Dapat dijadikan kunci dictionary atau anggota set; objek yang tidak dapat diubah.

Hashtag
:   Kata berawalan `#` yang menandai topik.

Header
:   Baris pertama CSV berisi nama kolom.

Hinge loss
:   $\max(0, 1 - y f(x))$: kerugian SVM yang 0 untuk contoh di luar margin.

Human in the loop
:   Manusia memverifikasi atau memutuskan hasil sistem.

Human-in-the-loop
:   Manusia memeriksa dan memutuskan. ([keamanan-model-card-roadmap](level-7-advanced-nlp/keamanan-model-card-roadmap.md))

Hyperparameter
:   Pengaturan model yang ditetapkan sebelum pelatihan (mis. `C`, `alpha`, `ngram_range`).

Idempoten
:   Operasi yang jika diulang tidak mengubah hasil lagi.

IDF
:   *Inverse document frequency*: ukuran kelangkaan kata di korpus ([TF-IDF](level-3-representasi-teks/tfidf.md)).

Immutable
:   Tidak dapat diubah setelah dibuat.

`ImportError`
:   Galat ketika modul tidak dapat di-*import*.

Indeks (*index*)
:   Nomor posisi elemen dalam urutan, dimulai dari 0.

Indentasi
:   Spasi di awal baris yang menandai blok kode.

IndoBERT
:   Nama untuk model BERT berbahasa Indonesia; ada lebih dari satu. ([tokenizer-bert-indobert](level-6-deep-learning/tokenizer-bert-indobert.md))

Inference (inferensi)
:   Memakai model yang sudah dilatih untuk memprediksi data baru.

Inferensi
:   Memakai model yang sudah dilatih untuk memprediksi data baru. ([ml-klasik-vs-dl-komputasi](level-6-deep-learning/ml-klasik-vs-dl-komputasi.md))

Inferensi batch
:   Memprediksi banyak teks dalam satu panggilan. ([arsitektur-pipeline](level-7-advanced-nlp/arsitektur-pipeline.md))

Iterasi
:   Mengunjungi elemen koleksi satu per satu.

JSON
:   Format data bersarang berbasis teks (objek, larik, string, angka).

Jupyter Notebook
:   Dokumen interaktif yang memuat kode, hasil, dan teks.

Kalibrasi
:   Kesesuaian antara probabilitas keluaran model dan frekuensi kebenaran sebenarnya.

Kasus tepi
:   Masukan di batas atau tak lazim (kosong, nol, spasi berlebih).

Kata dasar (root)
:   Bentuk kata tanpa imbuhan; hasil stemming.

Keadaan tersembunyi (*hidden state*)
:   Vektor ringkasan bacaan hingga langkah tertentu. ([rnn-lstm-gru](level-6-deep-learning/rnn-lstm-gru.md))

Kebocoran data
:   Informasi dari data uji ikut memengaruhi pelatihan.

Kelompok (*group*)
:   Bagian pola dalam kurung yang dapat diambil atau dirujuk.

Kemiripan kosinus
:   Kosinus sudut antara dua vektor. ([embedding-kata](level-6-deep-learning/embedding-kata.md))

Kepala klasifikasi
:   Lapisan akhir yang memetakan representasi ke kelas. ([fine-tuning-transfer-learning](level-6-deep-learning/fine-tuning-transfer-learning.md))

Kernel Jupyter
:   Proses Python yang menjalankan sel notebook.

Kesepakatan (*agreement*)
:   Proporsi contoh yang diberi label sama oleh dua anotator.

Kesetaraan peluang
:   Recall sama antar kelompok. ([bias-robustness-ood](level-7-advanced-nlp/bias-robustness-ood.md))

Ketidakseimbangan kelas
:   Jumlah contoh antarkelas sangat berbeda.

Klasifikasi teks
:   Tugas memberi satu label dari himpunan tetap pada sebuah teks.

Ko-kemunculan
:   Hitungan berapa kali dua kata muncul berdekatan. ([embedding-kata](level-6-deep-learning/embedding-kata.md))

Kode keluar (*exit code*)
:   Angka yang dikembalikan program ke terminal; `0` berarti sukses.

Kode status HTTP
:   Angka yang menyatakan hasil permintaan (200, 422, 500). ([fastapi-dasar](level-7-advanced-nlp/fastapi-dasar.md))

Kontrak respons
:   Kesepakatan kolom dan makna yang dijaga oleh tes. ([tahap-h-deployment](proyek-klasifikasi-bencana/tahap-h-deployment.md))

Kontribusi fitur
:   Nilai fitur dikali koefisien. ([interpretabilitas](level-7-advanced-nlp/interpretabilitas.md))

Korpus
:   Kumpulan dokumen yang dianalisis.

Kosakata (vocabulary)
:   Himpunan tipe token (kata unik) yang menjadi kolom matriks fitur.

Kredensial
:   Rahasia akses seperti kunci API. ([keamanan-model-card-roadmap](level-7-advanced-nlp/keamanan-model-card-roadmap.md))

Kriteria inklusi/eksklusi
:   Aturan postingan mana yang masuk atau dikeluarkan dari dataset. ([tahap-a-definisi-masalah](proyek-klasifikasi-bencana/tahap-a-definisi-masalah.md))

Kuantifier
:   Penanda jumlah pengulangan (`+`, `*`, `?`, `{n,m}`).

Label
:   Jawaban yang benar untuk suatu contoh (target `y`), misalnya `Emergency`.

Latensi
:   Waktu dari permintaan sampai jawaban diterima. ([tahap-h-deployment](proyek-klasifikasi-bencana/tahap-h-deployment.md))

Learning rate
:   Ukuran langkah pembaruan parameter. ([neural-network-dasar](level-6-deep-learning/neural-network-dasar.md))

Lemmatization
:   Mengembalikan kata ke bentuk kamus (lemma) dengan memperhatikan tata bahasa; berbeda dari stemming.

List
:   Wadah berurutan yang dapat diubah.

Log-loss
:   Kerugian cross-entropy untuk peluang tebakan terhadap label sebenarnya.

Machine Learning (ML)
:   Pendekatan di mana model belajar pola dari data, bukan diprogram dengan aturan eksplisit.

Margin
:   Jarak antara hyperplane pemisah dan contoh terdekat pada SVM.

Mask kausal
:   Pembatas agar posisi tidak melihat posisi sesudahnya. ([attention-transformer](level-6-deep-learning/attention-transformer.md))

Mention
:   Penyebutan akun dengan awalan `@`.

Metadata model
:   Catatan versi, library, data, ambang, dan checksum. ([arsitektur-pipeline](level-7-advanced-nlp/arsitektur-pipeline.md))

Method chaining
:   Merantai beberapa metode sehingga hasil satu menjadi masukan berikutnya.

Metode (*method*)
:   Fungsi yang melekat pada objek dan dipanggil dengan titik, mis. `teks.strip()`.

Minimisasi data
:   Menyimpan hanya data yang diperlukan. ([fastapi-batch-riwayat-tes](level-7-advanced-nlp/fastapi-batch-riwayat-tes.md))

Missing value
:   Nilai yang tidak ada pada data.

MLM
:   Tugas pra-latih menebak kata yang ditutup dari konteks. ([tokenizer-bert-indobert](level-6-deep-learning/tokenizer-bert-indobert.md))

Mode buka
:   Cara membuka berkas: `"r"`, `"w"`, `"a"`.

Model
:   Fungsi yang dipelajari dari data untuk memetakan fitur ke prediksi.

Model card
:   Dokumen ringkas tentang tujuan, data, evaluasi, dan keterbatasan model. ([keamanan-model-card-roadmap](level-7-advanced-nlp/keamanan-model-card-roadmap.md))

Model pra-latih
:   Model yang sudah dilatih pada korpus besar sebelum disesuaikan. ([tahap-g-advanced-modeling](proyek-klasifikasi-bencana/tahap-g-advanced-modeling.md))

Modul
:   Berkas Python yang dapat di-*import*.

Mojibake
:   Teks rusak karena byte dibaca dengan encoding yang salah.

Multi-head attention
:   Beberapa attention paralel yang hasilnya digabung. ([attention-transformer](level-6-deep-learning/attention-transformer.md))

N-gram
:   Urutan *n* item (kata atau karakter) yang berurutan.

Naive Bayes (Multinomial)
:   Pengklasifikasi yang menghitung peluang kelas dari peluang kata per kelas dengan asumsi kata saling bebas.

Named Entity Recognition (NER)
:   Mengenali entitas bertipe (orang, lokasi) dalam teks.

`NaN`
:   Nilai kosong numerik (*not a number*).

Natural Language Processing (NLP)
:   Bidang yang memungkinkan komputer memproses dan memahami bahasa manusia.

Near-duplicate
:   Teks yang hampir sama tetapi tidak persis sama; sumber kebocoran antar-templat.

Negasi
:   Kata yang membalik makna (tidak, belum, bukan, jangan); cakupannya sulit ditangkap BoW.

Neuron / lapisan
:   Unit hitung $\sigma(wx+b)$ dan kumpulannya. ([neural-network-dasar](level-6-deep-learning/neural-network-dasar.md))

Non-Emergency
:   Label untuk semua postingan lain: berita, opini, informasi lama, peringatan umum, dan topik tak terkait.

`None`
:   Nilai khusus yang berarti "tidak ada nilai".

Norma L2
:   Panjang vektor: akar jumlah kuadrat elemen.

Normalisasi Unicode
:   Penyeragaman representasi karakter yang tampak sama (NFC, NFD, NFKC, NFKD).

## O–Z

`[CLS]` / `[SEP]`
:   Token awal (ringkasan) / pemisah pada BERT. ([tokenizer-bert-indobert](level-6-deep-learning/tokenizer-bert-indobert.md))

Off-by-one
:   Kesalahan selisih satu pada batas indeks.

Oklusi
:   Menghapus bagian masukan untuk melihat perubahan keluaran. ([interpretabilitas](level-7-advanced-nlp/interpretabilitas.md))

One-hot encoding
:   Representasi kategori sebagai vektor dengan satu elemen 1 dan sisanya 0.

OOD
:   Data yang berbeda jenis dari data latih. ([bias-robustness-ood](level-7-advanced-nlp/bias-robustness-ood.md))

OOV (*out-of-vocabulary*)
:   Kata yang tidak ada di kosakata model. ([embedding-kata](level-6-deep-learning/embedding-kata.md))

OOV (out of vocabulary)
:   Kata pada data baru yang tidak ada di kosakata yang dipelajari saat pelatihan.

Overfitting
:   Model menghafal data latih sehingga buruk pada data baru. ([overfitting-evaluasi-dl](level-6-deep-learning/overfitting-evaluasi-dl.md))

Overfitting dan underfitting
:   Overfitting: model menghafal data latih sehingga buruk pada data baru. Underfitting: model terlalu sederhana sehingga buruk bahkan pada data latih.

Padding
:   Token kosong untuk menyamakan panjang teks dalam satu batch. ([rnn-lstm-gru](level-6-deep-learning/rnn-lstm-gru.md))

Paket
:   Folder berisi modul.

Parameter (model)
:   Nilai yang dipelajari model dari data (misalnya bobot kata). Berbeda dari *hyperparameter*, yang dipilih sebelum training.

Parameter / argumen
:   Nama di definisi / nilai yang diberikan saat memanggil.

`parametrize`
:   Menjalankan satu tes dengan banyak masukan. ([fastapi-batch-riwayat-tes](level-7-advanced-nlp/fastapi-batch-riwayat-tes.md))

Pasangan surrogate
:   Dua kode `\uXXXX` yang mewakili satu karakter di luar BMP, seperti emoji.

Path (jalur)
:   Lokasi berkas atau folder.

Penggunaan di luar maksud
:   Memakai model untuk tujuan yang tidak divalidasi. ([keamanan-model-card-roadmap](level-7-advanced-nlp/keamanan-model-card-roadmap.md))

Penjelasan lokal / global
:   Alasan satu prediksi / perilaku model secara keseluruhan. ([interpretabilitas](level-7-advanced-nlp/interpretabilitas.md))

Penugasan (*assignment*)
:   Pembuatan hubungan nama dan nilai dengan tanda `=`.

Penyaringan boolean
:   Memilih baris berdasarkan syarat `True/False`.

Percabangan
:   Pemilihan jalur program berdasarkan syarat.

Perkalian titik (*dot product*)
:   Jumlah hasil kali elemen yang bersesuaian dua vektor.

Perturbasi
:   Perubahan kecil terkontrol pada masukan untuk menguji ketahanan model.

Perulangan tak berujung
:   `while` yang kondisinya tidak pernah salah.

PII
:   Informasi yang dapat mengidentifikasi seseorang. ([keamanan-model-card-roadmap](level-7-advanced-nlp/keamanan-model-card-roadmap.md))

pip
:   Alat pemasang pustaka Python dari PyPI.

Pipeline (scikit-learn)
:   Rangkaian langkah transformasi dan model yang bekerja sebagai satu estimator ([Pipeline](level-4-machine-learning/pipeline-sklearn.md)).

Positional encoding
:   Informasi posisi yang ditambahkan ke embedding. ([attention-transformer](level-6-deep-learning/attention-transformer.md))

PPMI
:   PMI yang nilai negatifnya dijadikan 0. ([embedding-kata](level-6-deep-learning/embedding-kata.md))

Pra-latih (*pre-trained*)
:   Model yang sudah dilatih pada korpus besar dan dipakai ulang untuk tugas lain. ([ml-klasik-vs-dl-komputasi](level-6-deep-learning/ml-klasik-vs-dl-komputasi.md))

Precision
:   Dari semua yang diprediksi positif, berapa proporsi yang benar-benar positif.

Preprocessing
:   Rangkaian transformasi teks sebelum dijadikan fitur, misalnya case folding dan pembersihan URL.

Prevalensi
:   Proporsi kelas positif pada data.

Prior shift
:   Perubahan proporsi kelas. ([pemantauan-drift](level-7-advanced-nlp/pemantauan-drift.md))

Probe
:   Kumpulan kecil contoh untuk menyelidiki satu perilaku. ([bias-robustness-ood](level-7-advanced-nlp/bias-robustness-ood.md))

Provenance
:   Asal-usul dan riwayat pembuatan data. ([tahap-b-dataset](proyek-klasifikasi-bencana/tahap-b-dataset.md))

PSI
:   Population Stability Index. ([pemantauan-drift](level-7-advanced-nlp/pemantauan-drift.md))

Pustaka standar
:   Kumpulan modul bawaan Python.

Pydantic
:   Pustaka validasi data berbasis tipe. ([fastapi-dasar](level-7-advanced-nlp/fastapi-dasar.md))

PyPI
:   Gudang paket Python publik.

`pytest`
:   Kerangka pengujian untuk Python.

Query, Key, Value
:   Tiga proyeksi masukan yang dipakai attention untuk bertanya, ditawarkan, dan diberikan. ([attention-transformer](level-6-deep-learning/attention-transformer.md))

`raise`
:   Perintah membangkitkan exception secara sengaja.

Raw string
:   String berawalan `r` yang tidak menafsirkan garis miring terbalik.

Recall
:   Dari semua contoh positif yang sebenarnya, berapa proporsi yang berhasil ditemukan model.

Regex (*regular expression*)
:   Bahasa untuk menulis pola pencarian pada teks.

Regularisasi
:   Hukuman pada bobot besar agar model tidak menghafal (L2: jumlah kuadrat bobot).

Regularisasi L2
:   Penalti pada kuadrat bobot agar bobot kecil. ([overfitting-evaluasi-dl](level-6-deep-learning/overfitting-evaluasi-dl.md))

ReLU
:   Aktivasi $\max(0,z)$. ([neural-network-dasar](level-6-deep-learning/neural-network-dasar.md))

Rentang antar seed
:   Minimum dan maksimum hasil beberapa pelatihan acak. ([tahap-f-evaluasi](proyek-klasifikasi-bencana/tahap-f-evaluasi.md))

Representasi
:   Cara mengubah teks menjadi angka yang dapat diproses model.

Reproducibility
:   Kemampuan mengulang eksperimen dan mendapat hasil yang sama.

REST / endpoint
:   Gaya API berbasis HTTP; alamat tempat operasi ditawarkan. ([fastapi-dasar](level-7-advanced-nlp/fastapi-dasar.md))

Robustness
:   Ketahanan prediksi terhadap perubahan masukan yang tidak mengubah arti.

Scope (lingkup)
:   Wilayah program tempat sebuah nama berlaku.

Selang kepercayaan
:   Rentang nilai yang masuk akal untuk sebuah statistik pada tingkat kepercayaan tertentu.

Self-attention
:   Attention di mana $Q,K,V$ berasal dari barisan yang sama. ([attention-transformer](level-6-deep-learning/attention-transformer.md))

Seri (*tie*)
:   Dua kelas memiliki skor yang sama.

Serialisasi
:   Menyimpan objek di memori menjadi berkas (mis. `joblib`); muat hanya berkas tepercaya.

Serialisasi / deserialisasi
:   Mengubah objek ke teks (`dumps`) / teks ke objek (`loads`).

Series
:   Satu kolom atau baris dari DataFrame.

Set (himpunan)
:   Wadah elemen unik tanpa urutan.

`shape` / `dtype`
:   Ukuran tiap dimensi / tipe elemen array.

Shortcut
:   Sifat kebetulan yang berkorelasi dengan label. ([tahap-c-eda](proyek-klasifikasi-bencana/tahap-c-eda.md))

*Shortcut learning*
:   Model memakai petunjuk kebetulan dari data. ([interpretabilitas](level-7-advanced-nlp/interpretabilitas.md))

Sigmoid
:   Fungsi $1/(1+e^{-z})$ yang memetakan skor ke rentang 0-1.

Skala Platt
:   Pemetaan sigmoid dari skor ke probabilitas. ([kalibrasi-threshold](level-7-advanced-nlp/kalibrasi-threshold.md))

Skor
:   Angka keyakinan atau kecocokan yang dihasilkan model.

Skor Brier
:   Rata-rata kuadrat selisih probabilitas dan label. ([kalibrasi-threshold](level-7-advanced-nlp/kalibrasi-threshold.md))

Slice
:   Potongan urutan, ditulis `s[awal:akhir:langkah]`.

Smoothing Laplace
:   Penambahan konstanta agar tidak ada peluang nol pada Naive Bayes.

Sparse
:   Sebagian besar elemennya nol.

Sparse matrix
:   Matriks yang sebagian besar elemennya nol dan hanya menyimpan elemen bukan nol (CSR).

Sparsity
:   Sinyal terpecah menjadi banyak fitur yang jarang muncul.

SQL injection / XSS
:   Penyisipan perintah SQL / skrip melalui masukan. ([fastapi-batch-riwayat-tes](level-7-advanced-nlp/fastapi-batch-riwayat-tes.md))

Stemming
:   Memotong imbuhan dengan aturan sehingga bentuk turunan menyatu; Sastrawi untuk bahasa Indonesia.

Stopword
:   Kata yang sangat sering muncul dan dibuang saat preprocessing; daftar bawaan Sastrawi memuat `tidak`, `belum`, dan `tolong`.

String
:   Urutan karakter yang ditulis dengan tanda kutip.

Subword
:   Potongan kata yang dipakai sebagai satuan, mis. $n$-gram karakter. ([embedding-kata](level-6-deep-learning/embedding-kata.md))

Supervised learning
:   Pembelajaran dari contoh berlabel (pasangan teks dan label).

SVM linear
:   Pengklasifikasi yang mencari hyperplane dengan margin terbesar; skornya bukan probabilitas.

`sys.path`
:   Daftar lokasi tempat Python mencari modul.

Tabel silang
:   Hitungan dua variabel kategorik sekaligus. ([tahap-c-eda](proyek-klasifikasi-bencana/tahap-c-eda.md))

Tes regresi
:   Tes yang menjaga agar bug yang sudah diperbaiki tidak kembali.

`TestClient`
:   Klien yang memanggil aplikasi di dalam proses yang sama untuk pengujian. ([fastapi-dasar](level-7-advanced-nlp/fastapi-dasar.md))

Text mining
:   Proses menggali informasi dan pola dari kumpulan teks; beririsan dengan NLP.

TF-IDF
:   Pembobotan kata: frekuensi di dokumen dikali kelangkaan di korpus, lalu dinormalisasi L2.

Threshold (ambang)
:   Nilai skor yang memisahkan prediksi positif dan negatif; menukar presisi dan recall.

Tipe (type)
:   Token yang unik; jumlah tipe adalah ukuran kosakata.

Tipe data
:   Jenis nilai yang menentukan operasi yang boleh dilakukan (`str`, `int`, `float`, `bool`).

Token
:   Satuan teks hasil pemecahan, biasanya kata, subkata, atau karakter.

Tokenisasi
:   Proses memecah teks menjadi token.

Topeng boolean
:   Array `True/False` untuk memilih elemen.

Traceback
:   Jejak pemanggilan function yang ditampilkan saat galat tidak tertangkap.

Training (pelatihan)
:   Proses model menyesuaikan parameter berdasarkan data berlabel.

Transfer learning
:   Memakai pengetahuan dari satu tugas atau korpus untuk tugas lain. ([fine-tuning-transfer-learning](level-6-deep-learning/fine-tuning-transfer-learning.md))

Truthy / falsy
:   Nilai yang dianggap benar atau salah dalam syarat.

Tuple
:   Wadah berurutan yang tidak dapat diubah.

Uji kontrafaktual
:   Mengubah satu atribut dan mengamati perubahan keluaran. ([bias-robustness-ood](level-7-advanced-nlp/bias-robustness-ood.md))

`uncertain` (`U`)
:   Label sementara untuk kasus yang ragu dan perlu ditinjau bersama.

Unit analisis
:   Apa yang dianggap satu contoh; di sini satu postingan. ([tahap-a-definisi-masalah](proyek-klasifikasi-bencana/tahap-a-definisi-masalah.md))

Unit test
:   Pemeriksaan otomatis atas satu perilaku kecil.

Unpacking
:   Memecah pasangan atau tuple menjadi beberapa variabel.

Urutan (*sequence*)
:   Kumpulan elemen berurutan: string, list, tuple.

UTF-8
:   Encoding Unicode yang memakai 1-4 byte per karakter; paling umum dipakai.

Validasi silang (cross-validation)
:   Evaluasi berulang dengan bergantian memakai lipatan data sebagai uji.

Validasi silang berkelompok
:   Validasi silang di mana kelompok (kejadian) tidak terpecah antar lipatan. ([tahap-e-modeling](proyek-klasifikasi-bencana/tahap-e-modeling.md))

Variabel
:   Nama yang menunjuk ke sebuah nilai.

Vektor
:   Daftar angka dengan urutan tetap.

Vektorisasi
:   Menerapkan operasi pada seluruh array tanpa perulangan eksplisit.

Virtual environment
:   Lingkungan Python terisolasi per proyek agar versi library tidak bertabrakan.

Vocabulary shift
:   Perbedaan kosakata antara data latih dan data baru.

Warmup
:   Menaikkan learning rate bertahap di awal pelatihan. ([fine-tuning-transfer-learning](level-6-deep-learning/fine-tuning-transfer-learning.md))

Wheel
:   Format paket Python yang sudah dikompilasi untuk versi Python tertentu.

WordPiece
:   Kosakata subword dengan pemecahan greedy longest-match dan awalan `##`. ([tokenizer-bert-indobert](level-6-deep-learning/tokenizer-bert-indobert.md))

Zona ragu
:   Rentang skor dekat ambang yang perlu perhatian manusia. ([kalibrasi-threshold](level-7-advanced-nlp/kalibrasi-threshold.md))

