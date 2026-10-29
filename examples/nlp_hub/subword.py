"""Tokenisasi subword mini (Level 6): pembelajaran BPE dan pemecahan greedy ala WordPiece.

Ini versi pengajaran yang disederhanakan. Tokenizer BERT/IndoBERT sungguhan dilatih pada korpus
sangat besar dan punya aturan normalisasi tambahan; gunakan `AutoTokenizer` untuk model nyata.
"""
from collections import Counter


def hitung_kata(daftar_kata):
    return Counter(daftar_kata)


def latih_bpe(hitung, n_gabung):
    """Mempelajari `n_gabung` aturan BPE dari Counter kata. Mengembalikan daftar pasangan yang digabung, berurutan.

    Awalnya setiap kata = deretan huruf + penanda akhir kata '</w>'. Tiap putaran, pasangan simbol bersebelahan
    yang paling sering digabung menjadi satu simbol baru (seri diputus secara abjad agar hasil tetap).
    """
    kosakata = {tuple(k) + ("</w>",): n for k, n in hitung.items()}
    aturan = []
    for _ in range(n_gabung):
        pasangan = Counter()
        for simbol, n in kosakata.items():
            for a, b in zip(simbol, simbol[1:]):
                pasangan[(a, b)] += n
        if not pasangan:
            break
        terbaik = min(pasangan, key=lambda p: (-pasangan[p], p))
        aturan.append(terbaik)
        baru = {}
        for simbol, n in kosakata.items():
            hasil, i = [], 0
            while i < len(simbol):
                if i < len(simbol) - 1 and (simbol[i], simbol[i + 1]) == terbaik:
                    hasil.append(simbol[i] + simbol[i + 1])
                    i += 2
                else:
                    hasil.append(simbol[i])
                    i += 1
            baru[tuple(hasil)] = n
        kosakata = baru
    return aturan


def terapkan_bpe(kata, aturan):
    """Memecah satu kata dengan menerapkan aturan BPE sesuai urutan belajarnya."""
    simbol = list(kata) + ["</w>"]
    for a, b in aturan:
        i = 0
        while i < len(simbol) - 1:
            if simbol[i] == a and simbol[i + 1] == b:
                simbol[i:i + 2] = [a + b]
            else:
                i += 1
    return simbol


def pecah_wordpiece(kata, kosakata, tanda="##", tak_dikenal="[UNK]"):
    """Pemecahan greedy longest-match-first ala WordPiece. Potongan non-awal diberi awalan '##'.

    Bila ada bagian kata yang tidak bisa dicocokkan, seluruh kata menjadi [UNK] (perilaku WordPiece asli).
    """
    potongan, awal = [], 0
    while awal < len(kata):
        akhir, cocok = len(kata), None
        while akhir > awal:
            kandidat = kata[awal:akhir] if awal == 0 else tanda + kata[awal:akhir]
            if kandidat in kosakata:
                cocok = kandidat
                break
            akhir -= 1
        if cocok is None:
            return [tak_dikenal]
        potongan.append(cocok)
        awal = akhir
    return potongan
