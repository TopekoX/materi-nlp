"""Emoji dan emotikon (pelajaran Level 2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

from nlp_hub.data import muat_dataset
from nlp_hub.konsol import pakai_utf8
from nlp_hub.preprocessing import POLA_EMOJI, praproses, proses_emoji

pakai_utf8()

# --8<-- [start:deteksi]
post = "Tolong 🙏 air naik 😭😭 :( T_T"
print(POLA_EMOJI.findall(post))
print(len(POLA_EMOJI.findall(post)))
# --8<-- [end:deteksi]

# --8<-- [start:mode]
for mode in ["pertahankan", "hapus", "kata"]:
    print(mode, "->", repr(" ".join(proses_emoji(post, mode).split())))
# --8<-- [end:mode]

# --8<-- [start:tak_dikenal]
print(" ".join(proses_emoji("aman 🦖 👍🏽", "kata").split()))
print(len("👍🏽"), [hex(ord(c)) for c in "👍🏽"])
print(praproses("hati ❤️ untuk korban"))
# --8<-- [end:tak_dikenal]

# --8<-- [start:ambigu]
for teks in ["Rumah kami terendam 😭 tolong", "Dompetku kebanjiran 😭 wkwk"]:
    print(praproses(teks))
# --8<-- [end:ambigu]

# --8<-- [start:statistik]
df = muat_dataset()
df["ada_emoji"] = df["text"].apply(lambda t: bool(POLA_EMOJI.search(t)))
print(df.groupby("label")["ada_emoji"].agg(["sum", "count", "mean"]).round(3))
# --8<-- [end:statistik]
