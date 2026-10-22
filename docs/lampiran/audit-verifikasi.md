# Audit dan Verifikasi

Log pemeriksaan jujur: apa yang sudah dijalankan, apa yang gagal, dan apa yang
belum dilakukan. Diperbarui setiap tahap.

## Log verifikasi

| Tanggal | Tahap | Pemeriksaan | Hasil |
|---|---|---|---|
| 2026-10-22 | 1 | `mkdocs build --strict` pada template awal | Lolos |
| 2026-10-22 | 2 | Build strict setelah kerangka | Gagal sementara: 1 tautan ke halaman Level 0 yang belum ada; diperbaiki di Tahap 3 |
| 2026-10-22 | 3 | Skrip `examples/level-0-orientasi/*.py` dijalankan; output disalin dari eksekusi | Lolos |
| 2026-10-22 | 3 | Skrip `examples/level-1-python/01-16_*.py` dijalankan (Python 3.14.7, numpy 2.5.4, pandas 3.1.0); output disalin dari eksekusi | Lolos |
| 2026-10-22 | 3 | `mkdocs build --strict` (Level 0-1) | Lolos |

## Belum diperiksa

- Rendering visual di browser (hanya build statis yang diperiksa).
- Kebenaran DOI/URL di [Referensi](../referensi.md) terhadap sumber daring.
