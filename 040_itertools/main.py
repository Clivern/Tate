# 040. itertools
#
# count, chain, groupby, product, permutations, compress, and islice.
#
# Run: python 040_itertools/main.py

# --- itertools count ---
from itertools import count, islice, cycle, repeat

print(list(islice(count(10, 2), 4)))
print(list(islice(cycle("ab"), 5)))
print(list(repeat("x", 3)))

# --- itertools chain ---
from itertools import chain

print(list(chain([1, 2], "ab", (9,))))
print(list(chain.from_iterable([[1, 2], [3]])))

# --- itertools groupby ---
from itertools import groupby

rows = [("a", 1), ("a", 2), ("b", 3)]
for key, group in groupby(rows, key=lambda r: r[0]):
    print(key, list(group))

# --- itertools product ---
from itertools import product

print(list(product("ab", "12")))
print(list(product("ab", repeat=2)))

# --- itertools perm ---
from itertools import permutations, combinations

print(list(permutations("abc", 2)))
print(list(combinations("abc", 2)))

# --- itertools comb ---
from itertools import compress, dropwhile, takewhile

print(list(compress("abcd", [1, 0, 1, 0])))
print(list(dropwhile(lambda n: n < 3, [1, 2, 3, 1, 4])))
print(list(takewhile(lambda n: n < 3, [1, 2, 3, 1])))

# --- itertools islice ---
from itertools import islice, count

print(list(islice(count(), 5, 12, 2)))
print(list(islice("abcdef", 2, 5)))
