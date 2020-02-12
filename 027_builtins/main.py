# 027. Builtins
#
# copy, any/all, map/filter, sorted, min/max/sum.
#
# Run: python 027_builtins/main.py

# --- copy obj ---
import copy

a = [[1], [2]]
b = copy.copy(a)
c = copy.deepcopy(a)
a[0].append(9)
print(a, b, c)

# --- any all ---
print(any([0, 0, 2]), all([1, 2, 3]), all([]), any([]))
print(all(n > 0 for n in [1, 2, 3]))

# --- map filter ---
print(list(map(str.upper, ["a", "b"])))
print(list(filter(lambda n: n % 2 == 0, range(6))))

# --- sorted key ---
words = ["pear", "Fig", "apple"]
print(sorted(words))
print(sorted(words, key=str.lower))
print(sorted(words, key=len, reverse=True))

# --- min max sum ---
print(min(3, 1, 2), max([3, 1, 2]))
print(min("abc", "aa", key=len))
print(sum([1, 2, 3], start=10))
