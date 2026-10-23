"""Fungsi kecil yang diuji dengan assert, dan pytest pada berkas sementara."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path


# --8<-- [start:fungsi]
def hitung_kata(teks):
    return len(teks.split())


def tes_hitung_kata():
    assert hitung_kata("banjir naik") == 2
    assert hitung_kata("") == 0
    assert hitung_kata("  banjir   naik  ") == 2
# --8<-- [end:fungsi]


# --8<-- [start:bug]
def rata_kata_salah(daftar):
    total = 0
    for teks in daftar:
        total += hitung_kata(teks)
    return total / len(daftar)


def rata_kata(daftar):
    if not daftar:
        raise ValueError("daftar tidak boleh kosong")
    return sum(hitung_kata(t) for t in daftar) / len(daftar)
# --8<-- [end:bug]


if __name__ == "__main__":
    # --8<-- [start:jalan]
    tes_hitung_kata()
    print("semua tes lolos")
    try:
        assert hitung_kata("a b") == 3, "seharusnya 2 kata"
    except AssertionError as e:
        print("AssertionError:", e)
    # --8<-- [end:jalan]

    # --8<-- [start:hunting]
    print(rata_kata(["banjir naik", "gempa"]))
    try:
        rata_kata_salah([])
    except ZeroDivisionError as e:
        print("ZeroDivisionError:", e)
    try:
        rata_kata([])
    except ValueError as e:
        print("ValueError:", e)
    # --8<-- [end:hunting]

    # --8<-- [start:print_debug]
    teks = "tolong,  air naik"
    print(repr(teks), teks.split(), teks.split(" "))
    # --8<-- [end:print_debug]

    # --8<-- [start:pytest]
    isi = '''
def hitung_kata(teks):
    return len(teks.split())

def test_dua_kata():
    assert hitung_kata("banjir naik") == 2

def test_kosong():
    assert hitung_kata("") == 1   # sengaja salah
'''
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "test_contoh.py").write_text(isi, encoding="utf-8")
        hasil = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", tmp],
                               capture_output=True, text=True, encoding="utf-8")
    ringkas = re.search(r"(\d+ failed, \d+ passed|\d+ passed)", hasil.stdout)
    print("ringkasan pytest:", ringkas.group(1))
    print([b.strip() for b in hasil.stdout.splitlines() if b.startswith("E ")][:2])
    # --8<-- [end:pytest]
