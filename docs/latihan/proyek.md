# Latihan Proyek dan Kuis Gabungan

!!! abstract "Info latihan"
    **Tingkat kesulitan:** Menengah–lanjut. **Estimasi waktu:** 5–10 jam (mini-proyek) + 30 menit (kuis).
    **Cakupan:** seluruh kurikulum dan [Proyek Klasifikasi Kebencanaan](../proyek-klasifikasi-bencana/index.md). Mini-proyek bersifat terbuka: dinilai dengan **rubrik**, bukan satu kunci.

## Mini-proyek

Setiap mini-proyek diakhiri **laporan satu halaman** yang memuat: pertanyaan, data (sintetis atau sah), metode, tabel hasil dari kode (bukan diketik), kesimpulan **beserta batasnya**, dan apa yang tidak diuji.

### MP1: Pedoman anotasi baru (Tahap A–B)
Tulis 30 postingan sintetis tentang bahaya yang tidak ada di dataset (mis. gelombang panas, wabah, kecelakaan lalu lintas), beri label dengan pedoman, minta satu orang lain melabeli, hitung kappa, perbaiki pedoman, dan hitung kappa lagi pada 15 postingan baru.

**Rubrik:** kappa dihitung benar; perbedaan dianalisis per aturan; perbaikan pedoman spesifik; sampel kedua benar-benar baru; tidak ada data pribadi nyata.

### MP2: Audit dan perluasan dataset (Tahap B–C)
Jalankan `periksa_semua` pada dataset Anda sendiri, tambahkan satu pemeriksaan baru (mis. panjang teks > 280, karakter tak terlihat), tulis tesnya, dan lakukan EDA (distribusi, panjang, duplikat, kebocoran).

**Rubrik:** pemeriksaan baru memiliki tes sukses dan gagal; EDA menghasilkan hipotesis yang dapat diuji; ada pernyataan keterbatasan data.

### MP3: Studi ablation preprocessing (Tahap D)
Bandingkan tiga strategi preprocessing dengan protokol per kejadian dan **tiga seed pembagian berbeda**. Laporkan rata-rata dan rentang, bukan satu angka.

**Rubrik:** hanya preprocessing yang berubah; transformasi korpus di dalam pipeline; kesimpulan sesuai ukuran selisih; tidak ada pemilihan dari set tulis-tangan.

### MP4: Baseline vs model neural (Tahap E–G)
Bandingkan Linear SVM dan MLP NumPy (Level 6) atau IndoBERT (jika `requirements-dl.txt` terpasang) pada data latih yang **sama**, dengan ≥5 seed untuk model neural. Tambahkan selang bootstrap atau uji berpasangan (`selisih_recall_bootstrap`).

**Rubrik:** data latih sama; seed dilaporkan; rentang dan ukuran set disebut; kesimpulan tidak melebihi bukti; tanpa klaim operasional.

### MP5: Layanan dan model card (Tahap H)
Tambahkan satu endpoint (mis. `GET /versi` atau `GET /riwayat/zona-ragu`) beserta tes, perbarui README penggunaan, dan hasilkan model card untuk model Anda dengan keterbatasan yang ditulis manusia.

**Rubrik:** tes sukses dan gagal; tidak ada teks mentah di log/riwayat; model card memuat penggunaan yang tidak sesuai; tidak ada klaim probabilitas dari skor SVM.

## Kuis gabungan (seluruh kurikulum)

**1.** Sebutkan dua syarat Emergency pada definisi operasional proyek.

??? success "Jawaban"
    (a) Ada kejadian yang sedang berlangsung atau baru terjadi yang mengancam; (b) postingan melaporkannya atau meminta bantuan terkait kejadian itu. Keduanya harus terpenuhi.

**2.** Mengapa akurasi menipu pada data dengan 5% Emergency?

??? success "Jawaban"
    Model "selalu Non-Emergency" mendapat akurasi 0,95 tanpa menemukan satu pun Emergency (recall 0). Pakai recall/presisi kelas Emergency dan bandingkan dengan baseline.

**3.** Mengapa `TfidfVectorizer().fit_transform` pada seluruh data sebelum membagi adalah kebocoran?

??? success "Jawaban"
    Kosakata dan IDF dihitung dengan ikut memakai data uji.

**4.** Apa yang diukur kappa yang tidak diukur persentase kesepakatan?

??? success "Jawaban"
    Kesepakatan yang dikoreksi untuk kebetulan, penting pada kelas dominan.

**5.** Mengapa ambang yang dipilih pada validasi dapat gagal pada data bergaya lain?

??? success "Jawaban"
    Distribusi skor berubah dengan gaya bahasa; ambang bergantung pada distribusi skor, bukan melekat pada model. Contoh di proyek: recall tulis-tangan 0,083 pada ambang dari validasi.

**6.** Apa beda skor keputusan SVM dan probabilitas terkalibrasi?

??? success "Jawaban"
    Skor adalah angka monoton tanpa makna probabilistik; probabilitas terkalibrasi memiliki frekuensi nyata yang cocok dengan nilainya dan perlu divalidasi pada data representatif.

**7.** Mengapa Transformer memerlukan positional encoding?

??? success "Jawaban"
    Self-attention memperlakukan masukan sebagai himpunan; tanpa informasi posisi, urutan kata tidak berpengaruh.

**8.** Mengapa laporan fine-tuning harus memuat beberapa seed?

??? success "Jawaban"
    Inisialisasi kepala klasifikasi dan urutan batch acak; pada data kecil hasil antar seed dapat berbeda beberapa poin sehingga satu angka menyesatkan.

**9.** Apa yang dilindungi checksum model, dan apa yang tidak?

??? success "Jawaban"
    Melindungi dari berkas yang berubah sejak checksum dibuat; tidak membuktikan berkas aman.

**10.** Mengapa log layanan mencatat hash teks, bukan teksnya?

??? success "Jawaban"
    Pesan bencana dapat memuat data pribadi; hash memungkinkan melihat duplikasi tanpa menyimpan isi.

**11.** Mengapa PSI > 0,1 pada sampel kecil tidak membuktikan drift?

??? success "Jawaban"
    Derau pengambilan sampel sudah menaikkan PSI; ambang harus ditentukan dari simulasi pada ukuran jendela yang sama.

**12.** Bolehkah sistem ini mengirim bantuan otomatis berdasarkan label Emergency?

??? success "Jawaban"
    Tidak. Ia hanya alat bantu prioritas tinjauan manusia; verifikasi manusia, evaluasi pada data nyata yang sah, dan kontrol keamanan diperlukan.

## Checkpoint akhir

- [ ] Saya dapat menjalankan seluruh alur proyek dari definisi label sampai API dan tes.
- [ ] Saya dapat menjelaskan setiap angka yang saya laporkan: dari kode mana, data mana, seed mana.
- [ ] Saya dapat menyebut tiga batas klaim proyek ini tanpa membuka halaman.
- [ ] Saya dapat menolak permintaan "pasang di server dan kirim ambulans otomatis" dengan alasan tertulis.

## Materi berikutnya

Kembali ke [indeks latihan](index.md) atau [Proyek Klasifikasi Kebencanaan](../proyek-klasifikasi-bencana/index.md).
