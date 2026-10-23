"""Riwayat prediksi di SQLite (Level 7). Secara bawaan TIDAK menyimpan teks, hanya sidik jari, panjang, skor, dan label."""
import sqlite3
from datetime import datetime, timezone

SKEMA = """
CREATE TABLE IF NOT EXISTS prediksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    waktu TEXT NOT NULL,
    teks_hash TEXT NOT NULL,
    panjang INTEGER NOT NULL,
    skor REAL NOT NULL,
    label TEXT NOT NULL,
    zona_ragu INTEGER NOT NULL,
    versi_model TEXT NOT NULL,
    teks TEXT
)
"""


class Riwayat:
    def __init__(self, path=":memory:", simpan_teks=False):
        # check_same_thread=False: FastAPI dapat memanggil dari thread berbeda; akses diserialkan oleh SQLite.
        self.sambungan = sqlite3.connect(path, check_same_thread=False)
        self.sambungan.execute(SKEMA)
        self.simpan_teks = simpan_teks

    def catat(self, teks, teks_hash, hasil, versi_model):
        self.sambungan.execute(
            "INSERT INTO prediksi (waktu, teks_hash, panjang, skor, label, zona_ragu, versi_model, teks) VALUES (?,?,?,?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(timespec="seconds"), teks_hash, len(teks), hasil["skor"], hasil["label"],
             int(hasil["zona_ragu"]), versi_model, teks if self.simpan_teks else None),
        )
        self.sambungan.commit()

    def ringkasan(self):
        """Hitungan total, per label, jumlah zona ragu, dan skor rata-rata. Semua dihitung di SQL."""
        total, ragu, rata = self.sambungan.execute(
            "SELECT COUNT(*), COALESCE(SUM(zona_ragu), 0), AVG(skor) FROM prediksi").fetchone()
        per_label = dict(self.sambungan.execute("SELECT label, COUNT(*) FROM prediksi GROUP BY label").fetchall())
        return {"total": total, "per_label": per_label, "zona_ragu": ragu,
                "skor_rata_rata": None if rata is None else round(rata, 4)}

    def terbaru(self, n=20):
        baris = self.sambungan.execute(
            "SELECT waktu, teks_hash, panjang, skor, label, zona_ragu, versi_model FROM prediksi ORDER BY id DESC LIMIT ?",
            (int(n),)).fetchall()
        kunci = ("waktu", "teks_hash", "panjang", "skor", "label", "zona_ragu", "versi_model")
        return [dict(zip(kunci, b)) for b in baris]
