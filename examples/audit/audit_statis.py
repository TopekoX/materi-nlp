"""Audit statis (Tahap 8): struktur halaman, tabel, tanda $, karakter kontrol, penanda sisa, dan URL eksternal.

Pakai (dari mana saja): python examples/audit/audit_statis.py
Memerlukan jaringan untuk pemeriksaan URL. URL contoh yang sengaja fiktif (contoh.id, t.co/xyz123) akan dilaporkan; itu wajar.
Tanda `@@` pada IMPLEMENTATION_PLAN.md dan audit-verifikasi.md berasal dari teks yang menjelaskan sebuah bug dan diabaikan oleh pembaca laporan.
"""
import concurrent.futures as cf
import glob
import re
import urllib.request
from pathlib import Path

AKAR = Path(__file__).resolve().parents[2]
KECUALI = ("docs/authoring", "docs/examples", "docs/curriculum", "docs/getting-started")
masalah = []


def n_kolom(baris):
    return len(re.sub(r"\\\|", "", baris).strip("|").split("|"))


berkas = [p for p in glob.glob(str(AKAR / "docs/**/*.md"), recursive=True) if not any(k in p.replace("\\", "/") for k in KECUALI)]
for p in berkas:
    t = open(p, encoding="utf-8").read()
    kode = re.sub(r"```.*?```", "", t, flags=re.S)
    nama = Path(p).relative_to(AKAR).as_posix()
    if len(re.findall(r"(?m)^# ", kode)) != 1:
        masalah.append((nama, "jumlah H1 != 1"))
    if kode.count("$") % 2:
        masalah.append((nama, "tanda $ ganjil di luar blok kode"))
    if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", t):
        masalah.append((nama, "karakter kontrol"))
    if re.search(r"(?m)^#{1,6}\s*$", t):
        masalah.append((nama, "heading kosong"))
    if re.search(r"(?m)^#{1,6} .*\$", t):
        masalah.append((nama, "rumus di dalam heading (muncul mentah di daftar isi)"))
    if "@@" in t:
        masalah.append((nama, "penanda @@ tersisa"))
    for kata in ("TODO", "FIXME", "lorem ipsum"):
        if kata in t:
            masalah.append((nama, kata))
    blok, cur = [], []
    for baris in t.split("\n"):
        if baris.lstrip().startswith("|"):
            cur.append(baris.strip())
        elif cur:
            blok.append(cur)
            cur = []
    if cur:
        blok.append(cur)
    for b in blok:
        if len({n_kolom(x) for x in b}) > 1:
            masalah.append((nama, "kolom tabel tidak konsisten: " + b[0][:40]))
print("halaman diperiksa:", len(berkas), "| masalah struktur:", len(masalah))
for m in masalah:
    print("  ", m)

urls = {}
for p in berkas + [str(AKAR / "README.md")] + glob.glob(str(AKAR / "examples/**/*.md"), recursive=True):
    for u in re.findall(r"https?://[^\s<>)\]\"`']+", open(p, encoding="utf-8").read()):
        u = u.rstrip(".,;:")
        host = u.split("/")[2]
        if host.startswith(("localhost", "127.0.0.1")) or "example" in host:
            continue
        urls.setdefault(u, Path(p).name)


def cek(u):
    err = ""
    for metode in ("HEAD", "GET"):
        try:
            r = urllib.request.Request(u, method=metode, headers={"User-Agent": "Mozilla/5.0 ref-check"})
            return u, urllib.request.urlopen(r, timeout=30).status
        except Exception as e:
            err = str(e)[:70]
    return u, err


with cf.ThreadPoolExecutor(8) as ex:
    hasil = list(ex.map(cek, urls))
buruk = [h for h in hasil if h[1] != 200]
print(len(hasil), "URL unik;", len(buruk), "tidak berstatus 200")
for u, s in buruk:
    print("  ", u, s, "<-", urls[u])
