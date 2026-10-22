"""Fungsi kecil yang diuji dengan assert."""


def hitung_kata(teks):
    return len(teks.split())


def tes_hitung_kata():
    assert hitung_kata("banjir naik") == 2
    assert hitung_kata("") == 0
    assert hitung_kata("  banjir   naik  ") == 2


if __name__ == "__main__":
    tes_hitung_kata()
    print("semua tes lolos")
    try:
        assert hitung_kata("a b") == 3, "seharusnya 2 kata"
    except AssertionError as e:
        print("AssertionError:", e)
