# 033. json
#
# dumps/loads, indent, custom default, and JSON Lines.
#
# Run: python 033_json_mod/main.py

# --- json mod ---
import json

data = {"name": "Ada", "year": 1815, "ok": True}
s = json.dumps(data)
print(s)
print(json.loads(s)["year"])
print(json.dumps(data, indent=2))

# --- json custom ---
import json

from datetime import date


def default(o):
    if isinstance(o, date):
        return o.isoformat()
    raise TypeError(type(o))


print(json.dumps({"d": date(2025, 1, 2)}, default=default, indent=2, sort_keys=True))

# --- json indent ---
import json

rows = [{"n": 1}, {"n": 2}]
text = "\n".join(json.dumps(r) for r in rows)
print([json.loads(line)["n"] for line in text.splitlines()])
