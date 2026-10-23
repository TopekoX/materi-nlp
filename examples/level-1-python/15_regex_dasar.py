"""Dasar regex dengan modul re."""
import re

teks = "@bpbd Banjir di RT 05/RW 12 sejak 06.30, tinggi 120 cm https://t.co/abc #banjir"

# --8<-- [start:findall]
print(re.findall(r"\d+", teks))
print(re.findall(r"#\w+", teks), re.findall(r"@\w+", teks))
# --8<-- [end:findall]

# --8<-- [start:sub]
print(re.sub(r"https?://\S+", "<URL>", teks))
print(re.sub(r"\s+", " ", "banjir    naik \n cepat"))
# --8<-- [end:sub]

# --8<-- [start:grup]
m = re.search(r"RT (\d+)/RW (\d+)", teks)
print(m.groups(), m.group(0), m.start())
print(re.findall(r"\b\d{1,2}\.\d{2}\b", teks))
# --8<-- [end:grup]

# --8<-- [start:match]
print(re.match(r"banjir", "ada banjir"), bool(re.search(r"banjir", "ada banjir")))
hasil = re.search(r"gempa", teks)
print(hasil)
try:
    hasil.group(0)
except AttributeError as e:
    print("AttributeError:", e)
# --8<-- [end:match]

# --8<-- [start:flag]
print(re.findall(r"banjir", "Banjir banjir BANJIR"))
print(re.findall(r"banjir", "Banjir banjir BANJIR", flags=re.IGNORECASE))
# --8<-- [end:flag]

# --8<-- [start:serakah]
html = "<b>satu</b> dan <b>dua</b>"
print(re.findall(r"<b>.*</b>", html))
print(re.findall(r"<b>.*?</b>", html))
# --8<-- [end:serakah]

# --8<-- [start:compile]
pola = re.compile(r"(\w)\1{2,}")
print(pola.sub(r"\1", "TOLOOONG"))
print(pola.sub(r"\1", "Rp1000000"))
# --8<-- [end:compile]

# --8<-- [start:galat]
try:
    re.compile(r"(banjir")
except re.error as e:
    print("re.error:", e)
print(len("\b"), len(r"\b"))
# --8<-- [end:galat]
