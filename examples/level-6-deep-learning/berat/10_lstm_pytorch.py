"""Klasifikasi Emergency/Non-Emergency dengan LSTM PyTorch (EKSPERIMEN BERAT: butuh torch).

Alur: token -> id -> embedding -> LSTM -> keadaan tersembunyi terakhir -> Linear -> logit.
Kosakata dibangun HANYA dari data latih; kata lain menjadi <unk>.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # folder examples/

import numpy as np
import torch
from torch import nn

from nlp_hub.eksperimen import metrik_emergency
from nlp_hub.preprocessing import praproses_token
from nlp_hub.proyek import siapkan

PAD, UNK = 0, 1


# --8<-- [start:model]
class KlasifikasiLSTM(nn.Module):
    def __init__(self, n_kosakata, dim_embedding=64, dim_h=64, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(n_kosakata, dim_embedding, padding_idx=PAD)
        self.lstm = nn.LSTM(dim_embedding, dim_h, batch_first=True)
        self.dropout = nn.Dropout(dropout)
        self.keluaran = nn.Linear(dim_h, 1)

    def forward(self, ids, panjang):
        e = self.dropout(self.embedding(ids))
        paket = nn.utils.rnn.pack_padded_sequence(e, panjang.cpu(), batch_first=True, enforce_sorted=False)
        _, (h, _) = self.lstm(paket)              # h: (1, batch, dim_h) = keadaan terakhir TANPA padding
        return self.keluaran(self.dropout(h[-1])).squeeze(-1)   # logit (belum sigmoid)
# --8<-- [end:model]


# --8<-- [start:ke_id]
def ke_id(daftar_token, kosakata, maks=40):
    ids = [[kosakata.get(t, UNK) for t in tok][:maks] or [UNK] for tok in daftar_token]
    panjang = torch.tensor([len(x) for x in ids])
    papan = torch.zeros(len(ids), int(panjang.max()), dtype=torch.long)
    for i, x in enumerate(ids):
        papan[i, : len(x)] = torch.tensor(x)
    return papan, panjang
# --8<-- [end:ke_id]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=15)
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    torch.manual_seed(a.seed)
    np.random.seed(a.seed)
    d = siapkan()
    tok = lambda df: [praproses_token(t) for t in df["text"]]
    t_latih, t_val, t_uji, t_tangan = tok(d.latih), tok(d.val), tok(d.uji), tok(d.tangan)
    hitung = {}
    for x in t_latih:
        for t in x:
            hitung[t] = hitung.get(t, 0) + 1
    kosakata = {k: i + 2 for i, k in enumerate(sorted(k for k, n in hitung.items() if n >= 2))}
    y = lambda df: torch.tensor((df["label"] == "Emergency").astype(float).to_numpy(), dtype=torch.float32)
    X_latih, X_val, X_uji, X_tangan = (ke_id(t, kosakata) for t in (t_latih, t_val, t_uji, t_tangan))
    y_latih, y_val = y(d.latih), y(d.val)

    # --8<-- [start:latih]
    model = KlasifikasiLSTM(len(kosakata) + 2)
    optimizer = torch.optim.Adam(model.parameters(), lr=3e-3)
    kriteria = nn.BCEWithLogitsLoss()
    terbaik, salinan = float("inf"), None
    for epoch in range(a.epochs):
        model.train()
        urutan = torch.randperm(len(y_latih))
        for awal in range(0, len(urutan), 32):
            idx = urutan[awal: awal + 32]
            optimizer.zero_grad()
            loss = kriteria(model(X_latih[0][idx], X_latih[1][idx]), y_latih[idx])
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)   # menahan gradien yang meledak
            optimizer.step()
        model.eval()
        with torch.no_grad():
            lv = kriteria(model(*X_val), y_val).item()
        print(f"epoch {epoch + 1:2}: loss validasi {lv:.4f}")
        if lv < terbaik:
            terbaik, salinan = lv, {k: v.clone() for k, v in model.state_dict().items()}
    # --8<-- [end:latih]
    model.load_state_dict(salinan)
    model.eval()
    with torch.no_grad():
        for nama, X, yy in (("uji sintetis", X_uji, d.y_uji), ("tulis-tangan", X_tangan, d.y_tangan)):
            pred = (torch.sigmoid(model(*X)) >= 0.5).int().numpy()
            m = metrik_emergency(yy, pred)
            print(f"{nama}: F1 makro {m['f1_makro']:.3f} | recall E {m['recall_e']:.3f} | presisi E {m['presisi_e']:.3f}")


if __name__ == "__main__":
    main()
