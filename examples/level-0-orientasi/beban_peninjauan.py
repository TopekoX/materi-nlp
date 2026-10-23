"""Beban peninjauan manusia pada tiga skenario FIKTIF (ASUMSI, bukan hasil pengukuran)."""

# --8<-- [start:asumsi]
PESAN_PER_JAM = 1000          # ASUMSI
PREVALENSI = 0.02             # ASUMSI: 2% pesan benar-benar darurat
KAPASITAS_PER_JAM = 5 * 60    # ASUMSI: 5 petugas x 60 pesan/jam
SKENARIO = {
    "A (recall tinggi, alarm palsu sedang)": (0.90, 0.05),
    "B (alarm palsu sangat sedikit, banyak terlewat)": (0.70, 0.01),
    "C (hampir tak ada yang terlewat, banyak alarm palsu)": (0.95, 0.20),
}
# --8<-- [end:asumsi]

# --8<-- [start:hitung]
darurat = PESAN_PER_JAM * PREVALENSI
bukan = PESAN_PER_JAM - darurat
print(f"pesan darurat/jam = {darurat:.0f}, bukan darurat = {bukan:.0f}, kapasitas peninjau = {KAPASITAS_PER_JAM}/jam")
for nama, (recall, fpr) in SKENARIO.items():
    tp = darurat * recall
    fn = darurat - tp
    fp = bukan * fpr
    ditandai = tp + fp
    print(f"{nama}")
    print(f"   ditemukan={tp:.0f}  terlewat={fn:.0f}  alarm palsu={fp:.0f}  perlu ditinjau={ditandai:.0f}  muat kapasitas={ditandai <= KAPASITAS_PER_JAM}")
# --8<-- [end:hitung]
