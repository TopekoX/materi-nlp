"""Audit browser (Tahap 8): memuat tiap halaman situs hasil `mkdocs build` di Edge (Playwright) dan memeriksa
rumus MathJax, diagram Mermaid, galat konsol, permintaan gagal, dan halaman yang meluap horizontal.

Syarat (di luar requirements*.txt; hanya untuk audit): `pip install playwright`, Microsoft Edge terpasang,
`mkdocs build` sudah dijalankan, dan ada jaringan (MathJax dimuat dari CDN).
Pakai: python examples/audit/audit_browser.py [potongan-jalur-halaman]

Halaman examples/mermaid sengaja memuat diagram rusak (demonstrasi template) sehingga selalu dilaporkan.
Material memakai shadow DOM tertutup untuk Mermaid; keberhasilan render didekati dengan tinggi elemen > 40 px.
"""
import functools
import http.server
import re
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

SITE = Path(__file__).resolve().parents[2] / "site"
PORT = 8801

_handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE))
_handler.log_message = lambda *a, **k: None
_server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), _handler)
threading.Thread(target=_server.serve_forever, daemon=True).start()

halaman = sorted(p.relative_to(SITE).as_posix() for p in SITE.rglob("index.html") if "assets" not in p.parts)
pilih = [h for h in halaman if len(sys.argv) < 2 or sys.argv[1] in h]

JS = """() => {
  const mm = [...document.querySelectorAll('.mermaid')];
  const svgOk = mm.filter(m => m.getBoundingClientRect().height > 40).length;
  const mjx = document.querySelectorAll('mjx-container').length;
  const mjxErr = document.querySelectorAll('mjx-merror, merror').length;
  const lebar = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  return {mm: mm.length, svgOk, mjx, mjxErr, lebar};
}"""

total = dict(halaman=0, rumus=0, mjx=0, mermaid=0, mermaid_ok=0)
masalah = []
with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    for viewport in ({"width": 1280, "height": 900}, {"width": 390, "height": 800}):
        for rel in pilih:
            pg = browser.new_page(viewport=viewport)
            konsol, gagal = [], []
            pg.on("console", lambda m, k=konsol: k.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e, k=konsol: k.append(str(e)))
            pg.on("requestfailed", lambda r, g=gagal: g.append(r.url))
            pg.goto(f"http://127.0.0.1:{PORT}/" + rel.replace("index.html", ""), wait_until="networkidle", timeout=90000)
            pg.wait_for_timeout(1500)
            h = pg.evaluate(JS)
            n_rumus = len(re.findall(r'class="arithmatex"', (SITE / rel).read_text(encoding="utf-8")))
            if viewport["width"] == 1280:
                total["halaman"] += 1
                total["rumus"] += n_rumus
                total["mjx"] += h["mjx"]
                total["mermaid"] += h["mm"]
                total["mermaid_ok"] += h["svgOk"]
            m = []
            if n_rumus and h["mjx"] == 0:
                m.append(f"MathJax tidak merender ({n_rumus} rumus)")
            if h["mjxErr"]:
                m.append(f"{h['mjxErr']} galat MathJax")
            if h["mm"] and h["svgOk"] < h["mm"]:
                m.append(f"mermaid {h['svgOk']}/{h['mm']} (diagram rusak atau tidak dirender)")
            if h["lebar"] > 4:
                m.append(f"halaman meluap horizontal {h['lebar']}px")
            konsol = [k for k in konsol if "favicon" not in k.lower()]
            if konsol:
                m.append("konsol: " + " | ".join(konsol)[:160])
            if gagal:
                m.append("permintaan gagal: " + ", ".join(sorted(set(gagal)))[:160])
            if m:
                masalah.append((f"{viewport['width']}px", rel, m))
            pg.close()
    browser.close()
print(total)
for lebar, rel, m in masalah:
    print("MASALAH", lebar, rel, m)
print("temuan:", len(masalah))
