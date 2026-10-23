"""Membuat gambar untuk halaman Level 5 (confusion matrix, kurva PR dan ROC). Hasil ke docs/assets/gambar/."""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import average_precision_score, confusion_matrix, precision_recall_curve, roc_auc_score, roc_curve

from nlp_hub.proyek import model_rujukan, siapkan

warnings.filterwarnings("ignore")
PERMUKAAN, TEKS, TEKS_2 = "#fcfcfb", "#0b0b0b", "#52514e"
BIRU, ORANYE = "#2a78d6", "#eb6834"
TUJUAN = Path(__file__).resolve().parents[2] / "docs" / "assets" / "gambar"


def gaya(ax):
    ax.set_facecolor(PERMUKAAN)
    for sisi in ("top", "right"):
        ax.spines[sisi].set_visible(False)
    for sisi in ("left", "bottom"):
        ax.spines[sisi].set_color("#c3c2b7")
    ax.tick_params(colors=TEKS_2)


def matriks(ax, y, p, judul):
    m = confusion_matrix(y, p, labels=[1, 0])
    ax.imshow(m, cmap="Blues", vmin=0, vmax=m.max() * 1.1)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(m[i, j]), ha="center", va="center", fontsize=16,
                    color="white" if m[i, j] > m.max() * 0.55 else TEKS)
    ax.set_xticks([0, 1], ["ditebak\nEmergency", "ditebak\nNon-Emergency"], color=TEKS_2)
    ax.set_yticks([0, 1], ["sebenarnya\nEmergency", "sebenarnya\nNon-Emergency"], color=TEKS_2)
    ax.set_title(judul, color=TEKS, loc="left", fontsize=11)
    for sisi in ax.spines.values():
        sisi.set_visible(False)


def main():
    TUJUAN.mkdir(parents=True, exist_ok=True)
    d = siapkan()
    model = model_rujukan(d)
    sk_uji, sk_tan = model.decision_function(d.uji["text"]), model.decision_function(d.tangan["text"])

    fig, sumbu = plt.subplots(1, 2, figsize=(8, 3.8), facecolor=PERMUKAAN)
    matriks(sumbu[0], d.y_uji, (sk_uji > 0).astype(int), "Uji sintetis (112 teks)")
    matriks(sumbu[1], d.y_tangan, (sk_tan > 0).astype(int), "Tulis-tangan (48 teks)")
    fig.tight_layout()
    fig.savefig(TUJUAN / "level5-confusion-matrix.png", dpi=150, facecolor=PERMUKAAN)

    fig, sumbu = plt.subplots(1, 2, figsize=(8.4, 3.9), facecolor=PERMUKAAN)
    for ax in sumbu:
        gaya(ax)
        ax.grid(color="#e6e5e0", linewidth=0.8)
        ax.set_axisbelow(True)
    for nama, y, s, warna in [("Uji sintetis", d.y_uji, sk_uji, BIRU), ("Tulis-tangan", d.y_tangan, sk_tan, ORANYE)]:
        p, r, _ = precision_recall_curve(y, s)
        sumbu[0].plot(r, p, color=warna, linewidth=2, label=f"{nama} (AP={average_precision_score(y, s):.2f})")
        fpr, tpr, _ = roc_curve(y, s)
        sumbu[1].plot(fpr, tpr, color=warna, linewidth=2, label=f"{nama} (AUC={roc_auc_score(y, s):.2f})")
    sumbu[1].plot([0, 1], [0, 1], color="#9a998f", linestyle="--", linewidth=1)
    sumbu[0].set_xlabel("Recall Emergency", color=TEKS_2)
    sumbu[0].set_ylabel("Presisi Emergency", color=TEKS_2)
    sumbu[0].set_title("Kurva presisi-recall", color=TEKS, loc="left", fontsize=11)
    sumbu[1].set_xlabel("False positive rate", color=TEKS_2)
    sumbu[1].set_ylabel("Recall Emergency (TPR)", color=TEKS_2)
    sumbu[1].set_title("Kurva ROC", color=TEKS, loc="left", fontsize=11)
    for ax in sumbu:
        ax.set_xlim(0, 1.02)
        ax.set_ylim(0, 1.05)
        ax.legend(frameon=False, labelcolor=TEKS, loc="lower left" if ax is sumbu[0] else "lower right")
    fig.tight_layout()
    fig.savefig(TUJUAN / "level5-pr-roc.png", dpi=150, facecolor=PERMUKAAN)
    print("gambar ditulis ke", TUJUAN)


if __name__ == "__main__":
    main()
