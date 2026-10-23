"""Exception handling."""
import traceback


# --8<-- [start:dasar]
def ke_angka(teks):
    try:
        return int(teks)
    except ValueError:
        return None


print(ke_angka("12"), ke_angka("dua belas"))
# --8<-- [end:dasar]

# --8<-- [start:jenis]
try:
    {"a": 1}["b"]
except KeyError as e:
    print("KeyError:", e)
try:
    [1, 2][5]
except IndexError as e:
    print("IndexError:", e)
try:
    1 / 0
except ZeroDivisionError as e:
    print("ZeroDivisionError:", e)
finally:
    print("selesai")
# --8<-- [end:jenis]

# --8<-- [start:else]
def baca_angka(teks):
    try:
        nilai = int(teks)
    except ValueError:
        print("bukan angka:", repr(teks))
    else:
        print("angka valid:", nilai)
    finally:
        print("diperiksa:", repr(teks))


baca_angka("7")
baca_angka("x")
# --8<-- [end:else]

# --8<-- [start:raise]
def rata_panjang(daftar):
    if not daftar:
        raise ValueError("daftar teks tidak boleh kosong")
    return sum(len(t) for t in daftar) / len(daftar)


try:
    rata_panjang([])
except ValueError as e:
    print("ValueError:", e)
print(rata_panjang(["aa", "bbbb"]))
# --8<-- [end:raise]

# --8<-- [start:terlalu_lebar]
def hitung(a, b):
    try:
        return a / b
    except Exception:          # terlalu lebar: menyembunyikan bug
        return 0


print(hitung(6, 3), hitung(6, 0), hitung("6", 3))
# --8<-- [end:terlalu_lebar]

# --8<-- [start:traceback]
def level_3():
    return int("abc")


def level_2():
    return level_3()


try:
    level_2()
except ValueError:
    baris = traceback.format_exc().strip().splitlines()
    print(baris[-1])
    print(len([b for b in baris if b.strip().startswith("File")]), "frame pemanggilan")
# --8<-- [end:traceback]
