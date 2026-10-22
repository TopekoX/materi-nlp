# Penerapan NLP di Kehidupan Nyata

## Tujuan pembelajaran

- [ ] Mengidentifikasi tugas-tugas NLP umum dan masukan-keluarannya.
- [ ] Memetakan tiap tugas ke contoh nyata, termasuk di bidang kebencanaan.
- [ ] Menilai risiko kesalahan pada tiap aplikasi.

## Prasyarat

[Hubungan NLP dengan Machine Learning](hubungan-nlp-ml.md).

## Pengantar dan intuisi

NLP sudah hadir di keseharian: filter spam, saran ketikan, mesin pencari,
penerjemah. Cara terbaik memahami bidang ini adalah mengenali **jenis tugas**
di balik tiap aplikasi, karena satu jenis tugas dapat memakai teknik yang sama
di banyak domain.

## Konsep

| Tugas | Masukan → keluaran | Contoh umum | Contoh kebencanaan |
|---|---|---|---|
| Klasifikasi teks | Teks → satu kelas | Deteksi spam | **Emergency vs Non-Emergency** |
| Analisis sentimen | Teks → polaritas | Ulasan produk | Mengukur kecemasan publik |
| Named Entity Recognition | Teks → entitas bertipe | Mengenali nama orang | Mengekstrak lokasi kejadian |
| Ekstraksi informasi | Teks → data terstruktur | Menarik tanggal dari kontrak | Jumlah korban dan jenis kebutuhan |
| Topic modeling | Korpus → topik | Mengelompokkan berita | Tema keluhan pascabencana |
| Mesin penerjemah | Teks A → teks B | Penerjemah daring | Menerjemahkan peringatan lintas bahasa |
| Question answering | Pertanyaan → jawaban | Asisten virtual | "Di mana posko terdekat?" |
| Peringkasan | Teks panjang → ringkas | Ringkasan berita | Ringkasan laporan situasi |

### Dimensi risiko

Tidak semua kesalahan setara. Sebelum membangun sistem, tanyakan:

- Apa akibat **false positive** (sistem menandai padahal bukan)?
- Apa akibat **false negative** (sistem melewatkan padahal ya)?
- Siapa yang meninjau keluaran sistem, manusia atau mesin lain?

| Aplikasi | Akibat false positive | Akibat false negative |
|---|---|---|
| Filter spam | Surat penting masuk spam | Sedikit spam lolos |
| Penyaring pesan darurat | Petugas memeriksa pesan yang tidak mendesak | Permintaan tolong terlewat |

## Contoh kontekstual kebencanaan

Pusat koordinasi menerima ribuan postingan setelah gempa. Operator manusia
tidak mungkin membaca semuanya. Sistem NLP dapat **memprioritaskan antrean
tinjauan**: postingan yang diduga laporan kejadian dinaikkan peringkatnya.
Keputusan akhir tetap pada manusia.

!!! warning "Batas tanggung jawab"
    Dalam materi ini model hanya membantu *memprioritaskan* tinjauan. Ia tidak
    menentukan keadaan darurat secara otomatis.

## Contoh kode

Tidak ada kode pada halaman ini karena materinya konseptual. Sebagai gantinya,
ada analisis kasus pada bagian latihan.

## Kesalahan umum

- Menganggap satu model cocok untuk semua tugas.
- Mengabaikan perbedaan biaya kesalahan antar-aplikasi.
- Membangun sistem otomatis penuh untuk keputusan berisiko tinggi tanpa peninjauan manusia.

## Latihan mandiri

1. Pilih tiga aplikasi di ponsel Anda, tentukan tugas NLP di baliknya.
2. Untuk "ekstraksi lokasi dari laporan banjir", apa masukan dan keluarannya? Tulis satu contoh.
3. Analisis kasus: penyaring pesan darurat dengan 1.000 pesan per jam dan 5 petugas. Apakah false positive atau false negative lebih mahal? Beri alasan dan sebutkan asumsi Anda.

## Kuis singkat

**1.** Tugas apa yang dikerjakan sistem yang memberi label Emergency/Non-Emergency?

??? success "Jawaban"
    Klasifikasi teks (biner).

**2.** Mengapa penting menentukan biaya false negative sebelum membangun sistem?

??? success "Jawaban"
    Karena ia menentukan metrik dan ambang keputusan yang dioptimalkan; pada pesan darurat, pesan yang terlewat bisa berdampak serius.

## Ringkasan

NLP terdiri dari banyak jenis tugas. Memetakan masalah ke jenis tugas dan
memahami biaya kesalahan adalah langkah pertama perancangan.

## Referensi

- Imran, M., dkk. (2015). Processing social media messages in mass emergency: A survey. *ACM Computing Surveys*, 47(4).

## Materi selanjutnya

[Cara Kerja Sistem Klasifikasi Teks](cara-kerja-klasifikasi-teks.md)
