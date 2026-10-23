"""Memuat dataset sintetis dan membaginya tanpa kebocoran antarkejadian."""
from pathlib import Path

import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

FOLDER_DATA = Path(__file__).resolve().parents[1] / "disaster-classification" / "data"
RANDOM_STATE = 42
LABEL_POSITIF = "Emergency"  # kelas yang kita pedulikan; dikodekan 1
LABEL_NEGATIF = "Non-Emergency"  # dikodekan 0


def muat_dataset(hapus_duplikat=True):
    """Membaca dataset sintetis. Duplikat persis dibuang bila `hapus_duplikat` True."""
    df = pd.read_csv(FOLDER_DATA / "synthetic_disaster_id.csv")
    if hapus_duplikat:
        df = df.drop_duplicates(subset="text", keep="first").reset_index(drop=True)
    return df


def muat_uji_tangan():
    """Membaca set uji tulis-tangan (48 teks sintetis)."""
    return pd.read_csv(FOLDER_DATA / "handwritten_challenge_id.csv")


def kodekan_label(label):
    """Mengubah deret label teks menjadi 0/1 (Emergency = 1)."""
    pemetaan = {LABEL_NEGATIF: 0, LABEL_POSITIF: 1}
    hasil = label.map(pemetaan)
    if hasil.isna().any():
        raise ValueError(f"Label tidak dikenal: {sorted(set(label[hasil.isna()]))}")
    return hasil.astype(int)


def bagi_latih_uji(df, jumlah_lipatan=5, seed=RANDOM_STATE):
    """Membagi df menjadi latih dan uji berdasarkan `event_id` (satu kejadian tidak terpecah).

    Mengembalikan (df_latih, df_uji). Uji ~ 1/jumlah_lipatan data dan kelas dijaga proporsinya
    semampu mungkin. Tidak ada `event_id` yang muncul di kedua bagian.
    """
    pembagi = StratifiedGroupKFold(n_splits=jumlah_lipatan, shuffle=True, random_state=seed)
    y = kodekan_label(df["label"])
    idx_latih, idx_uji = next(pembagi.split(df, y, groups=df["event_id"]))
    return df.iloc[idx_latih].reset_index(drop=True), df.iloc[idx_uji].reset_index(drop=True)


def bagi_latih_val_uji(df, seed=RANDOM_STATE):
    """Membagi df menjadi latih (~60%), validasi (~20%), dan uji (~20%) berdasarkan `event_id`.

    Uji dipisahkan dahulu, lalu sisanya dibagi lagi menjadi latih dan validasi. Tidak ada
    `event_id` yang muncul di lebih dari satu bagian. Mengembalikan (latih, val, uji).
    """
    sisa, uji = bagi_latih_uji(df, jumlah_lipatan=5, seed=seed)
    latih, val = bagi_latih_uji(sisa, jumlah_lipatan=4, seed=seed)
    return latih, val, uji
