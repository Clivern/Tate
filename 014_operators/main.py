# 014. Operators and truthiness
#
# Arithmetic and bitwise ops, identity vs equality, and/or/not, chained comparisons, in,
# and del.
#
# Run: python 014_operators/main.py

# --- operators ---
print(7 + 3, 7 - 3, 7 * 3, 7 / 3, 7 // 3, 7 % 3)
print(7 & 3, 7 | 3, 7 ^ 3, 7 << 1)
print(3 == 3.0, True is True)

# --- identity ---
a = [1, 2]
b = a
c = [1, 2]
print(a is b, a is c, a == c)
print(id(a) == id(b))

# --- truthiness ---
for v in (None, 0, 0.0, "", [], {}, set(), "x", [0]):
    print(repr(v), bool(v))

# --- is vs eq ---
x = None
print(x is None, x == None)
a = 10**10
b = 10**10
print(a == b, a is b)

# --- and or ---
print(not [])
print([] or "default")
print("hi" and "there")
print(0 or 2 or 3)

# --- chaining ---
x = 3
print(1 < x < 5)
print(1 < x > 2)
print("a" <= "abc" <= "b")

# --- del stmt ---
xs = [1, 2, 3]
del xs[1]
print(xs)
d = {"a": 1, "b": 2}
del d["a"]
print(d)

# --- in op ---
print(3 in [1, 2, 3], "a" in "cat", "k" in {"k": 1})
print(2 not in {1, 3})
