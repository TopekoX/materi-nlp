"""Memeriksa apakah lingkungan siap untuk eksperimen berat Level 6. Aman dijalankan tanpa torch/transformers."""
import importlib.util
import platform
import sys


# --8<-- [start:cek]
def versi_paket(nama_distribusi, nama_impor=None):
    """Versi paket bila terpasang, atau None.

    Nama untuk `pip` (distribusi) bisa berbeda dari nama untuk `import`: scikit-learn diimpor sebagai sklearn.
    find_spec memeriksa keberadaan tanpa mengimpor paket berat.
    """
    if importlib.util.find_spec(nama_impor or nama_distribusi) is None:
        return None
    import importlib.metadata as md
    return md.version(nama_distribusi)


print("Python:", sys.version.split()[0], "|", platform.system())
for paket, nama_impor in (("numpy", "numpy"), ("scikit-learn", "sklearn"), ("torch", "torch"),
                          ("transformers", "transformers"), ("fastapi", "fastapi")):
    print(f"{paket:13}:", versi_paket(paket, nama_impor) or "TIDAK terpasang")

if versi_paket("torch"):
    import torch
    print("CUDA tersedia:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))
else:
    print("torch belum terpasang: eksperimen di folder berat/ belum dapat dijalankan.")
    print("Pasang dengan: pip install -r requirements-dl.txt")
# --8<-- [end:cek]
