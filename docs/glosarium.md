# Glosarium

Istilah dipakai secara konsisten di seluruh situs. Istilah bahasa Inggris yang
umum dipertahankan, disertai padanan atau penjelasan Indonesia. Glosarium
ditambah seiring materi baru ditulis.

## A–F

Ablation study
:   Eksperimen yang mencabut satu komponen pipeline untuk mengukur kontribusinya ([Ablation](level-5-evaluasi/ablation-robustness.md)).

Akurasi
:   Proporsi tebakan yang benar: (TP+TN)/N. Menyesatkan pada kelas tidak seimbang.

Aliasing
:   Dua nama yang menunjuk ke objek yang sama.

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

Artefak data
:   Pola pada data yang berasal dari cara data dibuat, bukan dari fenomena sebenarnya (mis. alamat selalu ada pada templat laporan).

Artificial Intelligence (AI)
:   Bidang yang membuat sistem komputer melakukan tugas yang biasanya memerlukan kecerdasan manusia.

Bag of Words (BoW)
:   Representasi teks sebagai hitungan kata dari kosakata, tanpa urutan ([Bag of Words](level-3-representasi-teks/bag-of-words.md)).

Baseline
:   Model atau aturan sederhana sebagai pembanding minimum. Model rumit hanya bermakna bila mengalahkan baseline.

Bootstrap
:   Resampling dengan pengembalian untuk memperkirakan sebaran sebuah statistik, mis. selang kepercayaan metrik.

Case folding
:   Menyeragamkan huruf besar/kecil (biasanya menjadi huruf kecil).

Checksum (SHA-256)
:   Sidik jari berkas untuk mendeteksi perubahan; dipakai untuk memeriksa data dan model.

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

Confusion matrix
:   Tabel hitungan TP, TN, FP, FN ([Confusion Matrix](level-5-evaluasi/confusion-matrix.md)).

Context manager (`with`)
:   Konstruksi yang menyiapkan dan membersihkan sumber daya otomatis.

CSV
:   Format tabel teks dengan kolom dipisah koma.

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

Duplikat
:   Baris yang isinya sama dengan baris lain.

EDA
:   *Exploratory data analysis*: pemeriksaan data (struktur, duplikat, distribusi) untuk memahaminya sebelum modeling.

Ekspresi kondisional (ternary)
:   `x if syarat else y`: memilih satu dari dua nilai.

Emergency
:   Label untuk postingan yang melaporkan kejadian darurat yang sedang atau baru terjadi, atau meminta bantuan. Definisi operasional lengkap ada di [Masalah Emergency](level-0-orientasi/masalah-emergency.md).

Emoji dan emotikon
:   Emoji: karakter Unicode bergambar. Emotikon: rangkaian tanda baca yang membentuk wajah, mis. `:(`.

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

Fitur (feature)
:   Representasi numerik dari suatu contoh yang menjadi masukan model.

Function
:   Blok kode bernama yang dapat dipanggil berulang.

## G–N

Gazetteer
:   Daftar nama tempat yang dipakai untuk mengenali lokasi dalam teks.

Git
:   Sistem pelacak riwayat perubahan berkas.

Greedy / non-greedy
:   Mengambil sebanyak / sesedikit mungkin.

Grid search
:   Pencarian semua kombinasi nilai hyperparameter dari daftar (`GridSearchCV`).

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

Inference (inferensi)
:   Memakai model yang sudah dilatih untuk memprediksi data baru.

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

Kebocoran data
:   Informasi dari data uji ikut memengaruhi pelatihan.

Kelompok (*group*)
:   Bagian pola dalam kurung yang dapat diambil atau dirujuk.

Kernel Jupyter
:   Proses Python yang menjalankan sel notebook.

Kesepakatan (*agreement*)
:   Proporsi contoh yang diberi label sama oleh dua anotator.

Ketidakseimbangan kelas
:   Jumlah contoh antarkelas sangat berbeda.

Klasifikasi teks
:   Tugas memberi satu label dari himpunan tetap pada sebuah teks.

Kode keluar (*exit code*)
:   Angka yang dikembalikan program ke terminal; `0` berarti sukses.

Korpus
:   Kumpulan dokumen yang dianalisis.

Kosakata (vocabulary)
:   Himpunan tipe token (kata unik) yang menjadi kolom matriks fitur.

Kuantifier
:   Penanda jumlah pengulangan (`+`, `*`, `?`, `{n,m}`).

Label
:   Jawaban yang benar untuk suatu contoh (target `y`), misalnya `Emergency`.

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

Mention
:   Penyebutan akun dengan awalan `@`.

Method chaining
:   Merantai beberapa metode sehingga hasil satu menjadi masukan berikutnya.

Metode (*method*)
:   Fungsi yang melekat pada objek dan dipanggil dengan titik, mis. `teks.strip()`.

Missing value
:   Nilai yang tidak ada pada data.

Mode buka
:   Cara membuka berkas: `"r"`, `"w"`, `"a"`.

Model
:   Fungsi yang dipelajari dari data untuk memetakan fitur ke prediksi.

Modul
:   Berkas Python yang dapat di-*import*.

Mojibake
:   Teks rusak karena byte dibaca dengan encoding yang salah.

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

Non-Emergency
:   Label untuk semua postingan lain: berita, opini, informasi lama, peringatan umum, dan topik tak terkait.

`None`
:   Nilai khusus yang berarti "tidak ada nilai".

Norma L2
:   Panjang vektor: akar jumlah kuadrat elemen.

Normalisasi Unicode
:   Penyeragaman representasi karakter yang tampak sama (NFC, NFD, NFKC, NFKD).

## O–Z

Off-by-one
:   Kesalahan selisih satu pada batas indeks.

One-hot encoding
:   Representasi kategori sebagai vektor dengan satu elemen 1 dan sisanya 0.

OOV (out of vocabulary)
:   Kata pada data baru yang tidak ada di kosakata yang dipelajari saat pelatihan.

Overfitting dan underfitting
:   Overfitting: model menghafal data latih sehingga buruk pada data baru. Underfitting: model terlalu sederhana sehingga buruk bahkan pada data latih.

Paket
:   Folder berisi modul.

Parameter (model)
:   Nilai yang dipelajari model dari data (misalnya bobot kata). Berbeda dari *hyperparameter*, yang dipilih sebelum training.

Parameter / argumen
:   Nama di definisi / nilai yang diberikan saat memanggil.

Pasangan surrogate
:   Dua kode `\uXXXX` yang mewakili satu karakter di luar BMP, seperti emoji.

Path (jalur)
:   Lokasi berkas atau folder.

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

pip
:   Alat pemasang pustaka Python dari PyPI.

Pipeline (scikit-learn)
:   Rangkaian langkah transformasi dan model yang bekerja sebagai satu estimator ([Pipeline](level-4-machine-learning/pipeline-sklearn.md)).

Precision
:   Dari semua yang diprediksi positif, berapa proporsi yang benar-benar positif.

Preprocessing
:   Rangkaian transformasi teks sebelum dijadikan fitur, misalnya case folding dan pembersihan URL.

Prevalensi
:   Proporsi kelas positif pada data.

Pustaka standar
:   Kumpulan modul bawaan Python.

PyPI
:   Gudang paket Python publik.

`pytest`
:   Kerangka pengujian untuk Python.

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

Representasi
:   Cara mengubah teks menjadi angka yang dapat diproses model.

Reproducibility
:   Kemampuan mengulang eksperimen dan mendapat hasil yang sama.

Robustness
:   Ketahanan prediksi terhadap perubahan masukan yang tidak mengubah arti.

Scope (lingkup)
:   Wilayah program tempat sebuah nama berlaku.

Selang kepercayaan
:   Rentang nilai yang masuk akal untuk sebuah statistik pada tingkat kepercayaan tertentu.

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

Sigmoid
:   Fungsi $1/(1+e^{-z})$ yang memetakan skor ke rentang 0-1.

Skor
:   Angka keyakinan atau kecocokan yang dihasilkan model.

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

Stemming
:   Memotong imbuhan dengan aturan sehingga bentuk turunan menyatu; Sastrawi untuk bahasa Indonesia.

Stopword
:   Kata yang sangat sering muncul dan dibuang saat preprocessing; daftar bawaan Sastrawi memuat `tidak`, `belum`, dan `tolong`.

String
:   Urutan karakter yang ditulis dengan tanda kutip.

Supervised learning
:   Pembelajaran dari contoh berlabel (pasangan teks dan label).

SVM linear
:   Pengklasifikasi yang mencari hyperplane dengan margin terbesar; skornya bukan probabilitas.

`sys.path`
:   Daftar lokasi tempat Python mencari modul.

Tes regresi
:   Tes yang menjaga agar bug yang sudah diperbaiki tidak kembali.

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

Truthy / falsy
:   Nilai yang dianggap benar atau salah dalam syarat.

Tuple
:   Wadah berurutan yang tidak dapat diubah.

`uncertain` (`U`)
:   Label sementara untuk kasus yang ragu dan perlu ditinjau bersama.

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

Wheel
:   Format paket Python yang sudah dikompilasi untuk versi Python tertentu.

