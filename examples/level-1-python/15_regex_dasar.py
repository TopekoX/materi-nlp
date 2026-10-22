"""Dasar regex dengan modul re."""
import re

teks = "@bpbd Banjir di RT 05/RW 12 sejak 06.30, tinggi 120 cm https://t.co/abc #banjir"
print(re.findall(r"\d+", teks))
print(re.findall(r"#\w+", teks), re.findall(r"@\w+", teks))
print(re.sub(r"https?://\S+", "<URL>", teks))
print(re.search(r"RT (\d+)/RW (\d+)", teks).groups())
print(re.findall(r"\b\d{1,2}\.\d{2}\b", teks))
print(re.sub(r"\s+", " ", "banjir    naik \n cepat"))
print(re.match(r"banjir", "ada banjir"), bool(re.search(r"banjir", "ada banjir")))
pola = re.compile(r"(\w)\1{2,}")
print(pola.sub(r"\1", "TOLOOONG"))
