# 042. copy and pprint
#
# deepcopy and pretty-printing nested structures.
#
# Run: python 042_copy_pprint/main.py

# --- copy mod ---
import copy


class Node:
    def __init__(self, v, child=None):
        self.v = v
        self.child = child


n = Node(1, Node(2))
d = copy.deepcopy(n)
n.child.v = 9
print(d.child.v)

# --- pprint mod ---
from pprint import pprint, pformat

data = {"users": [{"name": "Ada", "ids": list(range(5))}], "ok": True}
print(pformat(data, width=40, sort_dicts=True))
pprint({"b": 1, "a": 2}, sort_dicts=True)
