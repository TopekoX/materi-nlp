Model: `indobenchmark/indobert-base-p1`; 5 seed [1, 2, 3, 4, 5]; torch 2.14.1+cpu; transformers 5.20.2; perangkat: cpu; waktu per seed: [217, 141, 112, 111, 114] detik (termasuk pemuatan model; mesin CPU, proses lain berjalan bersamaan pada sebagian seed).

| Set | Metrik | Neural: rata-rata (min–maks) | Linear SVM (data latih sama) |
|---|---|---|---|
| uji sintetis | recall Emergency | 0.979 (0.947–1.000) | 1.000 |
| uji sintetis | presisi Emergency | 0.984 (0.974–1.000) | 0.950 |
| uji sintetis | F1 makro | 0.986 (0.980–1.000) | 0.980 |
| tulis-tangan | recall Emergency | 0.825 (0.708–0.917) | 0.583 |
| tulis-tangan | presisi Emergency | 1.000 (1.000–1.000) | 1.000 |
| tulis-tangan | F1 makro | 0.911 (0.851–0.958) | 0.782 |
