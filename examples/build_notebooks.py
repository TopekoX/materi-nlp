"""Membangun dan MENJALANKAN notebook pelajaran, sehingga keluaran di dalamnya asli.

Notebook dihasilkan dari daftar sel di berkas ini (sumber kebenaran), lalu
dieksekusi dengan nbclient. Menjalankan:

    python build_notebooks.py            # semua notebook
    python build_notebooks.py 2 4        # hanya notebook level 2 dan 4

Syarat: pip install -r requirements-ml.txt
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

RAIS = Path(__file__).resolve().parent

PEMBUKA = '''\
import sys
import warnings
from pathlib import Path

# Notebook ini berada di examples/<folder-level>/. Paket nlp_hub ada di examples/.
sys.path.insert(0, str(Path.cwd().parent))
warnings.filterwarnings("ignore", message="'count' is passed as positional argument")
'''


def md(teks):
    return new_markdown_cell(teks.strip("\n"))


def kode(teks):
    return new_code_cell(teks.strip("\n"))


def simpan(path, sel):
    nb = new_notebook(cells=sel)
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python"}
    NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}}).execute()
    for sel_ in nb.cells:  # buang metadata eksekusi yang berubah-ubah (waktu), agar diff stabil
        sel_.metadata.pop("execution", None)
    nbformat.write(nb, path)
    print("ditulis:", path.relative_to(RAIS))


# ------------------------------------------------------------------ Level 2
def level_2():
    return RAIS / "level-2-preprocessing" / "02_preprocessing_pipeline.ipynb", [
        md("""
# Level 2 — Preprocessing teks Indonesia untuk klasifikasi Emergency / Non-Emergency

> **Data sintetis.** Seluruh teks di notebook ini dibangkitkan dari templat atau ditulis tangan
> (lihat `../disaster-classification/DATA_CARD.md`). Angka di sini hanya menunjukkan bahwa kodenya
> bekerja, bukan performa pada data nyata.

**Cara menjalankan:** jalankan sel dari atas ke bawah. Prasyarat: `pip install -r requirements-ml.txt`
dari folder utama repository. Notebook ini membaca data lewat jalur relatif dan tidak mengunduh apa pun.
"""),
        kode(PEMBUKA),
        md("## 1. Memuat dataset sintetis\n`muat_dataset()` membaca CSV dan membuang duplikat persis."),
        kode("""
from nlp_hub.data import muat_dataset

df = muat_dataset()
print(df.shape)
df[["event_id", "post_type", "label", "text"]].head(5)
"""),
        md("""
## 2. Menelusuri satu postingan langkah demi langkah
Setiap langkah mengambil hasil langkah sebelumnya. Urutan penting: hashtag diproses sebelum huruf
menjadi kecil, dan emoji sebelum tokenisasi.
"""),
        kode("""
from nlp_hub.preprocessing import (
    ganti_mention, ganti_url, kurangi_huruf_berulang, normalisasi_unicode, proses_emoji,
    proses_hashtag, case_folding, tokenisasi,
)

teks = "@bpbd_contoh TOLOOONG banjir naik! #SiagaBencana https://contoh.example/1 🙏"
langkah = normalisasi_unicode(teks); print("1 unicode  :", langkah)
langkah = ganti_mention(ganti_url(langkah)); print("2 url/@    :", " ".join(langkah.split()))
langkah = proses_hashtag(langkah, "kata"); print("3 hashtag  :", " ".join(langkah.split()))
langkah = proses_emoji(langkah, "kata"); print("4 emoji    :", " ".join(langkah.split()))
langkah = case_folding(langkah); print("5 huruf kcl:", " ".join(langkah.split()))
langkah = kurangi_huruf_berulang(langkah); print("6 berulang :", " ".join(langkah.split()))
print("7 token    :", tokenisasi(langkah))
"""),
        md("""
## 3. Fungsi gabungan dan konfigurasi
`praproses_token` menjalankan langkah yang sama; pilihan diatur lewat `KonfigurasiPraproses`.
Hasilnya harus sama dengan langkah manual di atas.
"""),
        kode("""
from nlp_hub.preprocessing import KonfigurasiPraproses, praproses, praproses_token

print(praproses_token(teks))
lengkap = KonfigurasiPraproses(angka_waktu_lokasi=True, negasi=True, stopword=True, stem=True)
print(praproses("Tidak ada listrik di Jl. Melati RT 08 pukul 08.12, tolong!", lengkap))
"""),
        md("""
## 4. Efek pada ukuran kosakata
Normalisasi, stemming, dan penggantian lokasi menyatukan beberapa bentuk. Kita ukur jumlah *tipe* (kata unik).
Pengurangan kosakata **bukan** bukti bahwa model menjadi lebih baik; itu harus diuji (lihat halaman *Perbandingan Pipeline*).
"""),
        kode("""
import pandas as pd

konfigurasi = {
    "tanpa normalisasi": KonfigurasiPraproses(informal=False, huruf_berulang=False),
    "dasar": KonfigurasiPraproses(),
    "+ angka/waktu/lokasi": KonfigurasiPraproses(angka_waktu_lokasi=True),
    "+ stopword konservatif": KonfigurasiPraproses(stopword="konservatif"),
    "+ stemming": KonfigurasiPraproses(stem=True),
}
baris = []
for nama, k in konfigurasi.items():
    token = [t for x in df["text"] for t in praproses_token(x, k)]
    baris.append({"konfigurasi": nama, "token": len(token), "tipe": len(set(token))})
pd.DataFrame(baris)
"""),
        md("""
## 5. Audit: apakah ada teks yang menjadi kosong?
Stopword bawaan Sastrawi membuang kata seperti `tidak`, `belum`, dan `tolong`. Periksa kata yang terbuang dari satu contoh.
"""),
        kode("""
from nlp_hub.preprocessing import stopwords_sastrawi

contoh = "Tolong, air belum surut dan listrik tidak ada"
terbuang = [t for t in praproses_token(contoh) if t in stopwords_sastrawi()]
print("kata yang dibuang Sastrawi:", terbuang)
kosong = sum(1 for x in df["text"] if not praproses(x, KonfigurasiPraproses(stopword="sastrawi")).strip())
print("teks yang menjadi kosong:", kosong)
"""),
        md("""
## Latihan
1. Tambahkan konfigurasi baru ke sel 4 (mis. `negasi=True`) dan bandingkan jumlah tipe.
2. Ubah `contoh` pada sel 5 menjadi pasangan kalimat berlawanan (`Ada korban` / `Tidak ada korban`) dan bandingkan hasil dengan stopword Sastrawi dan konservatif.
3. Baca halaman *Perbandingan Pipeline* lalu jalankan `10_perbandingan_pipeline.py`. Apakah kesimpulannya berubah jika Anda mengganti seed?

**Keterbatasan:** dataset sintetis dan kecil; tidak ada kesimpulan tentang data Twitter/X nyata.
"""),
    ]


# ------------------------------------------------------------------ Level 3
def level_3():
    return RAIS / "level-3-feature-engineering" / "03_eda_dan_fitur.ipynb", [
        md("""
# Level 3 — EDA dan representasi teks (Tahap C proyek)

> **Data sintetis.** Dataset dibangkitkan dari templat; set tulis-tangan ditulis penulis materi
> (lihat `../disaster-classification/DATA_CARD.md`). Temuan di sini **tidak** mewakili data Twitter/X nyata.

Prasyarat: `pip install -r requirements-ml.txt`. Jalankan sel dari atas ke bawah.
"""),
        kode(PEMBUKA),
        md("## 1. Struktur, nilai kosong, duplikat, label"),
        kode("""
from nlp_hub.data import muat_dataset

mentah = muat_dataset(hapus_duplikat=False)
print(mentah.shape)
print("nilai kosong:", int(mentah.isna().sum().sum()), "| duplikat teks:", int(mentah["text"].duplicated().sum()))
print(mentah["label"].value_counts(normalize=True).round(3).to_dict())
df = muat_dataset()  # duplikat persis dibuang
print("setelah dedup:", df.shape)
"""),
        md("## 2. Panjang teks per kelas\nPerbedaan panjang berasal dari templat (laporan memuat alamat); jangan digeneralisasi."),
        kode("""
df["n_karakter"] = df["text"].str.len()
df.groupby("label")["n_karakter"].describe().round(1)
"""),
        md("## 3. Kata paling sering (document frequency) per kelas"),
        kode("""
from collections import Counter
from nlp_hub.preprocessing import praproses_token

token = [set(praproses_token(t)) for t in df["text"]]
for label in ["Emergency", "Non-Emergency"]:
    c = Counter(k for s, l in zip(token, df["label"]) if l == label for k in s)
    print(label, c.most_common(8))
"""),
        md("""
## 4. Bag of Words dan TF-IDF
Vektorizer **hanya** dilatih pada data latih (`fit`), lalu dipakai pada data uji (`transform`).
Pembagian dilakukan per `event_id` agar satu kejadian tidak terpecah.
"""),
        kode("""
from sklearn.feature_extraction.text import TfidfVectorizer
from nlp_hub.data import bagi_latih_uji
from nlp_hub.preprocessing import PraprosesTeks

latih, uji = bagi_latih_uji(df)
v = TfidfVectorizer(min_df=2)
X_latih = v.fit_transform(PraprosesTeks().transform(latih["text"]))
X_uji = v.transform(PraprosesTeks().transform(uji["text"]))
print("latih:", X_latih.shape, "uji:", X_uji.shape, f"kepadatan latih = {X_latih.nnz / (X_latih.shape[0] * X_latih.shape[1]):.2%}")
print("kejadian di kedua split:", len(set(latih["event_id"]) & set(uji["event_id"])))
"""),
        md("""
## 5. Pemeriksaan kebocoran
Pembagian per kejadian tidak mencegah kemiripan antar-templat. Periksa berapa templat uji yang juga ada di latih.
"""),
        kode("""
print("templat uji:", uji["template_id"].nunique(), "| ada juga di latih:", len(set(uji["template_id"]) & set(latih["template_id"])))
import pandas as pd
pd.crosstab(df["post_type"], df["label"])
"""),
        md("""
**Catatan keputusan (contoh):** (1) buang duplikat persis; (2) pembagian per `event_id`; (3) jangan pakai `post_type`
atau `template_id` sebagai fitur (diturunkan dari label/pembangkit data); (4) laporkan recall Emergency, bukan hanya akurasi.

## Latihan
Ulangi sel 3 pada `muat_uji_tangan()` dengan ambang DF yang lebih kecil. Mengapa katanya berbeda dari data sintetis?
"""),
    ]


# ------------------------------------------------------------------ Level 4
def level_4():
    return RAIS / "level-4-classification" / "04_baseline_klasifikasi.ipynb", [
        md("""
# Level 4 — Baseline klasifikasi Emergency / Non-Emergency (Tahap E proyek)

> **Data sintetis.** Skor di notebook ini tidak membuktikan kelayakan model untuk tanggap darurat nyata
> (lihat `../disaster-classification/DATA_CARD.md`).

Tiga baseline (TF-IDF + Multinomial NB / Logistic Regression / Linear SVM) dibandingkan dengan **data,
pembagian per kejadian, seed, dan metrik yang sama**. Prasyarat: `pip install -r requirements-ml.txt`.
"""),
        kode(PEMBUKA),
        md("## 1. Data dan pembagian per kejadian\nDuplikat persis dibuang. Tidak ada `event_id` yang muncul di lebih dari satu bagian."),
        kode("""
import pandas as pd
from nlp_hub.data import bagi_latih_val_uji, kodekan_label, muat_dataset, muat_uji_tangan

df = muat_dataset()
latih, val, uji = bagi_latih_val_uji(df)
dev = pd.concat([latih, val], ignore_index=True)   # data pengembangan
tangan = muat_uji_tangan()
print(len(latih), len(val), len(uji), "| tulis-tangan:", len(tangan))
print("kejadian tumpang tindih:", len(set(latih.event_id) & set(uji.event_id)))
"""),
        md("## 2. Tiga baseline dengan pipeline\n`buat_pipeline` merangkai preprocessing → TF-IDF → model. `fit` hanya melihat data latih."),
        kode("""
from nlp_hub.modeling import buat_pipeline

y_dev = kodekan_label(dev["label"])
model = {n: buat_pipeline(k).fit(dev["text"], y_dev) for n, k in [("Naive Bayes", "nb"), ("Logistic Regression", "lr"), ("Linear SVM", "svm")]}
list(model)
"""),
        md("## 3. Evaluasi: validasi silang berkelompok + uji sekali\nF1 makro dan recall kelas Emergency; Emergency = 1 (kelas positif)."),
        kode("""
import numpy as np
from sklearn.model_selection import StratifiedGroupKFold
from nlp_hub.eksperimen import metrik_emergency

X, y = dev["text"].to_numpy(), y_dev.to_numpy()
baris = {}
for nama, kode_algo in [("Naive Bayes", "nb"), ("Logistic Regression", "lr"), ("Linear SVM", "svm")]:
    hasil = []
    for i_latih, i_uji in StratifiedGroupKFold(5, shuffle=True, random_state=42).split(X, y, groups=dev["event_id"]):
        m = buat_pipeline(kode_algo).fit(X[i_latih], y[i_latih])
        hasil.append(metrik_emergency(y[i_uji], m.predict(X[i_uji])))
    baris[nama] = {"F1 makro CV": round(np.mean([h["f1_makro"] for h in hasil]), 3), "Recall E CV": round(np.mean([h["recall_e"] for h in hasil]), 3)}
pd.DataFrame(baris).T
"""),
        kode("""
y_uji, y_tan = kodekan_label(uji["label"]), kodekan_label(tangan["label"])
tab = {}
for nama, m in model.items():
    a, b = metrik_emergency(y_uji, m.predict(uji["text"])), metrik_emergency(y_tan, m.predict(tangan["text"]))
    tab[nama] = {"F1 makro uji": round(a["f1_makro"], 3), "Recall E uji": round(a["recall_e"], 3),
                 "F1 makro tangan": round(b["f1_makro"], 3), "Recall E tangan": round(b["recall_e"], 3)}
pd.DataFrame(tab).T
"""),
        md("""
**Membaca hasil:** bandingkan kolom uji sintetis dengan tulis-tangan. Selisih besar menunjukkan model
mengenali gaya templat, bukan memahami bahasa. Peringkat dapat berbeda antar-kolom; jangan menyebut satu model terbaik.
"""),
        md("## 4. Memprediksi teks baru dengan model Logistic Regression"),
        kode("""
baru = ["Tolong, air sudah masuk rumah kami di Jl. Melati RT 04, ada lansia yang tidak bisa jalan",
        "Musim hujan sudah dekat, waspada banjir ya semuanya"]
for t, p in zip(baru, model["Logistic Regression"].predict_proba(baru)[:, 1]):
    print(f"P(Emergency)={p:.3f} | {t[:60]}")
"""),
        md("""
Probabilitas ini belum terkalibrasi dan ambang 0,5 hanya bawaan. Keputusan operasional memerlukan evaluasi
(Level 5) dan peninjauan manusia.

## Latihan
1. Tambahkan `buat_pipeline("lr", C=10)` ke sel 3 dan bandingkan recall Emergency tulis-tangan. Apakah selisihnya lebih besar daripada satu teks (0,042)?
2. Cetak confusion matrix untuk SVM pada uji sintetis dan pada tulis-tangan (Level 5).
"""),
    ]


# ------------------------------------------------------------------ Level 5
def level_5():
    return RAIS / "level-5-evaluation" / "05_evaluasi_dan_error_analysis.ipynb", [
        md("""
# Level 5 — Evaluasi, error analysis, dan ketidakpastian (Tahap F proyek)

> **Data sintetis.** Skor tidak membuktikan kelayakan model untuk tanggap darurat nyata
> (lihat `../disaster-classification/DATA_CARD.md`). Tidak ada ambang produksi yang ditetapkan di sini.

Model rujukan: Linear SVM (dipilih dari F1 makro validasi silang Level 4, **bukan** dari set tulis-tangan).
Prasyarat: `pip install -r requirements-ml.txt`.
"""),
        kode(PEMBUKA),
        md("## 1. Data, model rujukan, dan prediksi"),
        kode("""
import numpy as np
import pandas as pd
from nlp_hub.proyek import model_rujukan, siapkan

d = siapkan()
model = model_rujukan(d)
skor = {"uji sintetis": model.decision_function(d.uji["text"]), "tulis-tangan": model.decision_function(d.tangan["text"])}
y = {"uji sintetis": d.y_uji, "tulis-tangan": d.y_tangan}
print({k: len(v) for k, v in y.items()})
"""),
        md("## 2. Confusion matrix dan metrik per kelas\nEmergency = 1 (kelas positif). Pada tulis-tangan, perhatikan **FN** (pesan darurat terlewat)."),
        kode("""
from sklearn.metrics import classification_report, confusion_matrix

for nama in skor:
    p = (skor[nama] > 0).astype(int)
    print(nama)
    print(pd.DataFrame(confusion_matrix(y[nama], p, labels=[1, 0]), index=["sebenarnya E", "sebenarnya N"], columns=["ditebak E", "ditebak N"]))
    print(classification_report(y[nama], p, target_names=["Non-Emergency", "Emergency"], digits=3))
"""),
        md("## 3. Ambang: menjelajahi trade-off (bukan memilih)\nTabel ini memakai tulis-tangan untuk **memahami** model. Memilih ambang dari tabel ini lalu melaporkan skornya adalah data snooping."),
        kode("""
from nlp_hub.eksperimen import metrik_emergency

baris = []
for t in [-0.6, -0.4, -0.2, 0.0, 0.2]:
    m = metrik_emergency(y["tulis-tangan"], (skor["tulis-tangan"] >= t).astype(int))
    baris.append({"ambang": t, "presisi E": round(m["presisi_e"], 3), "recall E": round(m["recall_e"], 3), "F1 E": round(m["f1_e"], 3)})
pd.DataFrame(baris)
"""),
        md("## 4. Ketidakpastian: selang bootstrap 95% untuk recall Emergency"),
        kode("""
from nlp_hub.eksperimen import bootstrap_metrik, selang_persentil

for nama in skor:
    p = (skor[nama] > 0).astype(int)
    lo, hi = selang_persentil(bootstrap_metrik(y[nama], p, "recall_e"))
    print(f"{nama:14} recall E = {metrik_emergency(y[nama], p)['recall_e']:.3f}  selang 95% [{lo:.3f}, {hi:.3f}]")
"""),
        md("## 5. Error analysis: false negative pada tulis-tangan, diurutkan menurut skor"),
        kode("""
p = (skor["tulis-tangan"] > 0).astype(int)
fn = np.where((d.y_tangan == 1) & (p == 0))[0]
for i in fn[np.argsort(-skor["tulis-tangan"][fn])]:
    print(f"skor={skor['tulis-tangan'][i]:+.2f} | {d.tangan['text'].iloc[i][:80]}")
"""),
        md("""
**Membaca hasil:** sebagian besar FN berskor dekat 0, tetapi ambang yang dipilih dari data bertemplat tidak berpindah ke
data bergaya lain (lihat halaman *Threshold*). Tuliskan temuan Anda dengan tingkat keyakinan, dan jangan menyimpulkan
kelayakan operasional dari data sintetis.

## Latihan
1. Ganti model rujukan dengan `model_rujukan(d, "nb")` dan ulangi sel 2 dan 4. Apakah selang recall tulis-tangan tumpang tindih dengan SVM?
2. Tambahkan perturbasi dari `nlp_hub.perturbasi.PERTURBASI` dan ukur perubahan recall.
"""),
    ]


DAFTAR = {2: level_2, 3: level_3, 4: level_4, 5: level_5}

if __name__ == "__main__":
    pilihan = [int(a) for a in sys.argv[1:]] or sorted(DAFTAR)
    for level in pilihan:
        path, sel = DAFTAR[level]()
        simpan(path, sel)
