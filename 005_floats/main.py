# 005. Floating point
#
# float is IEEE-754 double. Rounding, inf/nan, isclose, and hex() live here.
#
# Run: python 005_floats/main.py

import math

print(7 / 2)
print(0.1 + 0.2)
print(round(1.5), round(2.5))
print((2.0).is_integer(), (2.1).is_integer())
print((0.5).as_integer_ratio())

print(float("inf"), math.isinf(1e309))
nan = float("nan")
print(nan == nan, math.isnan(nan))
print(math.isclose(0.1 + 0.2, 0.3))

x = 0.1
print(x.hex())
print(float.fromhex(x.hex()) == x)
print(float.fromhex("0x1.0p0"))
