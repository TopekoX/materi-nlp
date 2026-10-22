# Memahami Masalah Emergency vs Non-Emergency

## Tujuan pembelajaran

- [ ] Menyatakan definisi operasional label Emergency dan Non-Emergency.
- [ ] Membedakan laporan kejadian, permintaan bantuan, berita, opini, informasi lama, dan peringatan umum.
- [ ] Menerapkan aturan anotasi pada contoh ambigu.

## Prasyarat

[Cara Kerja Sistem Klasifikasi Teks](cara-kerja-klasifikasi-teks.md).

## Pengantar dan intuisi

Sebelum model dilatih, kita harus sepakat tentang **apa yang dimaksud**
Emergency. Jika dua anotator berbeda pendapat tentang label yang sama, model
tidak mungkin belajar dengan baik. Definisi yang tegas lebih penting daripada
algoritma yang canggih.

!!! warning "Kata kunci bukan definisi"
    Postingan berisi "gempa", "banjir", atau "tolong" **tidak otomatis**
    Emergency. "Tolong doakan korban gempa kemarin" tidak meminta pertolongan
    darurat.

## Konsep

### Unit analisis

Satu **postingan** (satu teks) adalah satu contoh. Konteks utas, gambar, dan
profil tidak digunakan dalam versi dasar proyek ini.

### Definisi operasional

**Emergency** bila postingan memenuhi **kedua** syarat:

1. **Kejadian yang sedang berlangsung atau baru terjadi** (kira-kira jam terakhir menurut isi teks) yang mengancam keselamatan jiwa, kesehatan, atau harta; **dan**
2. Postingan itu **melaporkan kejadian tersebut** atau **meminta bantuan/penyelamatan** terkait kejadian tersebut.

**Non-Emergency** untuk selainnya, termasuk berita, opini, informasi lama, peringatan umum, edukasi, candaan, dan topik tidak terkait.

### Jenis postingan dan labelnya

| Jenis | Ciri | Label | Contoh |
|---|---|---|---|
| Laporan kejadian | Menyatakan kejadian berlangsung di lokasi tertentu | Emergency | "Rumah warga di RT 05 terbakar, api menjalar" |
| Permintaan bantuan | Meminta pertolongan terkait kejadian yang sedang terjadi | Emergency | "Tolong, ibu saya terjebak di lantai 2, air naik" |
| Berita | Pelaporan oleh media, sering ada rujukan sumber | Non-Emergency\* | "BMKG: gempa M4,1 terjadi pukul 08.12" |
| Opini | Pendapat atau emosi tanpa laporan baru | Non-Emergency | "Pemerintah lambat tangani banjir" |
| Informasi lama | Kejadian sudah berlalu/pulih | Non-Emergency | "Banjir kemarin sudah surut" |
| Peringatan umum | Imbauan tanpa kejadian spesifik | Non-Emergency | "Musim hujan, waspada banjir" |

\* Berita tentang kejadian yang sedang berlangsung bisa ambigu; lihat aturan di bawah.

### Aturan anotasi untuk kasus ambigu

1. Jika waktu kejadian tidak jelas dan tidak ada permintaan bantuan, beri **Non-Emergency**.
2. Berita dari akun media tentang kejadian sedang berlangsung dengan korban/ancaman nyata diberi **Emergency** hanya jika teks menyiratkan kejadian masih berlangsung. Catat sebagai kasus ambigu.
3. Sarkasme atau candaan: **Non-Emergency**, kecuali ada permintaan bantuan eksplisit.
4. Jika anotator tetap ragu, tandai `uncertain` untuk ditinjau bersama. **Jangan dipaksakan** sebagai data latih.
5. Jangan menilai berdasarkan siapa penulisnya; nilai isi teksnya.

!!! info "Konsistensi antaranotator"
    Dalam penelitian nyata, dua anotator melabeli sampel yang sama, lalu
    kesepakatan diukur (misalnya dengan Cohen's kappa). Hasil di bawah ambang
    yang disepakati menandakan definisi label perlu diperbaiki.

## Contoh kontekstual kebencanaan

| # | Postingan (sintetis) | Label | Alasan |
|---|---|---|---|
| 1 | "Banjir setinggi dada di Jl. Melati, mohon evakuasi!" | Emergency | Kejadian berlangsung + permintaan bantuan |
| 2 | "Ada yang tahu cara bikin tas siaga bencana?" | Non-Emergency | Pertanyaan edukasi |
| 3 | "Gempa tadi bikin lemari roboh, ada tetangga terluka, butuh ambulans" | Emergency | Kejadian baru + korban + bantuan |
| 4 | "Gempa tadi cuma terasa sebentar, semua aman" | Non-Emergency | Kejadian ada, tidak ada ancaman |
| 5 | "Doakan korban longsor minggu lalu ya" | Non-Emergency | Informasi lama |
| 6 | "Tolong follow akun saya, giveaway!" | Non-Emergency | Kata "tolong" tanpa kejadian |
| 7 | "Asap tebal dari gudang dekat pasar, terdengar ledakan" | Emergency | Laporan kejadian berlangsung |
| 8 | "Jembatan dekat rumah kayaknya mau ambruk" | `uncertain` | Tidak jelas urgensi dan waktu |

## Contoh kode

Pada tahap ini belum perlu kode; keputusan label bersifat manusiawi. Pada
[Mini Proyek](mini-proyek-manual.md) Anda akan menerapkan aturan di atas pada
contoh Anda sendiri.

## Kesalahan umum

- Memakai kata kunci sebagai definisi label.
- Mencampur "berita tentang bencana" dengan "kejadian darurat yang sedang berlangsung".
- Memaksa label pada kasus ragu sehingga data latih berisik.
- Mengubah aturan anotasi di tengah pelabelan tanpa mencatatnya.

## Latihan mandiri

1. Beri label dan alasan untuk lima postingan buatan Anda, termasuk satu yang `uncertain`.
2. Tulis ulang satu postingan Non-Emergency (peringatan umum) menjadi Emergency dengan hanya mengubah beberapa kata.
3. Cari kasus di mana aturan nomor 2 sulit diterapkan, lalu usulkan perbaikan aturan.

## Kuis singkat

**1.** "Banjir kemarin sudah surut, terima kasih relawan." Label?

??? success "Jawaban"
    Non-Emergency: kejadian sudah berlalu dan tidak ada permintaan bantuan.

**2.** Mengapa label `uncertain` tidak langsung dipakai sebagai data latih?

??? success "Jawaban"
    Label yang ragu menambah noise; sebaiknya ditinjau bersama atau dikecualikan.

**3.** Apa dua syarat Emergency pada definisi operasional?

??? success "Jawaban"
    Kejadian berlangsung/baru terjadi yang mengancam, dan postingan melaporkannya atau meminta bantuan terkait kejadian itu.

## Ringkasan

Definisi label yang eksplisit dan aturan anotasi untuk kasus ambigu adalah
fondasi proyek. Kata kunci bukan definisi; waktu, ancaman, dan maksud
postingan yang menentukan.

## Referensi

- Imran, M., dkk. (2015). Processing social media messages in mass emergency: A survey. *ACM Computing Surveys*, 47(4).

## Materi selanjutnya

[Mengenal Teks Media Sosial](teks-media-sosial.md)
