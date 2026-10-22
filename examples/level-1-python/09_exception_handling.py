"""Exception handling."""


def ke_angka(teks):
    try:
        return int(teks)
    except ValueError:
        return None


print(ke_angka("12"), ke_angka("dua belas"))

try:
    {"a": 1}["b"]
except KeyError as e:
    print("KeyError:", e)
try:
    1 / 0
except ZeroDivisionError as e:
    print("ZeroDivisionError:", e)
finally:
    print("selesai")


def rata_panjang(daftar):
    if not daftar:
        raise ValueError("daftar teks tidak boleh kosong")
    return sum(len(t) for t in daftar) / len(daftar)


try:
    rata_panjang([])
except ValueError as e:
    print("ValueError:", e)
print(rata_panjang(["aa", "bbbb"]))
