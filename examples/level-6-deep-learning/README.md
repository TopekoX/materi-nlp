# Level 6: Deep learning untuk NLP

Dua kelompok kode, dipisahkan sengaja:

| Kelompok | Lokasi | Dependensi | Dijalankan oleh |
|---|---|---|---|
| **Ringan** | `01_*.py` – `06_*.py`, `cek_lingkungan_dl.py` | NumPy, scikit-learn, pandas (`requirements-ml.txt`) | pytest, `check_page_outputs.py`, Anda |
| **Berat** | `berat/` | PyTorch, Transformers (`requirements-dl.txt`) | hanya Anda, dengan sengaja |

Kode ringan mengimplementasikan mekanisme dari nol dengan NumPy (embedding, propagasi mundur, sel RNN/LSTM/GRU,
attention) supaya setiap angka dapat diperiksa. Kode berat memakai PyTorch dan Hugging Face Transformers.

`mkdocs build` tidak menjalankan kode apa pun: halaman hanya menyalin teks skrip. Lihat `berat/README.md` untuk cara
menjalankan eksperimen berat dan `python level-6-deep-learning/cek_lingkungan_dl.py` untuk memeriksa lingkungan.
