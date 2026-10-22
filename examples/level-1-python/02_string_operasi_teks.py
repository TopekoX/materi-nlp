"""Operasi string yang sering dipakai dalam NLP."""
teks = "  TOLONG!! Banjir di Jl. Melati, air naik cepat  "

print(repr(teks.strip()))
print(teks.lower().strip())
print(teks.strip().split())
print("Jl. Melati" in teks)
print(teks.replace("!!", "!").strip())
print(len(teks), len(teks.strip()))
kata = ["banjir", "naik", "cepat"]
print(" ".join(kata))
nama = "Melati"
print(f"Lokasi: {nama!r}, panjang nama: {len(nama)}")
print("banjir".startswith("ban"), "banjir".endswith("jir"), "banjir".find("j"))
