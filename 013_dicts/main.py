# 013. Dicts
#
# dict maps hashable keys to values. get, update, merge, views, and nested dicts.
#
# Run: python 013_dicts/main.py

# --- dicts ---
d = {"name": "Ada", "year": 1815}
d["year"] = 1815
print(d["name"], d.get("city", "unknown"))
print(list(d), list(d.values()))
for k, v in d.items():
    print(k, v)

print(d.get("city"), d.get("city", "n/a"))
d.setdefault("tags", []).append("py")
d.setdefault("tags", []).append("learn")
print(d)
print(d.pop("year"), d.pop("missing", None))
print({"a": 1, "b": 2, "c": 3}.popitem())

base = {"a": 1, "b": 0}
base.update({"b": 2, "c": 3}, d=4)
print(base)
print(dict.fromkeys(["a", "b"], 0))
print({"x": 1, "y": 2} | {"y": 9, "z": 3})
print({**{"a": 1}, **{"a": 2, "b": 3}})

print("name" in d, "Ada" in d, "Ada" in d.values())
users = {"ada": {"year": 1815}}
print(users["ada"]["year"], users.get("alan", {}).get("city"))
users.setdefault("alan", {})["year"] = 1912
print(users["alan"])

nested = {"xs": [1, 2]}
copied = nested.copy()
copied["xs"].append(3)
print(nested, copied)
print(list(reversed({"a": 1, "b": 2, "c": 3})))
print({("Ada", 1815): "ok"}[("Ada", 1815)])

try:
    d["city"]
except KeyError as e:
    print(type(e).__name__, e)

# --- dict views ---
d = {"a": 1, "b": 2}
keys = d.keys()
d["c"] = 3
print("c" in keys, keys & {"a", "x"})
print(list(d.items()))
