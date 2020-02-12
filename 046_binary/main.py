# 046. Binary data
#
# struct, array, heapq, and bisect.
#
# Run: python 046_binary/main.py

# --- struct mod ---
import struct

blob = struct.pack(">IHI", 1, 2, 3)
print(blob, struct.unpack(">IHI", blob))
print(struct.calcsize(">IHI"))

# --- array mod ---
from array import array

a = array("i", [1, 2, 3])
a.append(4)
print(a.tolist(), a.tobytes())

# --- heapq ---
import heapq

h = []
for n in [5, 1, 3]:
    heapq.heappush(h, n)
print(heapq.heappop(h), h)
print(heapq.nsmallest(2, [9, 1, 5, 3]))

# --- bisect ---
import bisect

xs = [1, 3, 3, 7]
print(bisect.bisect_left(xs, 3), bisect.bisect_right(xs, 3))
bisect.insort(xs, 5)
print(xs)
