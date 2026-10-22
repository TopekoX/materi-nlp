# Persiapan Python, Virtual Environment, pip, Jupyter Notebook, dan Git

## Tujuan pembelajaran

- [ ] Memahami fungsi Python, virtual environment, pip, Jupyter Notebook, dan Git.
- [ ] Menyiapkan lingkungan kerja terisolasi untuk kurikulum ini.
- [ ] Menjalankan skrip dan notebook dari repository.

## Prasyarat

Python 3.10 atau lebih baru terpasang, dan terminal (PowerShell di Windows; Terminal di macOS/Linux).

## Pengantar dan intuisi

Proyek Python berbeda membutuhkan versi library berbeda. Jika semuanya dipasang
global, suatu saat satu proyek merusak proyek lain. **Virtual environment**
adalah folder berisi salinan Python dan library khusus untuk satu proyek.
Anggap seperti kotak peralatan terpisah untuk tiap proyek.

## Konsep

| Alat | Fungsi |
|---|---|
| Python | Bahasa dan interpreter |
| `venv` | Membuat lingkungan terisolasi (bawaan Python) |
| `pip` | Memasang library dari PyPI |
| `requirements.txt` | Daftar library yang dibutuhkan proyek |
| Jupyter Notebook | Dokumen interaktif: kode, hasil, dan teks bersama |
| Git | Pelacak riwayat perubahan berkas |

### Tiga berkas dependensi di repository ini

| Berkas | Isi | Kapan dipakai |
|---|---|---|
| `requirements.txt` | MkDocs dan theme | Menjalankan situs dokumentasi |
| `requirements-ml.txt` | NumPy, pandas, scikit-learn, Sastrawi, pytest, Jupyter, FastAPI | Level 1–5 dan 7 |
| `requirements-dl.txt` | PyTorch, Transformers (berat, opsional) | Level 6 |

!!! note "Jangan pasang semuanya sekaligus"
    Pasang `requirements-dl.txt` hanya saat mencapai Level 6. Unduhannya besar.

## Contoh kontekstual kebencanaan

Seorang relawan data memakai laptop yang sama untuk dua proyek: analisis
laporan banjir (butuh pandas versi 2.x) dan skrip lama yang membutuhkan
pandas 1.x. Dengan virtual environment terpisah, keduanya tetap berjalan.

## Langkah-langkah

### 1. Periksa Python

```bash
python --version
```

### 2. Buat dan aktifkan virtual environment

=== "Windows (PowerShell)"

    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

=== "macOS / Linux"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

Prompt biasanya berubah menjadi `(.venv)`. Folder `.venv/` sudah tercantum di `.gitignore` agar tidak ikut tersimpan di Git.

!!! warning "PowerShell menolak menjalankan skrip?"
    Jalankan sekali: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, lalu coba lagi.

### 3. Pasang dependensi

```bash
pip install --upgrade pip
pip install -r requirements.txt -r requirements-ml.txt
```

### 4. Jalankan Jupyter

```bash
jupyter lab
```

Browser akan terbuka. Buka berkas `.ipynb` di folder `examples/`.

### 5. Git dasar

```bash
git status            # lihat berkas yang berubah
git add examples/     # siapkan perubahan untuk disimpan
git commit -m "Menambah contoh Level 0"
git log --oneline     # riwayat commit
```

## Contoh kode

Memastikan perintah dijalankan dari lingkungan yang benar:

```python
import sys
print(sys.executable)
```

### Penjelasan kode

`sys.executable` menampilkan lokasi Python yang sedang dipakai. Bila lingkungan
aktif, lokasinya berada di dalam folder `.venv`.

### Output dan interpretasi

Contoh output pada Windows (jalur berbeda di setiap komputer):

```text
D:\...\materi-nlp\.venv\Scripts\python.exe
```

Jika yang tampil adalah Python global, lingkungan belum diaktifkan dan paket
akan terpasang di tempat yang salah.

## Kesalahan umum

- Lupa mengaktifkan `.venv` sebelum `pip install`.
- Menjalankan `jupyter` dari lingkungan lain sehingga notebook tidak menemukan library.
- Melakukan `git add .` yang ikut menyimpan `.venv/`, data pribadi, atau kredensial.
- Menulis jalur absolut (`C:\Users\...`) di notebook sehingga tidak jalan di komputer lain.

## Latihan mandiri

1. Buat `.venv` baru di folder percobaan, aktifkan, dan tampilkan `sys.executable`.
2. Pasang satu library kecil (mis. `pip install tqdm`) dan buktikan hanya ada di `.venv` tersebut.
3. Buat repository Git baru, buat satu berkas, lalu commit.

## Kuis singkat

**1.** Mengapa memakai virtual environment?

??? success "Jawaban"
    Mengisolasi dependensi tiap proyek agar versi tidak bertabrakan.

**2.** Folder mana yang tidak boleh di-commit?

??? success "Jawaban"
    `.venv/`, berkas data pribadi, model besar, dan kredensial.

## Ringkasan

Gunakan satu virtual environment per proyek, pasang dependensi dari berkas
`requirements*.txt`, jalankan Jupyter dari lingkungan yang sama, dan lacak
perubahan dengan Git tanpa menyertakan data sensitif.

## Referensi

- Dokumentasi Python: *venv* (<https://docs.python.org/3/library/venv.html>).
- Dokumentasi pip: <https://pip.pypa.io/>.
- Dokumentasi Jupyter: <https://docs.jupyter.org/>.
- Pro Git: <https://git-scm.com/book>.

## Materi selanjutnya

[Instalasi dan Verifikasi Lingkungan](verifikasi-lingkungan.md)
