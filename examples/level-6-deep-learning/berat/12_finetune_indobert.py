"""Fine-tuning IndoBERT untuk klasifikasi Emergency/Non-Emergency (EKSPERIMEN BERAT: torch + transformers + unduhan model).

Memakai perulangan pelatihan PyTorch biasa (bukan Trainer) agar setiap langkah terlihat dan tidak bergantung
pada nama argumen yang berubah antar versi transformers. Model terbaik (loss validasi terendah) disimpan
bersama tokenizer. Hasil bergantung pada seed, versi library, dan perangkat keras; catat semuanya.
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # folder examples/

import numpy as np
import torch
import transformers
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

from nlp_hub.eksperimen import metrik_emergency
from nlp_hub.proyek import siapkan

ap = argparse.ArgumentParser()
ap.add_argument("--model", default="indobenchmark/indobert-base-p1")
ap.add_argument("--epochs", type=int, default=3)
ap.add_argument("--batch", type=int, default=16)
ap.add_argument("--lr", type=float, default=2e-5)
ap.add_argument("--max-len", type=int, default=64)
ap.add_argument("--seed", type=int, default=42)
ap.add_argument("--subset", type=int, default=0, help="pakai hanya N teks latih (uji asap); 0 = semua")
ap.add_argument("--output", default=str(Path(__file__).resolve().parent / "artefak" / "indobert_emergency"))
a = ap.parse_args()

# --8<-- [start:siapkan]
torch.manual_seed(a.seed)
np.random.seed(a.seed)
perangkat = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"torch {torch.__version__} | transformers {transformers.__version__} | perangkat: {perangkat}")

d = siapkan()
latih = d.latih.sample(a.subset, random_state=a.seed) if a.subset else d.latih
tokenizer = AutoTokenizer.from_pretrained(a.model)
model = AutoModelForSequenceClassification.from_pretrained(a.model, num_labels=2).to(perangkat)
model.config.id2label = {0: "Non-Emergency", 1: "Emergency"}
model.config.label2id = {"Non-Emergency": 0, "Emergency": 1}
# --8<-- [end:siapkan]


# --8<-- [start:fungsi]
def enkode(df):
    return tokenizer(list(df["text"]), padding=True, truncation=True, max_length=a.max_len, return_tensors="pt")


def prediksi(df):
    """Mengembalikan P(Emergency) untuk tiap teks (softmax atas dua logit)."""
    model.eval()
    hasil = []
    with torch.no_grad():
        for awal in range(0, len(df), 32):
            b = {k: v.to(perangkat) for k, v in enkode(df.iloc[awal: awal + 32]).items()}
            hasil.append(torch.softmax(model(**b).logits, dim=-1)[:, 1].cpu())
    return torch.cat(hasil).numpy()
# --8<-- [end:fungsi]


# --8<-- [start:latih]
y_latih = torch.tensor((latih["label"] == "Emergency").astype(int).to_numpy())
pemuat = DataLoader(list(range(len(latih))), batch_size=a.batch, shuffle=True)
optimizer = torch.optim.AdamW(model.parameters(), lr=a.lr, weight_decay=0.01)
total = a.epochs * len(pemuat)
jadwal = get_linear_schedule_with_warmup(optimizer, int(0.1 * total), total)

terbaik, mulai = float("inf"), time.perf_counter()
y_val = torch.tensor((d.val["label"] == "Emergency").astype(int).to_numpy())
for epoch in range(a.epochs):
    model.train()
    for idx in pemuat:
        b = {k: v.to(perangkat) for k, v in enkode(latih.iloc[idx.tolist()]).items()}
        keluaran = model(**b, labels=y_latih[idx].to(perangkat))
        keluaran.loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        jadwal.step()
        optimizer.zero_grad()
    p_val = torch.tensor(prediksi(d.val)).clamp(1e-6, 1 - 1e-6)
    lv = torch.nn.functional.binary_cross_entropy(p_val, y_val.float()).item()
    print(f"epoch {epoch + 1}: loss latih (batch terakhir) {keluaran.loss.item():.4f} | loss validasi {lv:.4f}")
    if lv < terbaik:
        terbaik = lv
        model.save_pretrained(a.output)
        tokenizer.save_pretrained(a.output)
print(f"waktu pelatihan: {time.perf_counter() - mulai:.0f} detik")
# --8<-- [end:latih]

# --8<-- [start:evaluasi]
model = AutoModelForSequenceClassification.from_pretrained(a.output).to(perangkat)   # muat model TERBAIK
laporan = {"model": a.model, "seed": a.seed, "torch": torch.__version__, "transformers": transformers.__version__,
           "perangkat": str(perangkat), "data": "SINTETIS; bukan untuk penggunaan operasional"}
for nama, df, y_benar in (("uji sintetis", d.uji, d.y_uji), ("tulis-tangan", d.tangan, d.y_tangan)):
    m = metrik_emergency(y_benar, (prediksi(df) >= 0.5).astype(int))
    laporan[nama] = {k: round(v, 3) for k, v in m.items()}
    print(f"{nama}: F1 makro {m['f1_makro']:.3f} | recall E {m['recall_e']:.3f} | presisi E {m['presisi_e']:.3f}")
Path(a.output, "laporan.json").write_text(json.dumps(laporan, indent=2, ensure_ascii=False), encoding="utf-8")
# --8<-- [end:evaluasi]
