# Latihan dan Kuis

Latihan bertahap dan kuis lintas level, masing-masing dengan **kunci jawaban dan pembahasan**. Kode kunci disimpan di `examples/latihan/` dan diuji (`tests/test_latihan.py`), jadi jawaban yang dipublikasikan dijaga agar tetap benar.

## Daftar

| Halaman | Cakupan | Estimasi |
|---|---|---|
| [Latihan Level 0–1](level-0-1.md) | Orientasi, Python, dict, regex, baseline kata kunci | 2 jam |
| [Latihan Level 2–3](level-2-3.md) | Preprocessing, Bag of Words, TF-IDF dengan tangan, n-gram | 2,5 jam |
| [Latihan Level 4–5](level-4-5.md) | Metrik, baseline, kebocoran, ambang | 3 jam |
| [Latihan Level 6–7](level-6-7.md) | Kosinus, softmax, attention, gradien, PSI, tes API, fine-tuning | 4 jam |
| [Latihan Proyek dan Kuis Gabungan](proyek.md) | Lima mini-proyek (berrubrik) + 12 pertanyaan kuis | 5–10 jam |

## Cara belajar yang disarankan

1. Kerjakan soal **sebelum** membuka kunci. Tulis jawaban atau kode Anda sendiri.
2. Jalankan kode Anda dan bandingkan keluarannya dengan kunci. Perbedaan adalah bahan belajar.
3. Soal bertingkat: ★ konseptual, ★★ membaca/mengisi kode, ★★★ menulis/mendebug, ★★★★ mini-proyek.
4. Tandai **checkpoint** di akhir tiap halaman sebelum lanjut ke level berikutnya.

## Menjalankan kunci jawaban

Dari folder `examples/`:

```powershell
python latihan/solusi_level_0_1.py
python latihan/solusi_level_2_3.py
python latihan/solusi_level_4_5.py
python latihan/solusi_level_6_7.py
python -m pytest tests/test_latihan.py -q
```

## Catatan kejujuran

Soal dan kuis ditulis oleh penulis materi dan **belum diuji pada pembaca pemula sungguhan**. Soal bertanda **[berat]** membutuhkan PyTorch dan Transformers (`requirements-dl.txt`). Angka dalam kunci berasal dari eksekusi nyata pada dataset sintetis dan **tidak** menggambarkan performa pada postingan nyata.
