"""Mengenali ciri teks media sosial dengan regex sederhana (ILUSTRATIF)."""
import re

POLA = {
    "url": re.compile(r"https?://\S+"),
    "mention": re.compile(r"@\w+"),
    "hashtag": re.compile(r"#\w+"),
    "emoji": re.compile("[\U0001F300-\U0001FAFF☀-➿]"),
    "huruf_berulang": re.compile(r"(\w)\1{2,}"),
}

CONTOH = "@bpbd_kota TOLOOONG banjir naik cepet bgt di Jl. Melati 🙏 #banjir https://t.co/xyz123"


def ekstrak_ciri(teks):
    return {nama: [m.group(0) for m in pola.finditer(teks)] for nama, pola in POLA.items()}


if __name__ == "__main__":
    print(CONTOH)
    for nama, hasil in ekstrak_ciri(CONTOH).items():
        print(f"{nama:15}: {hasil}")
