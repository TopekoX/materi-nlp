"""Pembangkit dataset SINTETIS untuk NLP Learning Hub.

PERINGATAN: semua teks di sini dibuat dari templat dan bukan postingan nyata.
Label mengikuti definisi operasional di docs/level-0-orientasi/masalah-emergency.md,
bukan hasil anotasi manusia. Dataset ini hanya untuk belajar; skornya bukan
bukti bahwa model berfungsi pada data Twitter/X yang sesungguhnya.

Menjalankan:  python generate_dataset.py
Hasil      :  data/synthetic_disaster_id.csv
"""
import csv
import random
from pathlib import Path

SEED = 20261023
JUMLAH_EVENT = 80
JUMLAH_RETWEET = 10  # duplikat persis yang disengaja (meniru "RT")

KELURAHAN = [
    "Sukamaju", "Harapan Jaya", "Cibening", "Tanjung Asri", "Mekar Sari",
    "Bumi Indah", "Karang Tengah", "Sidomulyo", "Lembah Hijau", "Pasir Putih",
]
JALAN = [
    "Jl. Melati", "Jl. Kenanga", "Jl. Mawar", "Jl. Anggrek", "Jl. Cempaka",
    "Jl. Pahlawan", "Jl. Dahlia", "Gang Flamboyan",
]
TINGGI = ["setinggi lutut", "setinggi pinggang", "setinggi dada", "hampir sampai atap"]
JAM = ["06.45", "08.12", "11.30", "14.05", "19.40", "22.15"]

# Setiap bahaya punya templat untuk empat jenis postingan yang bergantung pada kejadian.
BAHAYA = {
    "banjir": {
        "laporan": [
            "Air banjir {tinggi} di {lok}, masih terus naik.",
            "Banjir masuk ke rumah-rumah warga {kel}, air sudah {tinggi}.",
            "Sungai meluap, jalan {lok} terendam {tinggi}, motor tidak bisa lewat.",
            "Warga {lok} mulai mengungsi ke musala karena air terus naik sejak tadi.",
        ],
        "bantuan": [
            "Tolong, air sudah masuk ke rumah kami di {lok}, ada dua lansia yang tidak bisa jalan.",
            "Butuh perahu karet segera di {lok}, anak-anak terjebak di lantai dua.",
            "Mohon bantuan evakuasi di {kel}, air {tinggi} dan listrik padam.",
        ],
        "berita": [
            "Pemkot mengumumkan pembangunan tanggul baru di {kel} untuk mengurangi risiko banjir.",
            "Dinas PU menganggarkan normalisasi sungai di {kel} tahun depan.",
        ],
        "info_lama": [
            "Banjir kemarin di {kel} sudah surut, terima kasih kepada para relawan.",
            "Alhamdulillah air sudah turun, warga {lok} mulai membersihkan lumpur sisa banjir minggu lalu.",
        ],
    },
    "gempa": {
        "laporan": [
            "Gempa barusan terasa sangat kuat di {kel}, tembok rumah retak dan warga berlarian keluar.",
            "Setelah gempa tadi, atap ruko di {lok} runtuh dan ada yang tertimpa.",
            "Gempa susulan masih terasa, warga {lok} bertahan di lapangan karena bangunan rusak.",
            "Listrik padam dan gedung sekolah di {kel} retak parah setelah guncangan barusan.",
        ],
        "bantuan": [
            "Tolong, ada korban tertimpa reruntuhan di {lok}, butuh ambulans sekarang.",
            "Mohon bantuan tim SAR, tetangga kami terjebak di dalam rumah yang roboh di {lok}.",
            "Butuh tenda dan obat-obatan di lapangan {kel}, banyak warga luka akibat gempa tadi.",
        ],
        "berita": [
            "BMKG: gempa magnitudo 4,1 terjadi pukul {jam}, tidak berpotensi tsunami dan tidak ada laporan kerusakan.",
            "Pemerintah daerah memperketat aturan bangunan tahan gempa di {kel}.",
        ],
        "info_lama": [
            "Sudah seminggu sejak gempa, rumah warga {kel} masih diperbaiki pelan-pelan.",
            "Doakan korban gempa tahun lalu di {kel} ya, hari ini kami mengadakan doa bersama.",
        ],
    },
    "kebakaran": {
        "laporan": [
            "Api membesar di rumah warga {lok}, asap hitam terlihat dari jauh.",
            "Kebakaran di pasar {kel} sedang berlangsung, kios-kios sebelah mulai terbakar.",
            "Terdengar ledakan dan asap tebal dari gudang di {lok}.",
            "Api menjalar ke atap rumah tetangga di {lok}, warga berusaha memadamkan dengan ember.",
        ],
        "bantuan": [
            "Tolong hubungi damkar, rumah di {lok} terbakar dan ada anak di dalam!",
            "Mohon kirim mobil pemadam ke {lok} sekarang, api sudah besar.",
            "Butuh bantuan evakuasi, asap tebal di apartemen {kel}, kami terjebak di lantai tiga.",
        ],
        "berita": [
            "Dinas pemadam kebakaran menggelar simulasi evakuasi di {kel} hari Sabtu.",
            "Pemkot menambah dua unit mobil pemadam untuk wilayah {kel}.",
        ],
        "info_lama": [
            "Api di gudang {kel} semalam sudah padam, tidak ada korban jiwa.",
            "Terima kasih damkar, kebakaran di rumah tetangga {lok} kemarin sudah berhasil dipadamkan.",
        ],
    },
    "longsor": {
        "laporan": [
            "Tebing longsor menimpa rumah warga di {lok}, tanah masih bergerak.",
            "Jalan menuju {kel} tertutup longsor, ada mobil yang terjebak di bawah material.",
            "Longsor susulan baru saja terjadi di {lok}, beberapa rumah tertimbun.",
            "Tanah di belakang rumah kami di {lok} retak dan mulai ambles, hujan belum berhenti.",
        ],
        "bantuan": [
            "Tolong, keluarga kami tertimbun longsor di {lok}, butuh alat berat dan tim SAR segera.",
            "Mohon bantuan evakuasi, warga {lok} terisolasi akibat jalan tertutup longsor.",
            "Butuh relawan dan cangkul di {lok}, masih ada yang tertimbun.",
        ],
        "berita": [
            "Pemkab merencanakan penanaman pohon di lereng {kel} untuk mencegah longsor.",
            "Peta rawan longsor {kel} diperbarui oleh dinas terkait dan dapat diunduh warga.",
        ],
        "info_lama": [
            "Jalan {kel} yang tertutup longsor bulan lalu kini sudah dibuka kembali.",
            "Setahun lalu longsor di {kel}, hari ini warga mengenang para korban.",
        ],
    },
    "angin kencang": {
        "laporan": [
            "Angin puting beliung menerjang {kel} barusan, atap rumah beterbangan.",
            "Pohon besar tumbang menimpa rumah di {lok} akibat angin kencang, jalan tertutup.",
            "Angin kencang masih berlangsung di {lok}, baliho roboh menimpa kendaraan.",
            "Atap sekolah di {kel} terbang terbawa angin, murid-murid dievakuasi ke ruang aman.",
        ],
        "bantuan": [
            "Tolong, pohon tumbang menimpa rumah kami di {lok}, ada yang terjepit!",
            "Mohon bantuan, atap rumah kami hilang diterbangkan angin dan ada bayi di dalamnya, {lok}.",
            "Butuh terpal dan bantuan evakuasi di {kel}, puluhan rumah rusak diterjang angin.",
        ],
        "berita": [
            "Pemkot menebang pohon rawan tumbang di sepanjang {jalan} sebagai langkah pencegahan.",
            "Hasil kajian menyebut kawasan {kel} termasuk wilayah yang sering dilalui angin kencang.",
        ],
        "info_lama": [
            "Puting beliung di {kel} minggu lalu merusak belasan atap, kini sudah diperbaiki gotong royong.",
            "Pohon tumbang kemarin di {lok} sudah dipotong dan jalan kembali lancar.",
        ],
    },
    "letusan gunung": {
        "laporan": [
            "Gunung mengeluarkan letusan besar barusan, hujan abu tebal turun di {kel}.",
            "Abu vulkanik menutup jalan di {lok}, jarak pandang tinggal beberapa meter.",
            "Kolom asap setinggi ribuan meter terlihat dari {kel}, warga mulai panik dan mengungsi.",
            "Terdengar dentuman keras dari gunung dan kerikil panas jatuh di sekitar {lok}.",
        ],
        "bantuan": [
            "Tolong, kami butuh masker dan evakuasi di {lok}, abu sangat tebal dan banyak anak sesak napas.",
            "Mohon bantuan truk untuk mengangkut warga lansia {kel} ke posko pengungsian.",
            "Butuh air bersih dan masker di pengungsian {kel}, abu masih terus turun.",
        ],
        "berita": [
            "Badan Geologi memperbarui peta kawasan rawan letusan gunung untuk wilayah {kel}.",
            "Pemkab menyiapkan jalur evakuasi permanen untuk warga lereng gunung di {kel}.",
        ],
        "info_lama": [
            "Abu letusan bulan lalu di {kel} sudah dibersihkan, sekolah kembali buka.",
            "Terima kasih relawan yang membantu membersihkan abu vulkanik di {lok} kemarin.",
        ],
    },
}

# Templat umum: {hz} diisi nama bahaya pada kejadian tersebut.
UMUM = {
    "opini": [
        "Pemerintah lambat sekali menangani {hz} di kota ini.",
        "Kenapa {hz} selalu datang setiap tahun tapi solusinya tidak pernah jelas?",
        "Capek lihat berita {hz} terus, kapan ada perbaikan tata kota?",
        "Menurut saya anggaran penanganan {hz} harus dinaikkan.",
        "Kasihan korban {hz}, semoga pemerintah lebih serius ke depan.",
        "Setiap ada {hz} yang disalahkan selalu warga, padahal tata ruangnya bermasalah.",
        "Debat soal penanganan {hz} makin seru, tapi belum ada tindakan nyata.",
        "Saya kurang setuju kalau dana mitigasi {hz} dipotong tahun ini.",
    ],
    "peringatan": [
        "Musim pancaroba sudah dekat, waspada {hz} ya semuanya.",
        "Imbauan: siapkan tas siaga untuk menghadapi {hz}, simpan dokumen penting dalam wadah kedap air.",
        "Hati-hati, wilayah {kel} termasuk rawan {hz}. Kenali jalur evakuasi terdekat.",
        "Ingat, jaga lingkungan agar risiko {hz} berkurang.",
        "Masyarakat diminta tetap waspada terhadap potensi {hz} sepekan ke depan.",
    ],
    "edukasi": [
        "Tips menghadapi {hz}: kenali jalur evakuasi dan kumpulkan nomor darurat.",
        "Webinar gratis tentang mitigasi {hz} akan digelar hari Sabtu pukul 10.00.",
        "Thread: sejarah {hz} terbesar di Indonesia dan pelajaran yang bisa kita ambil.",
        "Ada yang tahu cara membuat tas siaga untuk {hz}?",
        "Materi kuliah hari ini membahas penyebab {hz} dan upaya mitigasinya.",
        "Kenapa sih {hz} bisa terjadi? Simak penjelasan sederhana ini.",
    ],
    "candaan": [
        "Skripsiku udah kayak {hz}, datang tiba-tiba dan susah diatasi wkwk",
        "Mantan datang lagi, rasanya kayak {hz} di hati haha",
        "Tagihan bulan ini bikin dompet kena {hz} wkwk",
        "Nilai ujianku jatuh kayak {hz}, hancur semuanya haha",
        "Lapar banget, perutku bunyi kayak {hz} wkwk",
    ],
}

# Kata pemicu seperti "tolong"/"api"/"banjir" yang BUKAN kejadian darurat.
TIDAK_TERKAIT = [
    "Tolong follow akun saya ya, ada giveaway hari ini!",
    "Tolong dong rekomendasi laptop murah buat kuliah.",
    "Api semangat kerja belum padam walau deadline menumpuk.",
    "Diskon besar-besaran, harga banjir promo di toko kami!",
    "Tolong share ya, kami sedang mencari kos dekat kampus.",
    "Konser semalam gila, penonton berteriak sampai getarannya terasa seperti gempa wkwk",
    "Kopi ini panas banget, lidahku terbakar.",
    "Tolong bantu vote kontes foto kucing saya.",
    "Harga cabai naik lagi, ibu-ibu di pasar mulai kebakaran jenggot.",
    "Notifikasi ponselku longsor, pesan masuk banyak sekali.",
    "Diskusi kelompok tadi panas banget, hampir meledak wkwk",
    "Butuh bantuan: ada yang bisa ajarin Python dasar?",
    "Antrean tiket konser kayak banjir manusia, sabar ya semua.",
    "Tolong jangan spoiler dulu, filmnya belum selesai kutonton.",
    "Gunung cucian di rumah sudah tinggi banget, tolong semangatin aku.",
    "Pukul 08.12 kereta berangkat, jangan sampai ketinggalan ya.",
    "Warung sebelah kampus buka lagi, nasi goreng enak dan murah.",
    "Tolong kasih saran warna cat yang cocok buat kamar kecil.",
    "Lagu baru mereka meledak di tangga lagu minggu ini.",
    "Kemacetan pagi ini parah, jalanan seperti lautan kendaraan.",
]

# Variasi gaya informal. Peluangnya SAMA untuk kedua label agar tidak menjadi jalan pintas.
SINGKATAN = {
    "yang": "yg", "tidak": "gak", "sudah": "udah", "dengan": "dgn", "untuk": "utk",
    "karena": "krn", "sekarang": "skrg", "banget": "bgt", "belum": "blm",
    "tolong": "tlg", "orang": "org", "rumah": "rmh", "kami": "kita",
    "warga": "wrg", "jalan": "jln", "dan": "&", "juga": "jg", "tetapi": "tp",
}
EMOJI = ["🙏", "😭", "🔥", "🌊", "😂", "😱", "🚨", "🥺"]
HASHTAG = ["#SiagaBencana", "#InfoBencana", "#Cuaca", "#JagaSesama", "#kota"]
MENTION = ["@bpbd_contoh", "@relawan_contoh", "@info_siaga_contoh"]


def _huruf_berulang(kata, rng):
    """Memanjangkan satu vokal, mis. tolong -> tolooong."""
    posisi = [i for i, c in enumerate(kata) if c in "aiueo"]
    if not posisi:
        return kata
    i = rng.choice(posisi)
    return kata[: i + 1] + kata[i] * rng.randint(2, 3) + kata[i + 1 :]


def _typo(kata, rng):
    """Menukar dua huruf bersebelahan di tengah kata (kata minimal 5 huruf)."""
    if len(kata) < 5:
        return kata
    i = rng.randint(1, len(kata) - 3)
    return kata[:i] + kata[i + 1] + kata[i] + kata[i + 2 :]


def beri_gaya_informal(teks, rng):
    """Menerapkan variasi gaya acak. Peluang tidak bergantung pada label."""
    kata = teks.split(" ")
    if rng.random() < 0.5:
        kata = [
            SINGKATAN[k.lower()] if k.lower() in SINGKATAN and rng.random() < 0.6 else k
            for k in kata
        ]
    if rng.random() < 0.12:
        i = rng.randrange(len(kata))
        kata[i] = _huruf_berulang(kata[i], rng)
    if rng.random() < 0.08:
        i = rng.randrange(len(kata))
        kata[i] = _typo(kata[i], rng)
    teks = " ".join(kata)
    if rng.random() < 0.08:
        teks = teks.upper()
    if rng.random() < 0.15:
        teks = f"{rng.choice(MENTION)} {teks}"
    if rng.random() < 0.25:
        teks = f"{teks} {rng.choice(HASHTAG)}"
    if rng.random() < 0.18:
        teks = f"{teks} {rng.choice(EMOJI)}"
    if rng.random() < 0.12:
        teks = f"{teks} https://contoh.example/{rng.randrange(10**5):05d}"
    return teks


def buat_event(idx, rng):
    kel = rng.choice(KELURAHAN)
    jalan = rng.choice(JALAN)
    return {
        "event_id": f"E{idx:03d}",
        "bahaya": rng.choice(list(BAHAYA)),
        "kel": f"Kelurahan {kel}",
        "jalan": jalan,
        "lok": f"{jalan} RT {rng.randint(1, 12):02d}",
    }


def isi_slot(templat, event, rng):
    return templat.format(
        tinggi=rng.choice(TINGGI), lok=event["lok"], kel=event["kel"],
        jalan=event["jalan"], jam=rng.choice(JAM), hz=event["bahaya"],
    )


def bangkitkan():
    rng = random.Random(SEED)
    baris, terpakai = [], set()

    def tambah(event, jenis, label, kode_templat, teks):
        for _ in range(20):  # coba beberapa gaya sampai teksnya unik
            hasil = beri_gaya_informal(teks, rng)
            if hasil not in terpakai:
                terpakai.add(hasil)
                baris.append({
                    "event_id": event["event_id"], "post_type": jenis,
                    "template_id": kode_templat, "text": hasil, "label": label,
                })
                return

    for n in range(1, JUMLAH_EVENT + 1):
        ev = buat_event(n, rng)
        T = BAHAYA[ev["bahaya"]]
        rencana = (
            [("laporan", "Emergency")] * rng.randint(1, 2)
            + [("bantuan", "Emergency")] * rng.randint(0, 2)
            + [("berita", "Non-Emergency")] * rng.randint(0, 1)
            + [("info_lama", "Non-Emergency")] * rng.randint(0, 1)
            + [("opini", "Non-Emergency")] * rng.randint(0, 1)
            + [("peringatan", "Non-Emergency")] * rng.randint(0, 1)
            + [("edukasi", "Non-Emergency")] * rng.randint(0, 1)
            + [("candaan", "Non-Emergency")] * rng.randint(0, 1)
            + [("tidak_terkait", "Non-Emergency")] * rng.randint(1, 2)
        )
        for jenis, label in rencana:
            if jenis == "tidak_terkait":
                k = rng.randrange(len(TIDAK_TERKAIT))
                tambah(ev, jenis, label, f"tidak_terkait-{k}", TIDAK_TERKAIT[k])
            else:
                kumpulan = T[jenis] if jenis in T else UMUM[jenis]
                k = rng.randrange(len(kumpulan))
                kode = f"{ev['bahaya']}-{jenis}-{k}" if jenis in T else f"umum-{jenis}-{k}"
                tambah(ev, jenis, label, kode, isi_slot(kumpulan[k], ev, rng))

    # "Retweet": duplikat persis dari postingan Emergency pada kejadian yang sama.
    emergency = [b for b in baris if b["label"] == "Emergency"]
    for b in rng.sample(emergency, JUMLAH_RETWEET):
        baris.append(dict(b))

    # source_id diberikan setelah semua baris ada; urutan diacak agar baris sekejadian tidak berurutan.
    rng.shuffle(baris)
    for i, b in enumerate(baris, start=1):
        b["source_id"] = f"S{i:04d}"
    return baris


def tulis(baris, path):
    kolom = ["source_id", "event_id", "post_type", "template_id", "text", "label"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=kolom)
        w.writeheader()
        w.writerows(baris)


if __name__ == "__main__":
    tujuan = Path(__file__).resolve().parent / "data" / "synthetic_disaster_id.csv"
    data = bangkitkan()
    tulis(data, tujuan)
    print(f"Menulis {len(data)} baris ke {tujuan}")
