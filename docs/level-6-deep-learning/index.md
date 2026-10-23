# Level 6: Deep Learning untuk NLP

Dari embedding kata sampai fine-tuning model Transformer berbahasa Indonesia, dengan mekanisme yang ditulis dari nol di NumPy dan praktik modern di PyTorch/Transformers.

**Estimasi waktu:** 28–38 jam, termasuk latihan.
**Prasyarat:** [Level 5](../level-5-evaluasi/index.md).

!!! warning "Dua jenis kode, dua tingkat bukti"
    - **Ringan** (NumPy, scikit-learn): dijalankan, dites, dan keluarannya diperiksa otomatis terhadap halaman. Berjalan di CPU dalam hitungan detik.
    - **Berat** (PyTorch, Transformers; folder `berat/`): **dijalankan penulis pada 2026-10-23** di CPU (torch 2.14.1, transformers 5.20.2): tokenizer IndoBERT, LSTM × 5 seed, dan fine-tuning dua model IndoBERT × 5 seed. Hasilnya disertakan dari `berat/hasil/`, diberi label **tidak diperiksa otomatis** (bergantung unduhan model, versi, dan mesin), dan hanya berlaku untuk dataset sintetis kecil. Tes hanya memeriksa sintaks skrip. Lihat [Komputasi dan Dependensi](ml-klasik-vs-dl-komputasi.md).
    - `mkdocs build` tidak menjalankan kode apa pun.

## Daftar materi

| # | Materi | Topik spesifikasi | Kode |
|---|---|---|---|
| 1 | [ML Klasik vs Deep Learning, Komputasi, Dependensi](ml-klasik-vs-dl-komputasi.md) | 1, 24 | `cek_lingkungan_dl.py` |
| 2 | [Embedding Kata: Word2Vec, GloVe, FastText, OOV](embedding-kata.md) | 2, 3, 4, 5, 6 | `01_embedding.py` (ringan) |
| 3 | [Neural Network Dasar](neural-network-dasar.md) | 7, 8, 9 | `02_neural_network.py` (ringan) |
| 4 | [RNN, LSTM, dan GRU](rnn-lstm-gru.md) | 10, 11, 12 | `03_rnn_lstm_gru.py` (ringan); `berat/10_lstm_pytorch.py` |
| 5 | [Attention, Self-Attention, Transformer](attention-transformer.md) | 13, 14, 15, 16, 18 | `04_attention_transformer.py` (ringan) |
| 6 | [Tokenizer Modern, BERT, IndoBERT](tokenizer-bert-indobert.md) | 17, 19, 20 | `05_tokenizer_subword.py` (ringan); `berat/11_tokenizer_indobert.py` |
| 7 | [Fine-tuning dan Transfer Learning](fine-tuning-transfer-learning.md) | 21, 22 | `berat/12_finetune_indobert.py` |
| 8 | [Overfitting, Regularisasi, Evaluasi DL](overfitting-evaluasi-dl.md) | 23, 25 | `06_mlp_vs_klasik.py` (ringan) |

Semua 25 topik wajib spesifikasi tercakup. Kode bersama: `examples/nlp_hub/embedding.py`, `jaringan.py`, `atensi.py`, `subword.py`; tes: `examples/tests/test_embedding.py`, `test_jaringan.py`, `test_atensi.py`, `test_subword.py`.

## Capaian

- [ ] Menjelaskan perbedaan fitur yang dirancang dan fitur yang dipelajari, serta kapan deep learning layak dicoba.
- [ ] Membuat embedding dari ko-kemunculan dan menjelaskan OOV serta subword.
- [ ] Menghitung forward, backward, dan loss jaringan kecil dengan tangan dan memeriksanya dengan gradient check.
- [ ] Menjelaskan sel RNN/LSTM/GRU, gradien menghilang, attention, positional encoding, dan encoder vs decoder.
- [ ] Menjelaskan tokenizer BPE/WordPiece, BERT, dan perbedaan dua model "IndoBERT".
- [ ] Merencanakan dan melaporkan fine-tuning dengan jujur (seed, validasi, rentang, tanpa klaim berlebihan).

## Temuan utama (dari eksekusi nyata, dataset sintetis)

| Temuan | Halaman |
|---|---|
| Embedding dari 8 kalimat terkontrol: kosinus `gempa`–`retak` 0,94 vs `air`–`retak` −0,04; dari 564 teks bertemplat, tetangga banyak yang tidak bermakna | [Embedding](embedding-kata.md) |
| Gradient check: selisih relatif $5\times10^{-11}$; XOR: regresi logistik 0,5, MLP 1,0 | [Neural Network](neural-network-dasar.md) |
| Pengaruh keadaan awal RNN menyusut dari $6\times10^{-2}$ (5 langkah) ke $2\times10^{-15}$ (50 langkah) | [RNN, LSTM, GRU](rnn-lstm-gru.md) |
| Tanpa positional encoding, mengacak kata hanya mengacak keluaran; biaya attention $T^2$ | [Attention](attention-transformer.md) |
| BPE kecil: `banjir` satu potongan, `banjirnya` empat potongan; WordPiece memberi `[UNK]` untuk `meluap` | [Tokenizer](tokenizer-bert-indobert.md) |
| MLP NumPy vs SVM: recall Emergency tulis-tangan 0,792–0,833 vs 0,583 (48 teks, 3 seed; **bukan bukti keunggulan**) | [Overfitting dan Evaluasi](overfitting-evaluasi-dl.md) |
| IndoBERT p1 (5 seed, CPU): recall E tulis-tangan 0,825 (0,708–0,917), presisi 1,000 vs SVM 0,583 pada data latih sama; IndoLEM jauh lebih rendah (0,442); LSTM dari nol 0,192 | [Fine-tuning](fine-tuning-transfer-learning.md), [RNN](rnn-lstm-gru.md), [Tahap G](../proyek-klasifikasi-bencana/tahap-g-advanced-modeling.md) |

## Kode dan dependensi

| Berkas | Isi |
|---|---|
| `examples/level-6-deep-learning/01_*.py` – `06_*.py` | Skrip ringan tiap halaman |
| `examples/level-6-deep-learning/cek_lingkungan_dl.py` | Memeriksa torch/transformers/CUDA |
| `examples/level-6-deep-learning/berat/` | Skrip PyTorch/Transformers (dieksekusi), `13_ulang_seed.py`, `hasil/` (tabel dan JSON), dan `README.md` |
| `requirements-dl.txt` | Dependensi berat opsional |

## Checkpoint praktis

Sebelum lanjut ke Level 7, pastikan Anda dapat:

1. Menghitung kosinus dua vektor 2 dimensi dan menjelaskan artinya.
2. Menjelaskan mengapa XOR membutuhkan lapisan tersembunyi.
3. Menghitung softmax tiga angka dan menjelaskan peran $\sqrt{d_k}$.
4. Menjelaskan mengapa `[UNK]` muncul pada WordPiece tetapi tidak pada BPE.
5. Menyebut tiga hal yang membatasi kesimpulan dari perbandingan MLP vs SVM di halaman terakhir.
6. Menjelaskan mengapa hasil IndoBERT lima seed dilaporkan sebagai rentang dan mengapa tidak membuktikan keunggulan umum.

## Materi selanjutnya

Mulai dengan [ML Klasik vs Deep Learning, Komputasi, dan Dependensi](ml-klasik-vs-dl-komputasi.md). Setelah Level 6, lanjut ke [Level 7: Advanced NLP dan Deployment](../level-7-advanced-nlp/index.md).
