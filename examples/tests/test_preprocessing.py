"""Uji fungsi preprocessing. Setiap fungsi diuji sendiri, lalu pipeline gabungannya."""
import pytest

from nlp_hub import preprocessing as pp
from nlp_hub.preprocessing import KonfigurasiPraproses, PraprosesTeks


# ---- unicode & huruf
def test_normalisasi_unicode_menyatukan_huruf_bergaya():
    assert pp.normalisasi_unicode("𝐁𝐀𝐍𝐉𝐈𝐑") == "BANJIR"


def test_normalisasi_unicode_membuang_karakter_tak_terlihat():
    assert pp.normalisasi_unicode("ban​jir") == "banjir"


def test_case_folding():
    assert pp.case_folding("TOLONG Banjir") == "tolong banjir"


# ---- url, mention, hashtag
def test_ganti_url():
    assert pp.ganti_url("lihat https://contoh.example/1 sekarang").split() == ["lihat", "tok_url", "sekarang"]


def test_ganti_mention():
    assert "tok_mention" in pp.ganti_mention("halo @bpbd_contoh tolong")
    assert "@" not in pp.ganti_mention("halo @bpbd_contoh tolong")


@pytest.mark.parametrize(
    "mode,diharapkan",
    [("kata", "Siaga Bencana"), ("hapus", ""), ("pertahankan", "#SiagaBencana")],
)
def test_proses_hashtag(mode, diharapkan):
    assert " ".join(pp.proses_hashtag("#SiagaBencana", mode).split()) == diharapkan


def test_proses_hashtag_mode_salah():
    with pytest.raises(ValueError):
        pp.proses_hashtag("#a", "acak")


# ---- emoji
def test_emoji_ke_kata_dan_emoji_tak_dikenal():
    assert "emo_doa" in pp.proses_emoji("tolong 🙏", "kata")
    assert "emo_lain" in pp.proses_emoji("halo 🦖", "kata")


def test_emoji_hapus():
    assert "🙏" not in pp.proses_emoji("tolong 🙏", "hapus")


def test_emotikon_terpanjang_didahulukan():
    assert pp.proses_emoji(":'(", "kata").split() == ["emo_menangis"]


# ---- huruf berulang & informal
# --8<-- [start:berparameter]
@pytest.mark.parametrize(
    "masuk,keluar",
    [("tolooong", "tolong"), ("banjiiir", "banjir"), ("1000", "1000"), ("saat", "saat"), ("saaat", "sat")],
)
def test_kurangi_huruf_berulang(masuk, keluar):
    assert pp.kurangi_huruf_berulang(masuk) == keluar
# --8<-- [end:berparameter]


def test_normalisasi_informal():
    assert pp.normalisasi_informal("gak") == "tidak"
    assert pp.normalisasi_informal("banjir") == "banjir"


def test_koreksi_typo_memperbaiki_dan_tidak_menyentuh_kata_benar():
    assert pp.koreksi_typo("bnjir") == "banjir"  # huruf hilang
    assert pp.koreksi_typo("banjirr") == "banjir"  # huruf berlebih
    assert pp.koreksi_typo("banjir") == "banjir"
    assert pp.koreksi_typo("pun") == "pun"  # terlalu pendek


def test_koreksi_typo_kompromi_batas():
    # Kemiripan banjri~banjir dan banjar~banjir sama-sama 0,833.
    assert pp.koreksi_typo("banjri") == "banjri"  # batas 0,85: tertukar tidak terkoreksi
    assert pp.koreksi_typo("banjri", batas=0.8) == "banjir"
    assert pp.koreksi_typo("banjar", batas=0.8) == "banjir"  # kata sah ikut "dikoreksi" (salah)


# ---- angka, waktu, lokasi
def test_normalisasi_waktu():
    assert "tok_waktu" in pp.normalisasi_waktu("gempa pukul 08.12 tadi")
    assert "08" not in pp.normalisasi_waktu("gempa pukul 08.12 tadi")


def test_normalisasi_angka_tidak_menyentuh_huruf():
    hasil = pp.normalisasi_angka("setinggi 50 cm dan 1,5 m")
    assert hasil.split() == ["setinggi", "tok_angka", "cm", "dan", "tok_angka", "m"]


def test_normalisasi_lokasi_jalan_rt_dan_gazetteer():
    assert pp.normalisasi_lokasi("banjir di jl. melati rt 08").split() == ["banjir", "di", "tok_lokasi"]
    assert "sukamaju" not in pp.normalisasi_lokasi("kelurahan sukamaju terendam")


def test_normalisasi_lokasi_tidak_menelan_kota_ini():
    assert pp.normalisasi_lokasi("di kota ini aman") == "di kota ini aman"


# ---- kalimat & token
def test_pisah_kalimat_melindungi_singkatan():
    assert pp.pisah_kalimat("Banjir di Jl. Melati No. 5. Air naik! Tolong?") == [
        "Banjir di Jl. Melati No. 5.", "Air naik!", "Tolong?",
    ]


def test_tokenisasi_menjaga_kata_ulang_berhubung():
    assert pp.tokenisasi("hati-hati banjir") == ["hati-hati", "banjir"]


# ---- negasi, stopword, stem
def test_tandai_negasi_jendela_satu():
    assert pp.tandai_negasi(["tidak", "ada", "korban"]) == ["tidak", "neg_ada", "korban"]


def test_tandai_negasi_jendela_dua():
    assert pp.tandai_negasi(["belum", "ada", "korban", "jiwa"], jendela=2) == [
        "belum", "neg_ada", "neg_korban", "jiwa",
    ]


def test_stopword_konservatif_tidak_membuang_negasi_dan_permintaan():
    hasil = pp.hapus_stopword(["tolong", "air", "yang", "tidak", "surut", "di", "rumah"])
    assert hasil == ["tolong", "air", "tidak", "surut", "rumah"]


@pytest.mark.parametrize("kata,dasar", [("kebanjiran", "banjir"), ("pengungsian", "ungsi"), ("korban", "korban")])
def test_stem_kata(kata, dasar):
    assert pp.stem_kata(kata) == dasar


def test_stem_token_menjaga_token_khusus():
    assert pp.stem_token(["tok_url", "neg_kebanjiran", "emo_doa"]) == ["tok_url", "neg_banjir", "emo_doa"]


# ---- pipeline
def test_praproses_dasar():
    teks = "@bpbd_contoh TOLOOONG banjir bgt 🙏 #SiagaBencana https://contoh.example/1"
    assert pp.praproses(teks) == "tok_mention tolong banjir sangat emo_doa siaga bencana tok_url"


# --8<-- [start:galat]
def test_praproses_menolak_bukan_string():
    with pytest.raises(TypeError, match="harus str"):
        pp.praproses(None)
# --8<-- [end:galat]


def test_praproses_string_kosong():
    assert pp.praproses("") == ""
    assert pp.praproses("   ") == ""


# --8<-- [start:idempoten]
def test_praproses_idempoten_pada_konfigurasi_dasar():
    teks = "TOLOOONG banjir naik cepet bgt di Jl. Melati"
    sekali = pp.praproses(teks)
    assert pp.praproses(sekali) == sekali
# --8<-- [end:idempoten]


def test_praproses_tidak_mengubah_masukan():
    teks = "Banjir!"
    pp.praproses(teks)
    assert teks == "Banjir!"


def test_tanda_seru_menjadi_token_bila_diminta():
    assert pp.praproses("banjir!", KonfigurasiPraproses(tanda_seru=True)).endswith("tok_seru")
    assert "tok_seru" not in pp.praproses("banjir!")


def test_konfigurasi_lengkap():
    k = KonfigurasiPraproses(angka_waktu_lokasi=True, negasi=True, stopword=True, stem=True)
    hasil = pp.praproses("Tidak ada listrik di Jl. Melati RT 08 pukul 08.12", k)
    assert hasil == "tidak neg_ada listrik tok_lokasi tok_waktu"


# ---- pembungkus scikit-learn
def test_transformer_stateless_dan_dapat_di_clone():
    from sklearn.base import clone

    t = PraprosesTeks(KonfigurasiPraproses(stem=True))
    assert clone(t).konfigurasi == t.konfigurasi
    assert t.fit(["a"]).transform(["BANJIR bgt"]) == ["banjir sangat"]


# --8<-- [start:tanpa_state]
def test_transformer_tidak_belajar_dari_data():
    t = PraprosesTeks()
    a = t.fit(["banjir"]).transform(["Gempa kuat"])
    b = t.fit(["teks lain sama sekali", "dan lagi"]).transform(["Gempa kuat"])
    assert a == b
# --8<-- [end:tanpa_state]


# ---- stopword bawaan Sastrawi
def test_stopword_sastrawi_memuat_kata_yang_berbahaya_untuk_tugas_ini():
    daftar = pp.stopwords_sastrawi()
    assert {"tidak", "belum", "tolong"} <= daftar


def test_konfigurasi_stopword_sastrawi_membuang_negasi_dan_tolong():
    hasil = pp.praproses("tolong air tidak surut", KonfigurasiPraproses(stopword="sastrawi"))
    assert "tolong" not in hasil.split() and "tidak" not in hasil.split()
    assert pp.praproses("tolong air tidak surut", KonfigurasiPraproses(stopword=True)) == "tolong air tidak surut"


def test_emoji_sos_di_blok_berbeda_tetap_terdeteksi():
    # U+1F198 berada di luar blok 1F300-1FAFF; pola awal melewatkannya.
    assert pp.proses_emoji("🆘 tolong", "kata").split() == ["emo_sos", "tolong"]


@pytest.mark.parametrize(
    "masuk,keluar",
    [
        ("dana 50.000 rupiah", "dana tok_angka rupiah"),
        ("dana Rp50.000", "dana Rp50.000"),  # menempel pada huruf: tidak disentuh
        ("gempa m4,1", "gempa m4,1"),
        ("1,5 m", "tok_angka m"),
    ],
)
def test_normalisasi_angka_kasus_tepi(masuk, keluar):
    assert " ".join(pp.normalisasi_angka(masuk).split()) == keluar


def test_waktu_salah_baca_desimal_dua_digit_didokumentasikan():
    # Kelemahan yang diketahui: 1.50 m terbaca sebagai waktu (pukul 1.50).
    assert "tok_waktu" in pp.normalisasi_waktu("air setinggi 1.50 m")


def test_tidak_ada_teks_kosong_pada_dataset():
    from nlp_hub.data import muat_dataset

    assert all(pp.praproses(t).strip() for t in muat_dataset()["text"])
