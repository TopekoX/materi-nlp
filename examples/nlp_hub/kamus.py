"""Kamus kecil untuk preprocessing teks Indonesia.

Seluruh kamus di sini DIBUAT TANGAN, kecil, dan hanya untuk belajar. Cakupannya
jauh dari lengkap. Untuk data nyata, kamus harus dibangun dan divalidasi dari
korpus yang sesuai.
"""

# Bentuk informal/singkatan -> bentuk baku. Kunci harus huruf kecil.
KAMUS_INFORMAL = {
    "yg": "yang", "dgn": "dengan", "dg": "dengan", "utk": "untuk", "untk": "untuk",
    "krn": "karena", "karna": "karena", "tp": "tetapi", "jg": "juga", "sm": "sama",
    "gak": "tidak", "ga": "tidak", "nggak": "tidak", "ngga": "tidak", "tdk": "tidak",
    "gk": "tidak", "enggak": "tidak", "tak": "tidak",
    "udah": "sudah", "udh": "sudah", "sdh": "sudah", "dah": "sudah",
    "blm": "belum", "belom": "belum",
    "bgt": "sangat", "banget": "sangat", "bngt": "sangat",
    "skrg": "sekarang", "sekrg": "sekarang", "lg": "lagi", "lgi": "lagi",
    "tlg": "tolong", "tolg": "tolong", "tlong": "tolong",
    "org": "orang", "orng": "orang", "rmh": "rumah", "jln": "jalan", "jl": "jalan",
    "wrg": "warga", "kmrn": "kemarin", "kemaren": "kemarin", "hrs": "harus",
    "bs": "bisa", "bsa": "bisa", "cepet": "cepat", "cpt": "cepat", "brp": "berapa",
    "pd": "pada", "dr": "dari", "dlm": "dalam", "spy": "supaya", "biar": "agar",
    "trs": "terus", "terus2": "terus", "mohon2": "mohon",
    "sat": "saat", "maf": "maaf",  # hasil pemendekan huruf berulang (saaat, maaaf)
}

# Kata fungsi yang relatif aman dibuang. SENGAJA tidak memuat negasi (tidak, belum,
# bukan, jangan), kata permintaan (tolong, mohon, butuh), kata ganti orang (kami, saya),
# dan kata kejadian. Daftar bawaan Sastrawi memuat 'tidak', 'belum', dan 'tolong'.
STOPWORDS_KONSERVATIF = frozenset({
    "yang", "di", "ke", "dari", "dan", "atau", "itu", "ini", "untuk", "dengan",
    "pada", "adalah", "juga", "oleh", "dalam", "sebagai", "para", "sih", "deh",
    "dong", "nih", "tuh", "ya", "lah", "kok", "pun", "tersebut", "agar", "supaya",
})

KATA_NEGASI = frozenset({"tidak", "bukan", "belum", "jangan", "tak"})

EMOJI_KE_KATA = {
    "🙏": "emo_doa", "😭": "emo_menangis", "🔥": "emo_api", "🌊": "emo_ombak",
    "😂": "emo_tertawa", "🤣": "emo_tertawa", "😱": "emo_takut", "🚨": "emo_sirene",
    "🥺": "emo_memohon", "🆘": "emo_sos", "❤": "emo_hati", "👍": "emo_setuju",
}

# Urutan penting: pola yang lebih panjang harus dicocokkan lebih dulu.
EMOTIKON_KE_KATA = {
    ":'(": "emo_menangis", "T_T": "emo_menangis", ":(": "emo_sedih",
    ":D": "emo_tertawa", ":)": "emo_senyum", ":-)": "emo_senyum", ":-(": "emo_sedih",
}

# Kosakata domain untuk contoh koreksi typo (bukan kamus bahasa Indonesia lengkap).
KOSAKATA_DOMAIN = frozenset({
    "banjir", "gempa", "kebakaran", "longsor", "tolong", "bantuan", "evakuasi",
    "korban", "terjebak", "mengungsi", "ambulans", "pemadam", "listrik", "padam",
    "rumah", "warga", "jalan", "air", "naik", "api", "asap", "ledakan", "roboh",
    "tertimbun", "terluka", "angin", "pohon", "tumbang", "letusan", "abu", "gunung",
    "barusan", "sekarang", "segera", "mohon", "butuh", "sungai", "meluap",
})

# Nama tempat FIKTIF yang dipakai dataset sintetis (gazetteer sederhana).
NAMA_TEMPAT_CONTOH = (
    "sukamaju", "harapan jaya", "cibening", "tanjung asri", "mekar sari",
    "bumi indah", "karang tengah", "sidomulyo", "lembah hijau", "pasir putih",
)
