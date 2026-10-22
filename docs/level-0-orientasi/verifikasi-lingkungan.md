# Instalasi dan Verifikasi Lingkungan Pengembangan

## Tujuan pembelajaran

- [ ] Memasang dependensi dasar kurikulum.
- [ ] Menjalankan skrip verifikasi dan membaca hasilnya.
- [ ] Mendiagnosis masalah instalasi yang paling umum.

## Prasyarat

[Persiapan Python, Virtual Environment, pip, Jupyter, dan Git](persiapan-python.md) dengan `.venv` aktif.

## Pengantar dan intuisi

"Di komputer saya jalan" bukan bukti. Verifikasi lingkungan membuat kita tahu
**versi apa** yang dipakai, sehingga hasil eksperimen dapat diulang dan galat
mudah ditelusuri. Lakukan sekali di awal dan ulangi setelah mengubah paket.

## Konsep

Verifikasi menjawab tiga pertanyaan:

1. Python yang aktif berasal dari `.venv`?
2. Semua paket wajib dapat di-*import*?
3. Versi paket apa yang terpasang (untuk dicatat pada laporan eksperimen)?

## Contoh kontekstual kebencanaan

Tim relawan menjalankan notebook klasifikasi pesan darurat di beberapa
laptop. Satu laptop memberi hasil sedikit berbeda karena versi scikit-learn
berbeda. Mencatat versi dari skrip verifikasi mempercepat penelusurannya.

## Contoh kode

```python title="verifikasi_lingkungan.py" linenums="1"
--8<-- "level-0-orientasi/verifikasi_lingkungan.py"
```

Jalankan dari akar repository:

```bash
python examples/level-0-orientasi/verifikasi_lingkungan.py
```

### Penjelasan kode

1. `versi` mencoba meng-*import* modul dan membaca `__version__`. Jika gagal, mengembalikan `None`.
2. Paket wajib dan opsional dipisah. Kegagalan paket wajib membuat program berakhir dengan kode keluar `1`, sehingga dapat dipakai dalam otomasi.
3. Nama modul untuk scikit-learn adalah `sklearn`, bukan `scikit-learn`; ini sumber kebingungan yang umum.

### Output dan interpretasi

Output di bawah berasal dari eksekusi pada mesin penulis (Windows, Python 3.14). Versi dan jalur pada komputer Anda akan berbeda; yang penting semua baris wajib berstatus `OK`.

```text
Python  : 3.14.7
Lokasi  : D:\...\materi-nlp\.venv\Scripts\python.exe
[OK] numpy        2.5.4
[OK] pandas       3.1.0
[OK] sklearn      1.9.1
[OK] matplotlib   3.11.2
[OK] Sastrawi     terpasang
[OK] joblib       1.6.0
[OK] fastapi      0.159.1
[OK] pytest       9.1.1
[--] torch        tidak terpasang (opsional)
[--] transformers tidak terpasang (opsional)

Lingkungan siap untuk Level 1-5.
```

Baris `[--]` untuk paket opsional (`torch`, `transformers`) wajar sebelum Level 6.

## Kesalahan umum

| Gejala | Penyebab umum | Perbaikan |
|---|---|---|
| `ModuleNotFoundError` | `.venv` tidak aktif atau paket belum dipasang | Aktifkan `.venv`, lalu `pip install -r requirements-ml.txt` |
| `pip` memasang ke Python global | Memakai `pip` global | Gunakan `python -m pip install ...` dari `.venv` |
| Gagal membangun paket di Python terbaru | Belum ada *wheel* untuk versi Python Anda | Pakai Python versi stabil yang lebih rendah (mis. 3.12) |
| Emoji jadi `????` di Windows | Encoding konsol | `python -X utf8 skrip.py` atau `set PYTHONUTF8=1` |
| Notebook tidak melihat paket | Kernel Jupyter bukan dari `.venv` | `python -m ipykernel install --user --name nlp-hub` lalu pilih kernel itu |

## Latihan mandiri

1. Jalankan skrip, lalu `pip uninstall -y joblib` sementara dan jalankan lagi. Apa kode keluarnya? Pasang kembali.
2. Tambahkan `scipy` ke `PAKET_WAJIB`.
3. Simpan output skrip ke berkas `lingkungan.txt` dan jelaskan mengapa berkas ini berguna di laporan eksperimen.

## Kuis singkat

**1.** Mengapa nama modul `sklearn` berbeda dari nama paket pip?

??? success "Jawaban"
    Nama paket di PyPI adalah `scikit-learn`, tetapi modul yang di-*import* bernama `sklearn`; keduanya tidak harus sama.

**2.** Apa gunanya kode keluar non-nol?

??? success "Jawaban"
    Memberi tahu skrip lain atau CI bahwa pemeriksaan gagal.

## Ringkasan

Verifikasi lingkungan memastikan Python yang benar, paket lengkap, dan versi
tercatat. Kebanyakan masalah berasal dari `.venv` yang tidak aktif.

## Referensi

- Dokumentasi Python: `importlib` (<https://docs.python.org/3/library/importlib.html>).
- Dokumentasi Jupyter: *Installing the IPython kernel* (<https://ipython.readthedocs.io/en/stable/install/kernel_install.html>).

## Materi selanjutnya

[Mini Proyek: Memahami dan Mengelompokkan Teks Secara Manual](mini-proyek-manual.md)
