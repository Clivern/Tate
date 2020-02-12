# 012. Sets
#
# set and frozenset. Operators, in-place updates, and set methods.
#
# Run: python 012_sets/main.py

# --- sets ---
a = {1, 2, 3, 2}
b = {3, 4}
print(a, a | b, a & b, a - b, a ^ b)
print(2 in a)

s = {1, 2}
s.add(3)
s.update([4, 5], {5})
s.discard(9)
s.remove(1)
print(s)
print(s.union([5, 6]), s.intersection([2, 9]))

acc = {1, 2, 3, 4}
acc.intersection_update([2, 3, 9])
acc.difference_update([3])
print(acc)
print({1, 2} <= {1, 2, 3}, {1, 2}.isdisjoint({9}))

try:
    s.remove(9)
except KeyError:
    print("missing")
s.clear()
print(s)

# --- frozenset mod ---
a = frozenset([1, 2, 3])
b = frozenset([3, 4])
print(a | b, {a: "ok"}[a])

# --- set ops ---
s = {1, 2, 3}
s.add(4)
s.discard(9)
print(s.issubset({1, 2, 3, 4}), s.isdisjoint({9}))
s.remove(1)
print(s)
