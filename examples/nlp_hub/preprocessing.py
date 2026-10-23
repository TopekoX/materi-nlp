"""Preprocessing teks Indonesia: satu fungsi kecil per langkah, lalu digabung.

Hampir semua fungsi di sini TANPA STATE: hasilnya hanya bergantung pada teks
masuk dan parameter, tidak mempelajari apa pun dari korpus. Karena itu aman
dipakai di dalam pipeline tanpa risiko kebocoran data (lihat halaman
"Data leakage akibat preprocessing").
"""
import difflib
import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache

from sklearn.base import BaseEstimator, TransformerMixin

from .kamus import (
    EMOJI_KE_KATA, EMOTIKON_KE_KATA, KAMUS_INFORMAL, KATA_NEGASI, KOSAKATA_DOMAIN,
    NAMA_TEMPAT_CONTOH, STOPWORDS_KONSERVATIF,
)

# ---------------------------------------------------------------- unicode & huruf
KARAKTER_TAK_TERLIHAT = dict.fromkeys(map(ord, "​‌‍⁠﻿️"))


def normalisasi_unicode(teks):
    """NFKC menyatukan variasi bentuk huruf; karakter tak terlihat dibuang."""
    teks = unicodedata.normalize("NFKC", teks)
    return teks.translate(KARAKTER_TAK_TERLIHAT)


def case_folding(teks):
    """Mengubah ke huruf kecil."""
    return teks.lower()


# ---------------------------------------------------------------- url, mention, hashtag
POLA_URL = re.compile(r"https?://\S+|www\.\S+")
POLA_MENTION = re.compile(r"@\w+")
POLA_HASHTAG = re.compile(r"#(\w+)")
POLA_HURUF_BESAR = re.compile(r"(?<=[a-z])(?=[A-Z])")


def ganti_url(teks, token="tok_url"):
    return POLA_URL.sub(f" {token} ", teks)


def ganti_mention(teks, token="tok_mention"):
    return POLA_MENTION.sub(f" {token} ", teks)


def proses_hashtag(teks, mode="kata"):
    """Menangani hashtag. mode: 'pertahankan' | 'hapus' | 'kata'.

    'kata' membuang tanda # dan memisahkan CamelCase: #SiagaBencana -> Siaga Bencana.
    Panggil SEBELUM case folding, karena huruf besar adalah petunjuk pemisah.
    """
    if mode == "pertahankan":
        return teks
    if mode == "hapus":
        return POLA_HASHTAG.sub(" ", teks)
    if mode == "kata":
        return POLA_HASHTAG.sub(lambda m: " " + POLA_HURUF_BESAR.sub(" ", m.group(1)) + " ", teks)
    raise ValueError(f"mode hashtag tidak dikenal: {mode!r}")


# ---------------------------------------------------------------- emoji & emotikon
POLA_EMOJI = re.compile("[\U0001F100-\U0001F1FF\U0001F300-\U0001FAFF☀-➿]")
POLA_EMOTIKON = re.compile(
    "|".join(re.escape(e) for e in sorted(EMOTIKON_KE_KATA, key=len, reverse=True))
)


def proses_emoji(teks, mode="kata"):
    """Menangani emoji dan emotikon. mode: 'pertahankan' | 'hapus' | 'kata'."""
    if mode == "pertahankan":
        return teks
    if mode == "hapus":
        return POLA_EMOJI.sub(" ", POLA_EMOTIKON.sub(" ", teks))
    if mode == "kata":
        teks = POLA_EMOTIKON.sub(lambda m: f" {EMOTIKON_KE_KATA[m.group(0)]} ", teks)
        return POLA_EMOJI.sub(lambda m: f" {EMOJI_KE_KATA.get(m.group(0), 'emo_lain')} ", teks)
    raise ValueError(f"mode emoji tidak dikenal: {mode!r}")


# ---------------------------------------------------------------- huruf berulang & informal
POLA_HURUF_BERULANG = re.compile(r"([^\W\d_])\1{2,}")  # huruf yang sama minimal 3 kali


def kurangi_huruf_berulang(teks):
    """Memendekkan huruf yang berulang 3x atau lebih menjadi satu: tolooong -> tolong.

    Hanya HURUF yang diproses. Pola \\w akan merusak angka (1000 -> 10).
    """
    return POLA_HURUF_BERULANG.sub(r"\1", teks)


def normalisasi_informal(token, kamus=KAMUS_INFORMAL):
    return kamus.get(token, token)


def koreksi_typo(token, kosakata=KOSAKATA_DOMAIN, batas=0.85):
    """Mengganti token dengan kata terdekat di `kosakata` bila kemiripannya >= batas.

    Berisiko: kata yang benar tetapi tidak ada di kosakata dapat salah diganti.
    """
    if token in kosakata or len(token) < 4:
        return token
    cocok = difflib.get_close_matches(token, kosakata, n=1, cutoff=batas)
    return cocok[0] if cocok else token


# ---------------------------------------------------------------- angka, waktu, lokasi
POLA_WAKTU = re.compile(r"\b(?:(?:pukul|jam)\s*)?(?:[01]?\d|2[0-3])[.:][0-5]\d(?:\s*wib|\s*wita|\s*wit)?\b")
POLA_ANGKA = re.compile(r"(?<![\w.,])\d+(?:[.,]\d+)*\b")  # angka mandiri; yang menempel pada huruf dibiarkan
POLA_RT_RW = re.compile(r"\brt\s*\.?\s*\d+(?:\s*/\s*rw\s*\.?\s*\d+)?")
POLA_JALAN = re.compile(r"\b(?:jl|jln|jalan|gang|gg)\.?\s+\w+(?:\s+rt\s*\.?\s*\d+(?:\s*/\s*rw\s*\.?\s*\d+)?)?")
POLA_AWALAN_WILAYAH = re.compile(r"\b(?:kelurahan|kel|desa|kampung|kecamatan|kec|kabupaten|kab|kota)\.?\s+(?!(?:ini|itu|yang|sebelah)\b)\w+")


def normalisasi_waktu(teks, token="tok_waktu"):
    return POLA_WAKTU.sub(f" {token} ", teks)


def normalisasi_angka(teks, token="tok_angka"):
    return POLA_ANGKA.sub(f" {token} ", teks)


def normalisasi_lokasi(teks, nama_tempat=NAMA_TEMPAT_CONTOH, token="tok_lokasi"):
    """Mengganti alamat dan nama tempat dengan satu token. Masukan harus sudah huruf kecil.

    Pola alamat (jalan, RT/RW, awalan wilayah + satu kata) + daftar nama tempat
    (gazetteer). Nama tempat yang tidak ada di daftar tidak dikenali.
    """
    for nama in sorted(nama_tempat, key=len, reverse=True):
        teks = re.sub(rf"\b(?:(?:kelurahan|kel|desa|kampung)\.?\s+)?{re.escape(nama)}\b", f" {token} ", teks)
    teks = POLA_JALAN.sub(f" {token} ", teks)
    teks = POLA_RT_RW.sub(f" {token} ", teks)
    return POLA_AWALAN_WILAYAH.sub(f" {token} ", teks)


# ---------------------------------------------------------------- kalimat & token
SINGKATAN_TITIK = ("jl.", "jln.", "no.", "dr.", "ir.", "prof.", "hj.", "dll.", "dsb.", "dst.", "tgl.", "kec.", "kab.", "kel.")


def pisah_kalimat(teks):
    """Memecah teks menjadi kalimat dengan aturan sederhana (. ! ? diikuti spasi).

    Titik pada singkatan umum (Jl., No., dr.) dilindungi sementara. Ini bukan
    segmenter yang lengkap: lihat bagian keterbatasan pada pelajaran.
    """
    lindung = teks
    for s in SINGKATAN_TITIK:
        lindung = re.sub(rf"(?i)\b{re.escape(s)}", lambda m: m.group(0).replace(".", "<TITIK>"), lindung)
    potongan = re.split(r"(?<=[.!?])\s+", lindung.strip())
    return [p.replace("<TITIK>", ".") for p in potongan if p]


POLA_TOKEN = re.compile(r"[a-z0-9_]+(?:-[a-z0-9_]+)*")


def tokenisasi(teks):
    """Memecah teks huruf kecil menjadi token kata. Kata ulang berhubung (hati-hati) utuh."""
    return POLA_TOKEN.findall(teks)


# ---------------------------------------------------------------- negasi, stopword, stemming
def tandai_negasi(token, negasi=KATA_NEGASI, jendela=1):
    """Memberi awalan 'neg_' pada `jendela` token setelah kata negasi.

    ['tidak', 'ada', 'korban'] -> ['tidak', 'neg_ada', 'korban'] (jendela=1)
    """
    hasil, sisa = [], 0
    for t in token:
        if t in negasi:
            hasil.append(t)
            sisa = jendela
        elif sisa > 0 and not t.startswith(("tok_", "emo_")):
            hasil.append("neg_" + t)
            sisa -= 1
        else:
            hasil.append(t)
    return hasil


def hapus_stopword(token, stopwords=STOPWORDS_KONSERVATIF):
    return [t for t in token if t not in stopwords]


@lru_cache(maxsize=1)
def stopwords_sastrawi():
    """Daftar stopword bawaan Sastrawi (frozenset). Memuat 'tidak', 'belum', dan 'tolong'."""
    from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

    return frozenset(StopWordRemoverFactory().get_stop_words())


@lru_cache(maxsize=1)
def _stemmer():
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

    return StemmerFactory().create_stemmer()


@lru_cache(maxsize=None)
def stem_kata(kata):
    """Stemming satu kata dengan Sastrawi; hasil di-cache karena stemming lambat."""
    return _stemmer().stem(kata)


def stem_token(token):
    """Stemming daftar token; token khusus (tok_, emo_) dan awalan neg_ diperlakukan hati-hati."""
    hasil = []
    for t in token:
        if t.startswith(("tok_", "emo_")):
            hasil.append(t)
        elif t.startswith("neg_"):
            hasil.append("neg_" + stem_kata(t[4:]))
        else:
            hasil.append(stem_kata(t))
    return hasil


# ---------------------------------------------------------------- pipeline
@dataclass(frozen=True)
class KonfigurasiPraproses:
    """Pilihan langkah preprocessing. Nilai awal = pembersihan dasar tanpa pengurangan fitur."""

    unicode: bool = True
    url: bool = True
    mention: bool = True
    hashtag: str = "kata"  # 'pertahankan' | 'hapus' | 'kata'
    emoji: str = "kata"  # 'pertahankan' | 'hapus' | 'kata'
    huruf_berulang: bool = True
    informal: bool = True
    typo: bool = False
    angka_waktu_lokasi: bool = False
    tanda_seru: bool = False  # tambahkan token tok_seru bila ada '!'
    negasi: bool = False
    stopword: object = False  # False | True / 'konservatif' | 'sastrawi'
    stem: bool = False


def praproses_token(teks, k=KonfigurasiPraproses()):
    """Menjalankan langkah sesuai konfigurasi `k` dan mengembalikan daftar token."""
    if not isinstance(teks, str):
        raise TypeError(f"teks harus str, bukan {type(teks).__name__}")
    ada_seru = "!" in teks
    if k.unicode:
        teks = normalisasi_unicode(teks)
    if k.url:
        teks = ganti_url(teks)
    if k.mention:
        teks = ganti_mention(teks)
    teks = proses_hashtag(teks, k.hashtag)
    teks = proses_emoji(teks, k.emoji)
    teks = case_folding(teks).replace("&", " dan ")
    if k.angka_waktu_lokasi:
        teks = normalisasi_waktu(teks)
        teks = normalisasi_lokasi(teks)
        teks = normalisasi_angka(teks)
    if k.huruf_berulang:
        teks = kurangi_huruf_berulang(teks)
    token = tokenisasi(teks)
    if k.informal:
        token = [normalisasi_informal(t) for t in token]
    if k.typo:
        token = [koreksi_typo(t) for t in token]
    if k.negasi:
        token = tandai_negasi(token)
    if k.stopword == "sastrawi":
        token = hapus_stopword(token, stopwords_sastrawi())
    elif k.stopword:
        token = hapus_stopword(token)
    if k.stem:
        token = stem_token(token)
    if k.tanda_seru and ada_seru:
        token.append("tok_seru")
    return token


def praproses(teks, k=KonfigurasiPraproses()):
    """Seperti praproses_token, tetapi mengembalikan satu string (token digabung spasi)."""
    return " ".join(praproses_token(teks, k))


class PraprosesTeks(BaseEstimator, TransformerMixin):
    """Pembungkus scikit-learn. TANPA state: fit tidak mempelajari apa pun dari data."""

    def __init__(self, konfigurasi=None):
        self.konfigurasi = konfigurasi

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        k = self.konfigurasi or KonfigurasiPraproses()
        return [praproses(t, k) for t in X]
