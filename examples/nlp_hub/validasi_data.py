"""Pemeriksaan skema dan kebersihan dataset proyek (Tahap B).

Fungsi mengembalikan DAFTAR MASALAH (teks); daftar kosong berarti lolos. Pemeriksaan privasi bersifat heuristik:
ia dapat melewatkan data pribadi dan dapat salah menandai; hasil lolos BUKAN jaminan bahwa data aman.
"""
import re

LABEL_SAH = {"Emergency", "Non-Emergency"}
POLA_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
POLA_TELEPON = re.compile(r"(?<!\d)(?:\+62|62|0)8\d{8,11}(?!\d)")
POLA_URL = re.compile(r"https?://[^\s]+")
POLA_MENTION = re.compile(r"(?<![\w.])@\w+")  # lookbehind: bagian setelah @ pada alamat email bukan mention
DOMAIN_AMAN = ("contoh.example",)
AKHIRAN_MENTION_AMAN = "_contoh"


def periksa_skema(df, kolom_wajib=("text", "label")):
    """Kolom wajib ada, teks tidak kosong, label hanya Emergency/Non-Emergency, tidak ada nilai hilang."""
    masalah = []
    hilang = [k for k in kolom_wajib if k not in df.columns]
    if hilang:
        return [f"kolom wajib tidak ada: {hilang}"]
    for k in kolom_wajib:
        n = int(df[k].isna().sum())
        if n:
            masalah.append(f"kolom {k!r} punya {n} nilai hilang")
    teks = df["text"].dropna().astype(str)
    kosong = int((teks.str.strip() == "").sum())
    if kosong:
        masalah.append(f"{kosong} teks kosong atau hanya spasi")
    tak_dikenal = sorted(set(df["label"].dropna()) - LABEL_SAH)
    if tak_dikenal:
        masalah.append(f"label tidak dikenal: {tak_dikenal}")
    return masalah


def periksa_duplikat(df):
    """Jumlah teks duplikat persis (setelah dipangkas). Duplikat bukan selalu salah (mis. retweet) tetapi harus diketahui."""
    n = int(df["text"].astype(str).str.strip().duplicated().sum())
    return [f"{n} baris adalah duplikat persis dari baris sebelumnya"] if n else []


def periksa_label_bertentangan(df):
    """Teks yang sama dengan label berbeda: tanda pelabelan tidak konsisten."""
    g = df.assign(t=df["text"].astype(str).str.strip()).groupby("t")["label"].nunique()
    n = int((g > 1).sum())
    return [f"{n} teks identik punya label berbeda"] if n else []


def periksa_privasi(df):
    """Heuristik: email, nomor telepon seluler Indonesia, URL di luar domain contoh, dan @mention bukan akun contoh."""
    masalah, teks = [], df["text"].astype(str)
    email = teks.apply(lambda t: bool(POLA_EMAIL.search(t))).sum()
    tel = teks.apply(lambda t: bool(POLA_TELEPON.search(t))).sum()
    url_asing = teks.apply(lambda t: any(not any(d in u for d in DOMAIN_AMAN) for u in POLA_URL.findall(t))).sum()
    mention_asing = teks.apply(lambda t: any(not m.endswith(AKHIRAN_MENTION_AMAN) for m in POLA_MENTION.findall(t))).sum()
    for jumlah, nama in ((email, "alamat email"), (tel, "nomor telepon"), (url_asing, "URL di luar contoh.example"),
                         (mention_asing, "@mention yang bukan akun contoh")):
        if jumlah:
            masalah.append(f"{int(jumlah)} teks tampak memuat {nama}")
    return masalah


def periksa_kebocoran_kelompok(latih, uji, kolom="event_id"):
    """Kelompok (mis. kejadian) yang muncul di latih dan uji sekaligus: kebocoran antarpostingan."""
    irisan = set(latih[kolom]) & set(uji[kolom])
    return [f"{len(irisan)} {kolom} muncul di latih dan uji"] if irisan else []


def periksa_semua(df):
    """Gabungan skema, duplikat, label bertentangan, dan privasi. Mengembalikan dict nama -> daftar masalah."""
    skema = periksa_skema(df)
    if skema and any("kolom wajib" in m for m in skema):
        return {"skema": skema}
    return {"skema": skema, "duplikat": periksa_duplikat(df), "label_bertentangan": periksa_label_bertentangan(df),
            "privasi": periksa_privasi(df)}
