Model: `indolem/indobert-base-uncased`; 5 seed [1, 2, 3, 4, 5]; torch 2.14.1+cpu; transformers 5.20.2; perangkat: cpu; waktu per seed: [181, 113, 102, 109, 108] detik (termasuk pemuatan model; mesin CPU, proses lain berjalan bersamaan pada sebagian seed).

| Set | Metrik | Neural: rata-rata (min–maks) | Linear SVM (data latih sama) |
|---|---|---|---|
| uji sintetis | recall Emergency | 0.937 (0.895–0.947) | 1.000 |
| uji sintetis | presisi Emergency | 0.849 (0.773–0.900) | 0.950 |
| uji sintetis | F1 makro | 0.915 (0.865–0.941) | 0.980 |
| tulis-tangan | recall Emergency | 0.442 (0.375–0.542) | 0.583 |
| tulis-tangan | presisi Emergency | 0.879 (0.786–1.000) | 1.000 |
| tulis-tangan | F1 makro | 0.666 (0.644–0.719) | 0.782 |
