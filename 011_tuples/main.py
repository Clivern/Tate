# 011. Tuples
#
# tuple is an immutable sequence. Unpacking, concat, and tuple keys.
#
# Run: python 011_tuples/main.py

point = (3, 4)
x, y = point
print(x, y, point[0])
alone = (1,)
print(alone, type(alone).__name__, (1,) == (1))

t = (1, 2, 1, 3)
print(t.count(1), t.index(3))
print(t + (4,), t * 2)
head, *rest = t
print(head, rest)
(left, right), z = (10, 20), 30
print(left, right, z)

seen = {(0, 0), (1, 2)}
seen.add((0, 0))
print(sorted(seen))
print({(1, 2): "point"}[(1, 2)])
