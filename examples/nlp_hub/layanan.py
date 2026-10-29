"""Inti layanan inferensi (Level 7): menyimpan/memuat artefak dengan metadata dan memberi skor pada teks.

Tidak bergantung pada FastAPI sehingga dapat diuji dan dipakai dari skrip biasa. Model rujukan adalah
Linear SVM: keluarannya adalah SKOR KEPUTUSAN, BUKAN probabilitas. Skor 0 adalah batas bawaan model
dan belum divalidasi sebagai ambang operasional.
"""
import hashlib
import json
import platform
import sys
from pathlib import Path

import joblib
import sklearn

NAMA_BERKAS_MODEL = "model.joblib"
NAMA_BERKAS_META = "model.json"
BATAS_PANJANG_TEKS = 1000
BATAS_BATCH = 100
CATATAN_WAJIB = (
    "Keluaran ini adalah skor model pada data sintetis, bukan penentuan keadaan darurat. "
    "Verifikasi manusia diperlukan sebelum tindakan apa pun."
)


class ArtefakTidakValid(Exception):
    """Berkas model hilang, metadata rusak, atau checksum tidak cocok."""


def hash_berkas(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def simpan_artefak(model, folder, versi, ambang=0.0, margin_ragu=0.3, catatan=""):
    """Menyimpan model dan metadata (versi, library, checksum, ambang) ke `folder`. Mengembalikan metadata."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    berkas = folder / NAMA_BERKAS_MODEL
    joblib.dump(model, berkas)
    meta = {
        "model_version": versi,
        "jenis_keluaran": "skor_keputusan_svm",           # BUKAN probabilitas
        "ambang": ambang,
        "ambang_tervalidasi": False,
        "margin_ragu": margin_ragu,
        "scikit_learn": sklearn.__version__,
        "python": sys.version.split()[0],
        "platform": platform.system(),
        "sha256": hash_berkas(berkas),
        "data": "dataset SINTETIS; bukan untuk penggunaan operasional",
        "catatan": catatan,
    }
    (folder / NAMA_BERKAS_META).write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return meta


def muat_artefak(folder):
    """Memuat (model, metadata) setelah memeriksa checksum. SELALU memeriksa checksum sebelum joblib.load.

    joblib/pickle dapat menjalankan kode saat dimuat; jangan memuat berkas dari sumber yang tidak dipercaya.
    Checksum hanya melindungi dari berkas yang berubah, bukan dari berkas yang sejak awal berbahaya.
    """
    folder = Path(folder)
    berkas, meta_berkas = folder / NAMA_BERKAS_MODEL, folder / NAMA_BERKAS_META
    if not berkas.exists() or not meta_berkas.exists():
        raise ArtefakTidakValid(f"model.joblib atau model.json tidak ada di {folder}")
    try:
        meta = json.loads(meta_berkas.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ArtefakTidakValid(f"model.json bukan JSON yang valid: {e}") from e
    if meta.get("sha256") != hash_berkas(berkas):
        raise ArtefakTidakValid("checksum model.joblib tidak cocok dengan model.json (berkas berubah?)")
    return joblib.load(berkas), meta


def hash_teks(teks):
    """Sidik jari 12 karakter untuk log/riwayat; teks asli tidak perlu disimpan."""
    return hashlib.sha256(teks.encode("utf-8")).hexdigest()[:12]


class Penilai:
    """Membungkus model + metadata dan menghasilkan keluaran terstruktur untuk tiap teks."""

    def __init__(self, model, meta, ambang=None):
        if not hasattr(model, "decision_function"):
            raise TypeError("model harus punya decision_function (Linear SVM atau sejenisnya)")
        self.model, self.meta = model, meta
        self.ambang = float(meta["ambang"] if ambang is None else ambang)
        self.margin = float(meta.get("margin_ragu", 0.3))

    def nilai(self, daftar_teks):
        """Daftar dict {skor, label, ambang, zona_ragu} sesuai urutan masukan."""
        if isinstance(daftar_teks, str):
            raise TypeError("masukan harus daftar teks, bukan satu string")
        if not daftar_teks:
            return []
        for t in daftar_teks:
            if not isinstance(t, str) or not t.strip():
                raise ValueError("setiap teks harus string tidak kosong")
            if len(t) > BATAS_PANJANG_TEKS:
                raise ValueError(f"teks melebihi {BATAS_PANJANG_TEKS} karakter")
        skor = self.model.decision_function(daftar_teks)
        return [
            {
                "skor": round(float(s), 4),
                "label": "Emergency" if s >= self.ambang else "Non-Emergency",
                "ambang": self.ambang,
                "zona_ragu": bool(abs(s - self.ambang) <= self.margin),
            }
            for s in skor
        ]


def pastikan_artefak(folder, versi="svm-tfidf-sintetis-0.1"):
    """Membuat artefak bawaan (Linear SVM rujukan) bila `folder` belum berisi model.joblib. Mengembalikan metadata."""
    folder = Path(folder)
    if (folder / NAMA_BERKAS_MODEL).exists() and (folder / NAMA_BERKAS_META).exists():
        return json.loads((folder / NAMA_BERKAS_META).read_text(encoding="utf-8"))
    from .proyek import model_rujukan, siapkan      # impor di dalam fungsi: layanan tidak butuh data saat hanya memuat model

    return simpan_artefak(model_rujukan(siapkan()), folder, versi,
                          catatan="Linear SVM rujukan Level 5; ambang 0 = batas bawaan, BELUM divalidasi.")
