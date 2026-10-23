"""Membuat gambar untuk halaman Level 3. Hasil ke docs/assets/gambar/.

Warna: pasangan oranye/biru yang lolos validate_palette (ΔE CVD 24,7).
Gambar memakai latar terang tetap agar terbaca pada tema terang maupun gelap.
"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from nlp_hub.data import muat_dataset
from nlp_hub.preprocessing import praproses_token

warnings.filterwarnings("ignore", message="'count' is passed as positional argument")

PERMUKAAN, TEKS, TEKS_2 = "#fcfcfb", "#0b0b0b", "#52514e"
WARNA = {"Emergency": "#eb6834", "Non-Emergency": "#2a78d6"}
TUJUAN = Path(__file__).resolve().parents[2] / "docs" / "assets" / "gambar"


def gaya(ax):
    ax.set_facecolor(PERMUKAAN)
    for sisi in ("top", "right"):
        ax.spines[sisi].set_visible(False)
    for sisi in ("left", "bottom"):
        ax.spines[sisi].set_color("#c3c2b7")
    ax.tick_params(colors=TEKS_2)
    ax.grid(axis="y", color="#e6e5e0", linewidth=0.8)
    ax.set_axisbelow(True)


def panjang(df):
    fig, sumbu = plt.subplots(2, 1, figsize=(7, 4.6), facecolor=PERMUKAAN, sharex=True, sharey=True)
    tepi = range(30, 161, 10)
    for ax, (label, warna) in zip(sumbu, WARNA.items()):
        gaya(ax)
        ax.hist(df.loc[df["label"] == label, "text"].str.len(), bins=tepi, color=warna, edgecolor=PERMUKAAN, linewidth=1.5)
        ax.set_title(label, color=TEKS, loc="left", fontsize=11)
        ax.set_ylabel("Jumlah teks", color=TEKS_2)
    sumbu[1].set_xlabel("Panjang teks (karakter)", color=TEKS_2)
    fig.tight_layout()
    fig.savefig(TUJUAN / "level3-panjang-teks.png", dpi=150, facecolor=PERMUKAAN)


def kata(df):
    fig, sumbu = plt.subplots(1, 2, figsize=(8, 3.8), facecolor=PERMUKAAN, sharex=True)
    token = [praproses_token(t) for t in df["text"]]
    for ax, (label, warna) in zip(sumbu, WARNA.items()):
        gaya(ax)
        ax.grid(axis="x", color="#e6e5e0", linewidth=0.8)
        ax.grid(axis="y", visible=False)
        c = Counter(k for d, l in zip(token, df["label"]) if l == label for k in set(d))
        atas = c.most_common(8)[::-1]
        ax.barh([k for k, _ in atas], [n / (df["label"] == label).sum() for _, n in atas], color=warna, height=0.65)
        ax.set_title(label, color=TEKS, loc="left", fontsize=11)
        ax.set_xlabel("Proporsi teks yang memuat kata", color=TEKS_2)
        ax.set_xlim(0, 1)
    fig.tight_layout()
    fig.savefig(TUJUAN / "level3-kata-per-kelas.png", dpi=150, facecolor=PERMUKAAN)


if __name__ == "__main__":
    TUJUAN.mkdir(parents=True, exist_ok=True)
    data = muat_dataset()
    panjang(data)
    kata(data)
    print("gambar ditulis ke", TUJUAN)
