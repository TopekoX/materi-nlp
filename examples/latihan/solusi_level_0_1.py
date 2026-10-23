"""Kunci jawaban kode untuk Latihan Level 0-1 (Python dasar dan masalah Emergency)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # folder examples/

import pandas as pd

from nlp_hub.data import FOLDER_DATA
from nlp_hub.konsol import pakai_utf8


# --8<-- [start:hitung_kata]
def hitung_kata(teks):
    """Menghitung frekuensi tiap kata (huruf kecil, tanda baca di tepi dibuang). Mengembalikan dict."""
    hasil = {}
    for kata in teks.lower().split():
        kata = kata.strip(".,!?;:")
        if kata:                                   # lewati token yang hanya berisi tanda baca
            hasil[kata] = hasil.get(kata, 0) + 1   # .get memberi 0 bila kata belum ada, sehingga tidak KeyError
    return hasil
# --8<-- [end:hitung_kata]


# --8<-- [start:ekstrak]
POLA_HASHTAG = re.compile(r"#(\w+)")
POLA_MENTION = re.compile(r"(?<![\w.])@(\w+)")


def ekstrak_penanda(teks):
    """Mengembalikan (daftar hashtag, daftar mention) tanpa tanda # dan @."""
    return POLA_HASHTAG.findall(teks), POLA_MENTION.findall(teks)
# --8<-- [end:ekstrak]


# --8<-- [start:kata_kunci]
KATA_KUNCI = {"tolong", "banjir", "gempa", "kebakaran", "longsor", "evakuasi", "bantuan"}


def prediksi_kata_kunci(teks):
    """Baseline naif: Emergency bila ada kata kunci bencana di dalam teks."""
    kata = {k.strip(".,!?;:").lower() for k in teks.split()}
    return "Emergency" if kata & KATA_KUNCI else "Non-Emergency"
# --8<-- [end:kata_kunci]


if __name__ == "__main__":
    pakai_utf8()
    # --8<-- [start:jalan_hitung]
    print(hitung_kata("Tolong, air masuk rumah! Tolong kirim bantuan."))
    print(ekstrak_penanda("Banjir di Jl. Melati #SiagaBencana #banjir cc @posko_contoh, bukan a@b.com"))
    # --8<-- [end:jalan_hitung]
    # --8<-- [start:jalan_kunci]
    tangan = pd.read_csv(FOLDER_DATA / "handwritten_challenge_id.csv")
    tangan["pred"] = tangan["text"].apply(prediksi_kata_kunci)
    print("distribusi label:", tangan["label"].value_counts().to_dict())
    print("akurasi kata kunci:", round(float((tangan["pred"] == tangan["label"]).mean()), 3))
    salah = tangan[(tangan["pred"] == "Emergency") & (tangan["label"] == "Non-Emergency")]
    luput = tangan[(tangan["pred"] == "Non-Emergency") & (tangan["label"] == "Emergency")]
    print("alarm palsu:", len(salah), "| darurat terlewat:", len(luput))
    for _, r in salah.head(2).iterrows():
        print("  FP:", r["text"][:75])
    for _, r in luput.head(2).iterrows():
        print("  FN:", r["text"][:75])
    # --8<-- [end:jalan_kunci]
