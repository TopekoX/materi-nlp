"""Menjalankan 12_finetune_indobert.py atau 10_lstm_pytorch.py untuk beberapa seed dan merangkum hasilnya (EKSPERIMEN BERAT).

Contoh (dari folder examples/):
    python level-6-deep-learning/berat/13_ulang_seed.py --seeds 1 2 3 4 5                      # IndoBERT p1
    python level-6-deep-learning/berat/13_ulang_seed.py --model indolem/indobert-base-uncased  # model lain
    python level-6-deep-learning/berat/13_ulang_seed.py --jenis lstm --seeds 1 2 3 4 5         # LSTM
    python level-6-deep-learning/berat/13_ulang_seed.py --hanya-ringkas                        # susun ulang tabel dari JSON tersimpan

Tiap seed IndoBERT menulis laporan.json di berat/artefak/ (diabaikan git). Ringkasan (Markdown dan JSON) ditulis ke
berat/hasil/ dan DISERTAKAN dalam repository karena kecil dan menjadi dasar angka di halaman.
Pembanding Linear SVM dilatih pada data LATIH yang sama dengan model neural (bukan data pengembangan), agar adil.
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parents[1]))  # folder examples/

from nlp_hub.eksperimen import metrik_emergency  # noqa: E402
from nlp_hub.modeling import buat_pipeline  # noqa: E402
from nlp_hub.proyek import siapkan  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--jenis", choices=("indobert", "lstm"), default="indobert")
ap.add_argument("--model", default="indobenchmark/indobert-base-p1")
ap.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3, 4, 5])
ap.add_argument("--epochs", type=int, default=3, help="epoch IndoBERT; LSTM selalu 15 (bawaan skripnya)")
ap.add_argument("--nama", default=None, help="nama berkas hasil; bawaan dari jenis/model")
ap.add_argument("--hanya-ringkas", action="store_true", help="tidak melatih; susun tabel dari JSON yang ada")
a = ap.parse_args()
nama = a.nama or ("lstm_pytorch" if a.jenis == "lstm" else re.sub(r"[^a-z0-9]+", "_", a.model.lower()))
(FOLDER / "hasil").mkdir(exist_ok=True)
berkas_json = FOLDER / "hasil" / f"{nama}.json"

POLA_LSTM = re.compile(r"^(uji sintetis|tulis-tangan): F1 makro ([\d.]+) \| recall E ([\d.]+) \| presisi E ([\d.]+)", re.M)


# --8<-- [start:jalankan]
def jalankan_seed(seed):
    mulai = time.perf_counter()
    if a.jenis == "indobert":
        keluar = FOLDER / "artefak" / f"{nama}_seed{seed}"
        perintah = [sys.executable, str(FOLDER / "12_finetune_indobert.py"), "--model", a.model, "--seed", str(seed),
                    "--epochs", str(a.epochs), "--output", str(keluar)]
    else:
        perintah = [sys.executable, str(FOLDER / "10_lstm_pytorch.py"), "--seed", str(seed)]
    hasil = subprocess.run(perintah, capture_output=True, text=True, encoding="utf-8")
    if hasil.returncode != 0:
        raise SystemExit(f"seed {seed} gagal:\n{hasil.stderr[-1500:]}")
    if a.jenis == "indobert":
        data = json.loads((keluar / "laporan.json").read_text(encoding="utf-8"))
    else:   # LSTM tidak menulis JSON; ambil dari baris keluaran
        data = {"model": "LSTM PyTorch (10_lstm_pytorch.py)", "seed": seed}
        for set_data, f1, rec, pre in POLA_LSTM.findall(hasil.stdout):
            data[set_data] = {"f1_makro": float(f1), "recall_e": float(rec), "presisi_e": float(pre)}
        import torch
        data.update({"torch": torch.__version__, "transformers": "-", "perangkat": "cpu" if not torch.cuda.is_available() else "cuda"})
    data["detik_total"] = round(time.perf_counter() - mulai)
    return data
# --8<-- [end:jalankan]


if a.hanya_ringkas:
    laporan = json.loads(berkas_json.read_text(encoding="utf-8"))
else:
    laporan = []
    for seed in a.seeds:
        data = jalankan_seed(seed)
        laporan.append(data)
        print(f"seed {seed}: tulis-tangan recall E {data['tulis-tangan']['recall_e']} | uji recall E {data['uji sintetis']['recall_e']} | {data['detik_total']} dtk", flush=True)
    berkas_json.write_text(json.dumps(laporan, indent=2, ensure_ascii=False), encoding="utf-8")

# --8<-- [start:ringkas]
d = siapkan()
y_latih = (d.latih["label"] == "Emergency").astype(int).to_numpy()
svm = buat_pipeline("svm").fit(d.latih["text"].to_numpy(), y_latih)       # data latih yang sama dengan model neural
baris_svm = {n: metrik_emergency(y, svm.predict(df["text"])) for n, df, y in
             (("uji sintetis", d.uji, d.y_uji), ("tulis-tangan", d.tangan, d.y_tangan))}


def rangkum(set_data, kunci):
    nilai = np.array([r[set_data][kunci] for r in laporan])
    return f"{nilai.mean():.3f} ({nilai.min():.3f}–{nilai.max():.3f})"


tabel = ["| Set | Metrik | Neural: rata-rata (min–maks) | Linear SVM (data latih sama) |", "|---|---|---|---|"]
for set_data in ("uji sintetis", "tulis-tangan"):
    for kunci, judul in (("recall_e", "recall Emergency"), ("presisi_e", "presisi Emergency"), ("f1_makro", "F1 makro")):
        tabel.append(f"| {set_data} | {judul} | {rangkum(set_data, kunci)} | {baris_svm[set_data][kunci]:.3f} |")
# --8<-- [end:ringkas]
meta = laporan[0]
kepala = (f"Model: `{meta['model']}`; {len(laporan)} seed {[r['seed'] for r in laporan]}; torch {meta['torch']}; transformers {meta['transformers']}; "
          f"perangkat: {meta['perangkat']}; waktu per seed: {[r['detik_total'] for r in laporan]} detik (termasuk pemuatan model; mesin CPU, "
          f"proses lain berjalan bersamaan pada sebagian seed).\n\n")
(FOLDER / "hasil" / f"{nama}.md").write_text(kepala + "\n".join(tabel) + "\n", encoding="utf-8")
print(kepala + "\n".join(tabel))
