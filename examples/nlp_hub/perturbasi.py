"""Perturbasi teks DETERMINISTIK untuk uji ketahanan (robustness) terhadap variasi bahasa.

Setiap fungsi menerima satu string dan mengembalikan string baru tanpa memakai pengacak, sehingga
hasilnya dapat diulang dan diuji. Perturbasi ini meniru variasi informal; ia bukan pengganti data nyata
yang ditulis oleh orang berbeda.
"""
import re

SINGKATAN_BALIK = {
    "yang": "yg", "tidak": "gak", "sudah": "udh", "dengan": "dgn", "untuk": "utk", "karena": "krn",
    "sekarang": "skrg", "sangat": "bgt", "banget": "bgt", "belum": "blm", "tolong": "tlg",
    "orang": "org", "rumah": "rmh", "jalan": "jln", "warga": "wrg", "kemarin": "kmrn", "juga": "jg",
}
VOKAL = "aiueo"


def huruf_besar(teks):
    return teks.upper()


def singkat(teks):
    """Mengganti kata baku yang ada di kamus dengan singkatan informal (huruf kecil/besar diabaikan)."""
    def ganti(m):
        return SINGKATAN_BALIK.get(m.group(0).lower(), m.group(0))

    return re.sub(r"[A-Za-z]+", ganti, teks)


def perpanjang_huruf(teks, setiap=3):
    """Memanjangkan vokal terakhir pada setiap kata ke-`setiap` yang panjangnya >= 4 (tolong -> toloong)."""
    hasil, n = [], 0
    for kata in teks.split(" "):
        huruf = re.sub(r"[^A-Za-z]", "", kata)
        if len(huruf) >= 4:
            n += 1
            if n % setiap == 0:
                pos = [i for i, c in enumerate(kata) if c.lower() in VOKAL]
                if pos:
                    i = pos[-1]
                    kata = kata[: i + 1] + kata[i] * 2 + kata[i + 1 :]
        hasil.append(kata)
    return " ".join(hasil)


def typo(teks, setiap=4):
    """Menukar dua huruf tengah pada setiap kata ke-`setiap` yang panjangnya >= 5."""
    hasil, n = [], 0
    for kata in teks.split(" "):
        if len(kata) >= 5 and kata.isalpha():
            n += 1
            if n % setiap == 0:
                i = len(kata) // 2
                kata = kata[: i - 1] + kata[i] + kata[i - 1] + kata[i + 1 :]
        hasil.append(kata)
    return " ".join(hasil)


def tambah_derau(teks):
    """Menambahkan emoji, hashtag, dan URL di akhir (seperti pada postingan nyata)."""
    return f"{teks} 🙏 #SiagaBencana https://contoh.example/0"


def tanpa_tanda_baca(teks):
    return re.sub(r"[^\w\s]", "", teks)


PERTURBASI = {
    "huruf besar semua": huruf_besar,
    "singkatan informal": singkat,
    "huruf diperpanjang": perpanjang_huruf,
    "typo (tukar huruf)": typo,
    "emoji+hashtag+URL": tambah_derau,
    "tanpa tanda baca": tanpa_tanda_baca,
}
