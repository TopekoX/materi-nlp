"""Case folding, URL, mention, hashtag, dan tanda baca (pelajaran Level 2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # agar paket nlp_hub (folder examples/) dapat diimpor

from nlp_hub.konsol import pakai_utf8
from nlp_hub.preprocessing import (
    KonfigurasiPraproses, case_folding, ganti_mention, ganti_url, praproses, proses_hashtag,
)

pakai_utf8()

# --8<-- [start:case_folding]
print(case_folding("TOLONG, Banjir di JL. Melati"))
print("BMKG".lower(), "SAR".lower())
# --8<-- [end:case_folding]

# --8<-- [start:url_mention]
post = "@bpbd_contoh banjir naik, info: https://contoh.example/12345"
print(ganti_url(post))
print(ganti_mention(ganti_url(post)))
# --8<-- [end:url_mention]

# --8<-- [start:hashtag]
tagar = "Air naik #SiagaBencana #banjirkelurahan"
for mode in ["pertahankan", "hapus", "kata"]:
    print(mode, "->", repr(" ".join(proses_hashtag(tagar, mode).split())))
# --8<-- [end:hashtag]

# --8<-- [start:tanda_baca]
a = "Tolong!!! Air naik"
b = "tolong air naik"
print(praproses(a) == praproses(b))
print(praproses(a, KonfigurasiPraproses(tanda_seru=True)))
print(praproses(b, KonfigurasiPraproses(tanda_seru=True)))
# --8<-- [end:tanda_baca]

# --8<-- [start:langkah]
from nlp_hub.preprocessing import (  # noqa: E402  (impor diletakkan di sini agar potongan terbaca mandiri)
    kurangi_huruf_berulang, normalisasi_unicode, proses_emoji, tokenisasi,
)

mentah = "@bpbd_contoh TOLOOONG banjir naik! #SiagaBencana https://contoh.example/1 🙏"
langkah = normalisasi_unicode(mentah)
print("1", langkah)
langkah = ganti_mention(ganti_url(langkah))
print("2", " ".join(langkah.split()))
langkah = proses_hashtag(langkah, "kata")
print("3", " ".join(langkah.split()))
langkah = proses_emoji(langkah, "kata")
print("4", " ".join(langkah.split()))
langkah = case_folding(langkah)
print("5", " ".join(langkah.split()))
langkah = kurangi_huruf_berulang(langkah)
print("6", " ".join(langkah.split()))
print("7", tokenisasi(langkah))
# --8<-- [end:langkah]
