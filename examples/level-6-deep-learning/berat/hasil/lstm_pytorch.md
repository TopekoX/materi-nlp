Model: `LSTM PyTorch (10_lstm_pytorch.py)`; 5 seed [1, 2, 3, 4, 5]; torch 2.14.1+cpu; transformers -; perangkat: cpu; waktu per seed: [8, 5, 5, 5, 5] detik (termasuk pemuatan model; mesin CPU, proses lain berjalan bersamaan pada sebagian seed).

| Set | Metrik | Neural: rata-rata (min–maks) | Linear SVM (data latih sama) |
|---|---|---|---|
| uji sintetis | recall Emergency | 0.968 (0.947–1.000) | 1.000 |
| uji sintetis | presisi Emergency | 0.964 (0.923–1.000) | 0.950 |
| uji sintetis | F1 makro | 0.974 (0.951–1.000) | 0.980 |
| tulis-tangan | recall Emergency | 0.192 (0.000–0.333) | 0.583 |
| tulis-tangan | presisi Emergency | 0.778 (0.000–1.000) | 1.000 |
| tulis-tangan | F1 makro | 0.505 (0.333–0.608) | 0.782 |
