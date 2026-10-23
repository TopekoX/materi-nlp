"""REST API FastAPI untuk klasifikasi Emergency/Non-Emergency (Level 7).

Jalankan dari folder examples/ (artefak harus dibuat dulu, lihat level-7-deployment/README.md):

    python -m uvicorn nlp_hub.api:buat_app --factory --port 8000

Pengaturan lewat variabel lingkungan: NLP_HUB_ARTEFAK, NLP_HUB_AMBANG, NLP_HUB_DB, NLP_HUB_SIMPAN_TEKS.
"""
import html
import logging
import os
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from .layanan import (
    BATAS_BATCH, BATAS_PANJANG_TEKS, CATATAN_WAJIB, ArtefakTidakValid, Penilai, hash_teks, muat_artefak,
)
from .riwayat import Riwayat

log = logging.getLogger("nlp_hub.api")
ARTEFAK_BAWAAN = Path(__file__).resolve().parents[1] / "level-7-deployment" / "artefak"


# --8<-- [start:skema]
class PermintaanTeks(BaseModel):
    teks: str = Field(min_length=1, max_length=BATAS_PANJANG_TEKS, description="Teks postingan yang dinilai.")


class PermintaanBatch(BaseModel):
    teks: list[str] = Field(min_length=1, max_length=BATAS_BATCH)


class HasilPrediksi(BaseModel):
    skor: float = Field(description="Skor keputusan SVM. BUKAN probabilitas.")
    label: str
    ambang: float
    zona_ragu: bool = Field(description="True bila skor dekat ambang; prioritaskan tinjauan manusia.")
    versi_model: str
    waktu_ms: float = Field(description="Waktu pemrosesan model dalam milidetik; pada batch: rata-rata per teks.")
    catatan: str = CATATAN_WAJIB


class HasilBatch(BaseModel):
    hasil: list[HasilPrediksi]
# --8<-- [end:skema]


def buat_app(folder_artefak=None, path_db=None, ambang=None, simpan_teks=None):
    """Membuat aplikasi. Argumen None dibaca dari variabel lingkungan, lalu dari nilai bawaan."""
    folder = Path(folder_artefak or os.environ.get("NLP_HUB_ARTEFAK") or ARTEFAK_BAWAAN)
    env_ambang = os.environ.get("NLP_HUB_AMBANG")
    ambang = ambang if ambang is not None else (float(env_ambang) if env_ambang else None)
    simpan = simpan_teks if simpan_teks is not None else os.environ.get("NLP_HUB_SIMPAN_TEKS") == "1"
    # --8<-- [start:mulai]
    model, meta = muat_artefak(folder)               # gagal cepat saat start bila artefak tidak valid
    penilai = Penilai(model, meta, ambang)
    riwayat = Riwayat(path_db or os.environ.get("NLP_HUB_DB") or ":memory:", simpan_teks=simpan)
    app = FastAPI(title="NLP Learning Hub: klasifikasi Emergency", version=meta["model_version"],
                  description="Demo pendidikan pada data SINTETIS. Bukan sistem penentuan keadaan darurat.")
    # --8<-- [end:mulai]

    # --8<-- [start:galat]
    @app.exception_handler(Exception)
    async def galat_tak_terduga(request: Request, exc: Exception):
        id_galat = uuid.uuid4().hex[:8]
        log.exception("galat tak terduga id=%s path=%s", id_galat, request.url.path)   # trace lengkap hanya di log server
        return JSONResponse(status_code=500, content={"detail": "Terjadi kesalahan internal.", "id_galat": id_galat})

    def _jalankan(daftar):
        """Mengembalikan (hasil, milidetik per teks). Waktu hanya mencakup pemanggilan model."""
        mulai = time.perf_counter()
        try:
            hasil = penilai.nilai(daftar)
            return hasil, (time.perf_counter() - mulai) * 1000 / len(daftar)
        except ValueError as e:                       # masukan tidak valid yang lolos pydantic (mis. hanya spasi)
            raise HTTPException(status_code=422, detail=str(e)) from e

    # --8<-- [end:galat]

    # --8<-- [start:bentuk]
    def _bentuk(teks, h, ms):
        riwayat.catat(teks, hash_teks(teks), h, meta["model_version"])
        log.info("prediksi hash=%s panjang=%d skor=%.3f label=%s", hash_teks(teks), len(teks), h["skor"], h["label"])
        return HasilPrediksi(**h, versi_model=meta["model_version"], waktu_ms=round(ms, 3))
    # --8<-- [end:bentuk]

    # --8<-- [start:endpoint]
    @app.get("/kesehatan")
    def kesehatan():
        return {"status": "ok", "versi_model": meta["model_version"]}

    @app.get("/model/info")
    def info():
        return {**meta, "ambang_dipakai": penilai.ambang, "catatan_wajib": CATATAN_WAJIB}

    @app.post("/prediksi", response_model=HasilPrediksi)
    def prediksi(p: PermintaanTeks):
        hasil, ms = _jalankan([p.teks])
        return _bentuk(p.teks, hasil[0], ms)

    @app.post("/prediksi/batch", response_model=HasilBatch)
    def prediksi_batch(p: PermintaanBatch):
        hasil, ms = _jalankan(p.teks)                  # satu panggilan model untuk seluruh batch
        return HasilBatch(hasil=[_bentuk(t, h, ms) for t, h in zip(p.teks, hasil)])

    # --8<-- [end:endpoint]

    # --8<-- [start:riwayat]
    @app.get("/riwayat/ringkasan")
    def ringkasan():
        return riwayat.ringkasan()

    @app.get("/riwayat/terbaru")
    def terbaru(n: int = 20):
        return riwayat.terbaru(min(max(n, 1), 200))

    # --8<-- [end:riwayat]

    # --8<-- [start:dasbor]
    @app.get("/dasbor", response_class=HTMLResponse)
    def dasbor():
        r = riwayat.ringkasan()
        baris = "".join(
            f"<tr><td>{html.escape(b['waktu'])}</td><td>{html.escape(b['teks_hash'])}</td>"
            f"<td>{b['skor']}</td><td>{html.escape(b['label'])}</td><td>{'ya' if b['zona_ragu'] else ''}</td></tr>"
            for b in riwayat.terbaru(20))
        return (
            "<!doctype html><meta charset='utf-8'><title>Riwayat prediksi</title>"
            f"<h1>Riwayat prediksi</h1><p>{html.escape(CATATAN_WAJIB)}</p>"
            f"<p>Total: {r['total']} | zona ragu: {r['zona_ragu']} | per label: {html.escape(str(r['per_label']))}</p>"
            "<table border=1 cellpadding=4><tr><th>waktu (UTC)</th><th>sidik jari teks</th><th>skor</th><th>label</th><th>ragu</th></tr>"
            f"{baris}</table>"
        )

    # --8<-- [end:dasbor]

    app.state.penilai, app.state.riwayat = penilai, riwayat
    return app
