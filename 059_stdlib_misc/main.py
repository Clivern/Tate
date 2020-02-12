# 059. stdlib extras
#
# ipaddress, importlib, graphlib, sched, copyreg, and pkgutil.
#
# Run: python 059_stdlib_misc/main.py

# --- ipaddress ---
import ipaddress

n = ipaddress.ip_network("10.0.0.0/30")
print(n.num_addresses, list(n.hosts()))
print(ipaddress.ip_address("127.0.0.1").is_loopback)

# --- importlib ---
import importlib.util

m = importlib.util.import_module("math")
print(m.sqrt(9))
print(importlib.util.find_spec("json").name)

# --- graphlib ---
from graphlib import TopologicalSorter

ts = TopologicalSorter({"compile": {"parse"}, "parse": set(), "link": {"compile"}})
print(list(ts.static_order()))

# --- sched mod ---
import sched, time

s = sched.scheduler(time.time, time.sleep)
out = []
s.enter(0, 1, out.append, argument=("tick",))
s.run()
print(out)

# --- copyreg mod ---
import copyreg, copy


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


def reduce_point(p):
    return Point, (p.x, p.y)


copyreg.pickle(Point, reduce_point)
p = copy.copy(Point(1, 2))
print(p.x, p.y)

# --- pkgutil ---
import pkgutil

names = [m.name for m in pkgutil.iter_modules() if m.name.startswith("json")]
print("json" in {m.name for m in pkgutil.iter_modules()})
print(len(names) >= 0)
