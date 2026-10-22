"""Import dan modul."""
import math
import re as regex
import sys
from collections import Counter
from pathlib import Path

print(math.sqrt(16), math.log(1))
print(Counter("tolong tolong banjir".split()).most_common(1))
print(Path("examples") / "level-1-python")
print(regex.findall(r"\d+", "RT 05 RW 12"))
print(type(sys.modules["math"]).__name__)
