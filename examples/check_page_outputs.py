"""Memeriksa bahwa blok keluaran di halaman materi sama dengan keluaran skrip yang sebenarnya.

Untuk setiap halaman di folder yang diberikan:
  1. cari skrip yang disertakan lewat `--8<-- "folder/skrip.py[:bagian]"`;
  2. jalankan skrip (cwd = examples/, UTF-8) dan kumpulkan keluarannya;
  3. untuk tiap blok kode berjudul `Output nyata` (persis), pastikan blok itu adalah
     potongan BERURUTAN dan UTUH dari keluaran salah satu skrip (spasi di ujung baris diabaikan).

Modul `nlp_hub/` (bukan skrip) dan skrip di folder `berat/` (PyTorch/Transformers) tidak pernah dijalankan oleh pemeriksa ini.
Blok dengan judul lain (mis. `Output nyata: tes gagal`) tidak diperiksa.
Menjalankan dari folder examples/:

    python check_page_outputs.py ../docs/level-2-fondasi-teks
"""
import os
import re
import subprocess
import sys
from pathlib import Path

RAIS = Path(__file__).resolve().parent
POLA_SNIPPET = re.compile(r'--8<--\s+"([^":]+\.py)(?::[^"]*)?"')
# Blok boleh berada di dalam admonition/tab (menjorok); indentasi dibuang sebelum dibandingkan.
POLA_BLOK = re.compile(r'^([ \t]*)```text title="Output nyata"\n(.*?)^\1```', re.S | re.M)


def jalankan(skrip):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    hasil = subprocess.run(
        [sys.executable, "-W", "ignore", str(RAIS / skrip)],
        capture_output=True, text=True, encoding="utf-8", env=env, cwd=RAIS,
    )
    if hasil.returncode != 0:
        raise RuntimeError(f"{skrip} gagal:\n{hasil.stderr[-800:]}")
    return [baris.rstrip() for baris in hasil.stdout.splitlines()]


def ada_berurutan(blok, keluaran):
    """True bila `blok` (daftar baris) muncul sebagai potongan berurutan di `keluaran`."""
    n = len(blok)
    return any(keluaran[i:i + n] == blok for i in range(len(keluaran) - n + 1))


def periksa(folder):
    gagal = diperiksa = 0
    cache = {}
    for md in sorted(Path(folder).glob("*.md")):
        teks = md.read_text(encoding="utf-8")
        blok = [(i, isi) for i, isi in POLA_BLOK.findall(teks)]
        if not blok:
            continue
        skrip = sorted(s for s in set(POLA_SNIPPET.findall(teks)) if not s.startswith(("tests/", "nlp_hub/")) and "/berat/" not in s)
        for s in skrip:
            if s not in cache:
                cache[s] = jalankan(s)
        for indent, isi in blok:
            baris = [(b[len(indent):] if b.startswith(indent) else b).rstrip() for b in isi.splitlines()]
            while baris and not baris[-1].strip():
                baris.pop()
            diperiksa += 1
            if not any(ada_berurutan(baris, cache[s]) for s in skrip):
                gagal += 1
                print(f"BLOK TIDAK COCOK di {md.name}: {ascii(baris[0])} ...({len(baris)} baris)")
    print(f"blok keluaran diperiksa: {diperiksa}, tidak cocok: {gagal}")
    return gagal


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "../docs/level-2-fondasi-teks"
    sys.exit(1 if periksa(folder) else 0)
