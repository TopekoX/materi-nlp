"""Menulis set uji tulis-tangan SINTETIS (48 teks).

Teks ditulis manual dengan gaya yang sengaja berbeda dari templat di
generate_dataset.py. Label mengikuti definisi operasional di
docs/level-0-orientasi/masalah-emergency.md. Ini BUKAN hasil anotasi oleh
beberapa anotator dan bukan ground truth ilmiah. Kolom `catatan` mencatat
kasus yang menurut penulis ambigu.

Menjalankan:  python tulis_uji_tangan.py
Hasil      :  data/handwritten_challenge_id.csv
"""
import csv
from pathlib import Path

E, N = "Emergency", "Non-Emergency"

# (label, teks, catatan)
BARIS = [
    (E, "Astaga dapur tetangga meledak, apinya udah ngejalar ke atap. Siapa punya APAR? Jl. Cendana 4", ""),
    (E, "air di lorong rumah gue udh sepinggang dan masih nambah, listrik gue matiin. ada yg punya pelampung buat bocil?", ""),
    (E, "Bumi goyang kenceng bgt barusan!! plafon kamar jatuh, kaki adek kejepit. ada dokter di sekitar sini??", ""),
    (E, "Mohon info: jalur Puncak km 12 baru saja longsor, 2 mobil keseret ke jurang. sudah ada tim yg ke sana?", ""),
    (E, "kapal nelayan kami bocor dan miring di sebelah barat dermaga, 6 orang di atas, tolong hubungkan ke Basarnas", "di luar enam bahaya pada dataset latih"),
    (E, "pak RT, rumah bu Ningsih ambruk kena angin tadi, beliau ketimpa kayu. tolong ambulans ke gang 3", ""),
    (E, "asap putih tebal keluar dari ventilasi pabrik sebelah, mata perih, anak-anak sekolah di depannya batuk2", "tidak ada permintaan bantuan eksplisit; ancaman kesehatan sedang berlangsung"),
    (E, "Sungai belakang rumah jebol 10 menit lalu. Kami lari ke atap masjid, ada 30an orang. Sinyal tinggal 1 bar.", ""),
    (E, "Banjir bandang!!! jembatan putus, desa kami terisolasi, stok obat diabetes ibu habis", ""),
    (E, "Tanah di samping rumah turun sekitar 1 meter sejak subuh dan masih turun, kami mengungsi ke rumah paman, tolong cek BPBD", ""),
    (E, "Ada bau gas menyengat di gang kami dan tabung bocor berdesis, jangan ada yang nyalain rokok! hubungi pemadam", ""),
    (E, "gunung bunyi dentuman 3x barusan, abu mulai turun di desa kami, mau mengungsi tapi mobil kami cuma muat 5", ""),
    (E, "Air laut surut tiba2 lalu balik naik masuk ke warung pantai, semua lari ke bukit sekarang!", "tsunami tidak ada di dataset latih"),
    (E, "kebakaran hutan makin dekat ke kampung, api sdh 200 m dari rumah warga. butuh air dan bantuan pemadam!", ""),
    (E, "Mohon bantuan, ibu hamil 8 bulan terjebak banjir di perumahan Griya Asri blok C, ketubannya pecah", ""),
    (E, "ledakan di bengkel las, 2 orang terbakar parah, kami nunggu ambulans di depan gerbang", ""),
    (E, "pohon tumbang nutup jalan sekaligus nimpa mobil, ada org dlm mobil blm bisa keluar. depan SDN 3.", ""),
    (E, "Rumah sakit kami kebanjiran, pasien ICU perlu dipindahkan, kami butuh generator dan ambulans", ""),
    (E, "gempa barusan kerasa banget, saya di lantai 9, tangga penuh orang panik, ada yang pingsan", "tidak ada permintaan bantuan eksplisit"),
    (E, "Angin kenceng ngangkat seng warung sampai nancep ke jalan, pengendara motor jatuh berdarah, tolong", ""),
    (E, "arus sungai bawa anak SD yg main di tepi, org2 lagi ngejar, tlg bantu cari ke arah hilir jembatan merah", ""),
    (E, "Kami 12 orang terjebak di gua karena air naik cepat setelah hujan deras, baterai senter menipis", ""),
    (E, "jalan raya depan pasar amblas, motor masuk lubang, mungkin ada yg tertimbun", ""),
    (E, "ada korsleting di gardu depan rumah, percikan api besar dan kabel putus menyentuh genangan air, jauhi area ini dan hubungi PLN", ""),
    (N, "Alhamdulillah rumah kami aman semua setelah gempa tadi pagi, cuma gelas pecah. Terima kasih yang sudah menanyakan kabar.", "kejadian ada, ancaman sudah tidak ada"),
    (N, "Hari ini sekolah anak diliburkan karena prakiraan hujan lebat, semoga tidak terjadi apa-apa.", ""),
    (N, "Dulu waktu kecil rumah nenek sering kebanjiran, kenangan banget main perahu kardus di halaman.", ""),
    (N, "Rapat RW malam ini bahas kerja bakti bersihin selokan sebelum musim hujan, yang bisa datang jam 8 ya.", ""),
    (N, "BNPB merilis laporan tahunan jumlah kejadian bencana, banjir masih mendominasi.", ""),
    (N, "tolong bantu RT ya, kita lagi galang dana buat beli pompa air cadangan untuk musim hujan nanti", "kata 'tolong' dan topik air, tanpa kejadian"),
    (N, "Film dokumenter soal letusan gunung tadi malam bagus banget, sinematografinya keren.", ""),
    (N, "Kebakaran di sinetron semalam lebay amat, apinya jelas efek komputer wkwk", ""),
    (N, "Saya takut gempa, makanya tiap malam tas siaga sudah disiapkan di dekat pintu.", ""),
    (N, "Dua tahun lalu longsor di kampung kami menewaskan beberapa tetangga. Hari ini kami ziarah bersama.", ""),
    (N, "Info: besok jam 9 akan ada simulasi evakuasi gempa di gedung kantor, mohon semua karyawan ikut.", ""),
    (N, "Mahasiswa teknik sipil bikin alat peringatan dini banjir murah, keren banget idenya!", ""),
    (N, "Lagi nonton berita banjir di kota lain, sedih sih lihatnya, semoga cepat pulih ya.", "ambigu: empati atas kejadian di tempat lain, bukan laporan atau permintaan bantuan"),
    (N, "Siapa yang tahu kontak tukang service AC yang bisa datang hari ini? tolong ya", ""),
    (N, "Hujan deras banget malam ini, enaknya makan mie rebus sambil nonton drama.", ""),
    (N, "Pemkab menyalurkan bantuan sembako ke warga terdampak banjir bulan lalu.", ""),
    (N, "Tim SAR menghentikan pencarian korban longsor pada hari ketujuh sesuai prosedur.", "ambigu: berita; operasi sudah berakhir"),
    (N, "Tolong dong, ada yang bisa bantu benerin laptop saya, layarnya mati total 😭", ""),
    (N, "Peringatan dini BMKG: hujan lebat disertai petir berpotensi terjadi di sebagian wilayah sore ini.", "ambigu: peringatan umum tanpa kejadian spesifik"),
    (N, "Api unggun di acara pramuka semalam seru banget, nyanyi sampai larut.", ""),
    (N, "Debu pembangunan jalan bikin mata perih tiap lewat sini, kapan selesai ya?", "opini/keluhan, bukan kejadian darurat"),
    (N, "Kapan ya gempa besar yang sering dibahas pakar itu datang? Cuma penasaran, bukan menakut-nakuti.", ""),
    (N, "Gempa kecil tadi sore cuma bikin lampu gantung goyang, tidak ada kerusakan. Aman.", "kejadian baru tetapi tanpa ancaman"),
    (N, "Banjir rob di pantai utara itu memang masalah tahunan, perlu solusi jangka panjang bukan sekadar tanggul.", ""),
]


def tulis(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_id", "text", "label", "catatan"])
        for i, (label, teks, catatan) in enumerate(BARIS, start=1):
            w.writerow([f"H{i:03d}", teks, label, catatan])


if __name__ == "__main__":
    tujuan = Path(__file__).resolve().parent / "data" / "handwritten_challenge_id.csv"
    tulis(tujuan)
    print(f"Menulis {len(BARIS)} baris ke {tujuan}")
