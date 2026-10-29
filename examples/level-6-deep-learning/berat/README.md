# Eksperimen berat Level 6 (PyTorch dan Transformers)

Folder ini berisi skrip yang butuh `torch` dan `transformers`. Skrip di sini:

- **tidak dijalankan** oleh `mkdocs build` (MkDocs hanya menyalin teks skrip lewat `pymdownx.snippets`);
- **tidak dikumpulkan** oleh `pytest` bawaan (`testpaths = tests`); tes terkait memakai `pytest.importorskip` dan dilewati bila `torch` tidak ada;
- **tidak diperiksa** oleh `check_page_outputs.py` (skrip di folder `berat/` sengaja dilewati).

Instal (dari akar repository, setelah `requirements-ml.txt`):

    pip install -r requirements-dl.txt

Untuk PyTorch ikuti perintah resmi di https://pytorch.org/get-started/locally/ agar sesuai CPU/CUDA.

Jalankan dari folder `examples/`:

    python level-6-deep-learning/berat/10_lstm_pytorch.py
    python level-6-deep-learning/berat/11_tokenizer_indobert.py
    python level-6-deep-learning/berat/12_finetune_indobert.py --subset 64 --epochs 1   # uji asap
    python level-6-deep-learning/berat/12_finetune_indobert.py                          # penuh, satu seed
    python level-6-deep-learning/berat/13_ulang_seed.py --seeds 1 2 3 4 5               # lima seed + tabel ke hasil/
    python level-6-deep-learning/berat/13_ulang_seed.py --jenis lstm                    # LSTM lima seed

`11_...` dan `12_...` mengunduh berkas dari Hugging Face Hub pada pemakaian pertama (bobot model sekitar 0,5 GB).
Folder `hasil/` memuat tabel Markdown dan JSON hasil eksekusi nyata penulis (2026-10-23, CPU, torch 2.14.1, transformers 5.20.2) yang disertakan halaman dokumentasi; folder `artefak/` (bobot model) diabaikan git. Hasil Anda dapat berbeda sedikit karena versi, perangkat, dan seed. Status verifikasi dicatat di `docs/lampiran/audit-verifikasi.md`.
