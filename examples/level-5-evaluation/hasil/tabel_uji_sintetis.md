| model | akurasi | presisi E | recall E | selang 95% recall E | F1 E | F1 makro | FN | FP |
|---|---|---|---|---|---|---|---|---|
| Baseline: selalu Non-Emergency | 0.661 | 0.000 | 0.000 | [0.00, 0.00] | 0.000 | 0.398 | 38 | 0 |
| Multinomial NB | 0.973 | 0.949 | 0.974 | [0.91, 1.00] | 0.961 | 0.970 | 1 | 2 |
| Logistic Regression | 0.982 | 1.000 | 0.947 | [0.86, 1.00] | 0.973 | 0.980 | 2 | 0 |
| Linear SVM | 0.982 | 0.950 | 1.000 | [1.00, 1.00] | 0.974 | 0.980 | 0 | 2 |
