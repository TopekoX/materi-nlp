"""Import dan modul."""
# --8<-- [start:gaya]
import math
import re as regex
import sys
from collections import Counter
from pathlib import Path

print(math.sqrt(16), math.log(1))
print(regex.findall(r"\d+", "RT 05 RW 12"))
# --8<-- [end:gaya]

# --8<-- [start:from]
print(Counter("tolong tolong banjir".split()).most_common(1))
print((Path("examples") / "level-1-python").as_posix())
# --8<-- [end:from]

# --8<-- [start:objek]
print(type(math).__name__, type(sys.modules["math"]).__name__, math is sys.modules["math"])
print(math.pi.__class__.__name__, "pi" in dir(math))
# --8<-- [end:objek]

# --8<-- [start:galat]
try:
    import paket_yang_tidak_ada
except ModuleNotFoundError as e:
    print("ModuleNotFoundError:", e)
try:
    from math import fungsi_tidak_ada
except ImportError as e:
    print("ImportError:", e)
# --8<-- [end:galat]

# --8<-- [start:nama]
print(__name__)
# --8<-- [end:nama]
