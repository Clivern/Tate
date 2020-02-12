# 043. Math
#
# math, cmath, decimal, fractions, statistics, and numbers ABCs.
#
# Run: python 043_math_mod/main.py

# --- math mod ---
import math

print(math.sqrt(16), math.hypot(3, 4), math.pi)
print(math.comb(5, 2), math.isclose(0.1 + 0.2, 0.3))

# --- cmath ---
import cmath

z = 1 + 1j
print(z * z, abs(z), cmath.phase(z))
print(cmath.polar(z))

# --- decimal mod ---
from decimal import Decimal, getcontext

getcontext().prec = 6
print(Decimal("0.1") + Decimal("0.2"))
print(Decimal("1") / Decimal("7"))

# --- fractions ---
from fractions import Fraction

print(Fraction(1, 3) + Fraction(1, 6))
print(Fraction(0.5), Fraction("0.5"))
print(Fraction(3.14159).limit_denominator(100))

# --- statistics ---
import statistics

xs = [1, 2, 2, 3, 8]
print(statistics.mean(xs), statistics.median(xs), statistics.mode(xs))
print(statistics.pstdev(xs))

# --- statistics spread ---
import statistics

xs = [1.0, 2.0, 2.0, 3.0, 8.0]
ys = [1.0, 2.0, 2.1, 2.9, 9.0]
print(statistics.stdev(xs))
print(statistics.quantiles(xs, n=4))
print(statistics.correlation(xs, ys))

# --- numbers mod ---
import numbers

print(isinstance(3, numbers.Integral), isinstance(1.2, numbers.Real))
print(isinstance(1 + 0j, numbers.Complex))
