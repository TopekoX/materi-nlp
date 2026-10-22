"""Persentase kesepakatan dua anotator (data FIKTIF untuk demonstrasi rumus)."""

anotator_a = ["E", "N", "E", "N", "N", "N", "E", "U", "N", "U"]
anotator_b = ["E", "N", "E", "N", "N", "N", "E", "E", "N", "N"]

sama = sum(a == b for a, b in zip(anotator_a, anotator_b))
agreement = sama / len(anotator_a)
beda = [i + 1 for i, (a, b) in enumerate(zip(anotator_a, anotator_b)) if a != b]

print(f"Kesepakatan: {sama}/{len(anotator_a)} = {agreement:.0%}")
print("Contoh yang berbeda (nomor):", beda)
