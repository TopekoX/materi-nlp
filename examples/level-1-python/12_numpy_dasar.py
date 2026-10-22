"""Dasar NumPy."""
import numpy as np

panjang = np.array([6, 5, 4, 3])
print(panjang, panjang.dtype, panjang.shape)
print(panjang.mean(), panjang.max(), panjang.std().round(3))
print(panjang * 2, panjang[panjang > 4])

m = np.array([[1, 0, 2], [0, 3, 0]])
print(m.shape, m.sum(axis=0), m.sum(axis=1))
print(m.T.shape, (m == 0).mean())
a, b = np.array([1, 0, 1]), np.array([1, 1, 0])
print(a @ b, np.linalg.norm(a).round(3))
print(np.arange(0, 1, 0.25), np.zeros((2, 2), dtype=int))
