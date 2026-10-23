"""Dasar NumPy."""
import numpy as np

# --8<-- [start:array]
panjang = np.array([6, 5, 4, 3])
print(panjang, panjang.dtype, panjang.shape)
print(type(panjang).__name__, len(panjang))
# --8<-- [end:array]

# --8<-- [start:vektor]
print(panjang.mean(), panjang.max(), panjang.std().round(3))
print(panjang * 2, panjang[panjang > 4])
print(panjang > 4)
# --8<-- [end:vektor]

# --8<-- [start:matriks]
m = np.array([[1, 0, 2], [0, 3, 0]])
print(m.shape, m.sum(axis=0), m.sum(axis=1))
print(m.T.shape, (m == 0).mean())
# --8<-- [end:matriks]

# --8<-- [start:vektor_kata]
a, b = np.array([1, 0, 1]), np.array([1, 1, 0])
print(a @ b, np.linalg.norm(a).round(3))
print(np.arange(0, 1, 0.25), np.zeros((2, 2), dtype=int))
# --8<-- [end:vektor_kata]

# --8<-- [start:perbandingan]
daftar = [6, 5, 4, 3]
print(daftar * 2)
print(np.array(daftar) * 2)
# --8<-- [end:perbandingan]

# --8<-- [start:galat]
try:
    np.array([1, 2, 3]) + np.array([1, 2])
except ValueError as e:
    print("ValueError:", e)
# --8<-- [end:galat]
