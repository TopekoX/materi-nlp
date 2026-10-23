# Level 5: Evaluasi, Error Analysis, dan Eksperimen

Level ini mengajarkan cara mengukur model dengan benar dan mempelajari kesalahannya: confusion matrix,
presisi/recall/F1, class imbalance dan baseline, ambang, kurva PR dan ROC, error analysis, ablation,
robustness, audit kebocoran, ketidakpastian, dan penulisan laporan eksperimen. Model rujukan: Linear SVM
(dipilih dari validasi silang Level 4, bukan dari set tulis-tangan).

**Estimasi waktu:** 22–30 jam, termasuk latihan dan notebook.
**Prasyarat:** [Level 4](../level-4-machine-learning/index.md).

!!! warning "Prioritas recall Emergency, tetapi bukan ambang produksi"
    Pesan darurat yang terlewat (false negative) dapat berdampak serius, sehingga recall kelas Emergency
    menjadi prioritas. Namun false positive juga diukur karena sumber daya respons terbatas. **Tidak ada
    ambang produksi yang ditetapkan di sini.** Menetapkannya memerlukan data validasi yang representatif dan
    analisis biaya, yang tidak tersedia pada dataset sintetis.

## Daftar materi

| # | Materi | Topik spesifikasi |
|---|---|---|
| 1 | [Confusion Matrix: TP, TN, FP, FN](confusion-matrix.md) | 1, 2 |
| 2 | [Accuracy, Precision, Recall, F1, Makro/Mikro/Berbobot](metrik-klasifikasi.md) | 3, 4, 5, 6, 7 |
| 3 | [Class Imbalance dan Baseline](class-imbalance-baseline.md) | 8, 9 |
| 4 | [Threshold, Kurva PR, dan ROC/AUC](threshold-pr-roc.md) | 10, 11, 12 |
| 5 | [Error Analysis: FN dan FP](error-analysis.md) | 13, 14 |
| 6 | [Ablation Study dan Robustness](ablation-robustness.md) | 15, 16 |
| 7 | [Data Leakage, Ketidakpastian, Reproducibility](leakage-reproducibility.md) | 17, 18 |
| 8 | [Tabel Perbandingan dan Laporan Eksperimen](tabel-laporan-eksperimen.md) | 19, 20 |

## Capaian

- [ ] Menghitung metrik klasifikasi dari confusion matrix dan menafsirkannya untuk kelas Emergency.
- [ ] Menjelaskan mengapa akurasi menyesatkan pada kelas tidak seimbang dan memakai baseline.
- [ ] Menjelaskan trade-off ambang, membaca kurva PR/ROC, dan membedakan eksplorasi dari pemilihan ambang.
- [ ] Menjalankan error analysis, ablation, dan uji perturbasi serta menafsirkan hasilnya dengan jujur.
- [ ] Melakukan audit kebocoran, menghitung selang bootstrap, dan mencatat jejak reproducibility.
- [ ] Menulis laporan eksperimen dengan tabel yang dihasilkan dari kode.

## Temuan utama (dari eksekusi nyata, dataset sintetis)

| Temuan | Halaman |
|---|---|
| Akurasi 0,95 dapat dicapai tanpa menemukan satu Emergency pun (data 5% Emergency) | [Metrik](metrik-klasifikasi.md) |
| Pada tulis-tangan, SVM melewatkan 9 dari 24 pesan darurat dengan 0 alarm palsu | [Confusion Matrix](confusion-matrix.md) |
| AUC 0,976 tetapi recall 0,625 pada ambang bawaan; ambang dari validasi silang malah menurunkan recall menjadi 0,250 | [Threshold](threshold-pr-roc.md) |
| Hipotesis "FN karena kosakata asing" tidak didukung data (cakupan 0,57 vs 0,59) | [Error Analysis](error-analysis.md) |
| Emoji+hashtag+URL menurunkan recall tulis-tangan 0,625 → 0,458; komponen preprocessing tidak terbukti membantu | [Ablation dan Robustness](ablation-robustness.md) |
| Selang 95% recall tulis-tangan SVM [0,435; 0,810]; NB − SVM tidak cukup jelas | [Leakage dan Ketidakpastian](leakage-reproducibility.md) |

## Kode dan notebook

| Berkas | Isi |
|---|---|
| `examples/level-5-evaluation/01_*.py` – `08_*.py` | Skrip tiap halaman |
| `examples/level-5-evaluation/gambar_level5.py` | Pembuat gambar confusion matrix, PR, dan ROC |
| `examples/level-5-evaluation/05_evaluasi_dan_error_analysis.ipynb` | Notebook evaluasi (sudah dieksekusi) |
| `examples/level-5-evaluation/hasil/*.md` | Tabel laporan yang ditulis skrip dan disertakan halaman |
| `examples/nlp_hub/perturbasi.py`, `proyek.py`, `eksperimen.py` | Perturbasi, penyiapan data, metrik dan bootstrap |
| `examples/check_page_outputs.py` | Memeriksa bahwa blok "Output nyata" di halaman sama dengan keluaran skrip |

## Checkpoint praktis

Sebelum lanjut ke Level 6, pastikan Anda dapat:

1. Menghitung presisi, recall, dan F1 dari TP = 15, FP = 0, FN = 9 tanpa melihat catatan.
2. Menjelaskan mengapa menurunkan ambang menaikkan recall dan biasanya menurunkan presisi.
3. Menjelaskan mengapa memilih ambang dari set uji adalah data snooping.
4. Menyebut tiga hal yang membatasi kesimpulan dari 48 teks tulis-tangan.

## Materi selanjutnya

Mulai dengan [Confusion Matrix](confusion-matrix.md). Setelah Level 5, lanjut ke
[Level 6: Deep Learning](../level-6-deep-learning/index.md).
