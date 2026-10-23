"""Tahap B: memeriksa skema, duplikat, label bertentangan, privasi, dan kebocoran kelompok pada dataset proyek."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # folder examples/

import pandas as pd

from nlp_hub.data import bagi_latih_uji, muat_dataset, muat_uji_tangan
from nlp_hub.konsol import pakai_utf8
from nlp_hub.validasi_data import periksa_kebocoran_kelompok, periksa_semua

pakai_utf8()

# --8<-- [start:periksa]
for nama, df in (("synthetic_disaster_id.csv (mentah)", muat_dataset(hapus_duplikat=False)),
                 ("handwritten_challenge_id.csv", muat_uji_tangan())):
    print(f"{nama}: {len(df)} baris, kolom {list(df.columns)}")
    for jenis, masalah in periksa_semua(df).items():
        print(f"  {jenis:19}:", masalah if masalah else "lolos")
# --8<-- [end:periksa]

# --8<-- [start:bocor]
latih, uji = bagi_latih_uji(muat_dataset())
print("pembagian per event_id    :", periksa_kebocoran_kelompok(latih, uji) or "tidak ada kebocoran kelompok")
acak = muat_dataset().sample(frac=1, random_state=0)
setengah = len(acak) * 4 // 5
print("pembagian acak per baris  :", periksa_kebocoran_kelompok(acak.iloc[:setengah], acak.iloc[setengah:]))
# --8<-- [end:bocor]

# --8<-- [start:rusak]
rusak = pd.DataFrame({
    "text": ["Tolong, hubungi 081234567890", "banjir", "", "banjir", "kontak budi@contoh-mail.com", "lihat https://situs-asing.org/x"],
    "label": ["Emergency", "Emergency", "Non-Emergency", "Non-Emergency", "Darurat", "Emergency"],
})
for jenis, masalah in periksa_semua(rusak).items():
    print(f"  {jenis:19}:", masalah if masalah else "lolos")
print("tanpa kolom label:", periksa_semua(pd.DataFrame({"text": ["a"]})))
# --8<-- [end:rusak]
