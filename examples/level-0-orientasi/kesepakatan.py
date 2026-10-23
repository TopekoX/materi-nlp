"""Kesepakatan dua anotator (data FIKTIF untuk demonstrasi rumus, bukan hasil anotasi nyata)."""
from collections import Counter

# --8<-- [start:data]
anotator_a = ["E", "N", "E", "N", "N", "N", "E", "U", "N", "U"]
anotator_b = ["E", "N", "E", "N", "N", "N", "E", "E", "N", "N"]
print(len(anotator_a), len(anotator_b))
# --8<-- [end:data]

# --8<-- [start:agreement]
sama = sum(a == b for a, b in zip(anotator_a, anotator_b))
agreement = sama / len(anotator_a)
beda = [i + 1 for i, (a, b) in enumerate(zip(anotator_a, anotator_b)) if a != b]

print(f"Kesepakatan: {sama}/{len(anotator_a)} = {agreement:.0%}")
print("Contoh yang berbeda (nomor):", beda)
# --8<-- [end:agreement]


# --8<-- [start:kappa]
def cohen_kappa(a, b):
    """kappa = (po - pe) / (1 - pe); po = kesepakatan teramati, pe = kesepakatan karena kebetulan."""
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[k] / n) * (cb[k] / n) for k in set(a) | set(b))
    return (po - pe) / (1 - pe)


print(f"kappa contoh: {cohen_kappa(anotator_a, anotator_b):.2f}")
# --8<-- [end:kappa]

# --8<-- [start:timpang]
a_timpang = ["N"] * 9 + ["E"]
b_timpang = ["N"] * 10
sama_t = sum(x == y for x, y in zip(a_timpang, b_timpang))
print(f"kesepakatan: {sama_t / 10:.0%}, kappa: {cohen_kappa(a_timpang, b_timpang):.2f}")
# --8<-- [end:timpang]
