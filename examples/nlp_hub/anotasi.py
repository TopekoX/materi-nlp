"""Aturan anotasi label Emergency / Non-Emergency sebagai fungsi yang dapat diperiksa (Tahap A proyek)."""


# --8<-- [start:aturan]
def label_menurut_aturan(kejadian_berlangsung, melaporkan_atau_meminta_bantuan, waktu_dan_ancaman_jelas=True):
    """Menerapkan definisi operasional dari tiga jawaban ya/tidak yang diberikan anotator.

    Emergency      : kejadian berlangsung/baru terjadi DAN postingan melaporkannya atau meminta bantuan.
    uncertain      : kedua syarat tampak terpenuhi tetapi waktu atau ancamannya tidak jelas (ditinjau bersama).
    Non-Emergency  : selain itu.
    """
    if not (kejadian_berlangsung and melaporkan_atau_meminta_bantuan):
        return "Non-Emergency"
    return "Emergency" if waktu_dan_ancaman_jelas else "uncertain"
# --8<-- [end:aturan]
