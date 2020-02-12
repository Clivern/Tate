# 039. collections
#
# Counter, defaultdict, deque, namedtuple, OrderedDict, and ChainMap.
#
# Run: python 039_collections/main.py

# --- collections counter ---
from collections import Counter

c = Counter("abracadabra")
print(c["a"], c.most_common(2))
print(Counter("ab") + Counter("bc"))

# --- defaultdict ---
from collections import defaultdict

g = defaultdict(list)
for name in ["Ada", "Alan", "Alonzo"]:
    g[name[0]].append(name)
print(dict(g))

# --- deque ---
from collections import deque

q = deque([1, 2, 3], maxlen=5)
q.appendleft(0)
q.append(4)
print(q, q.popleft())

# --- namedtuple mod ---
from collections import namedtuple

Row = namedtuple("Row", ["id", "name"])
r = Row(1, "Ada")
print(r._fields, r.id, tuple(r))

# --- ordereddict ---
from collections import OrderedDict

d = OrderedDict([("a", 1), ("b", 2)])
d.move_to_end("a")
print(list(d))
print(OrderedDict([("a", 1), ("b", 2)]) == OrderedDict([("b", 2), ("a", 1)]))

# --- chainmap ---
from collections import ChainMap

defaults = {"host": "localhost", "port": 80}
env = {"port": 8080}
print(ChainMap(env, defaults)["host"], ChainMap(env, defaults)["port"])
