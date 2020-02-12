# 050. re
#
# search, groups, sub, split, and VERBOSE flags.
#
# Run: python 050_re_mod/main.py

# --- re mod ---
import re

print(re.search(r"\d+", "id=42").group())
print(re.findall(r"[A-Z][a-z]+", "Ada Alan"))
print(bool(re.match(r"Ada", "Ada Lovelace")))
print(re.findall(r"\d+", "a1 b23"))

# --- re groups ---
import re

m = re.search(r"(?P<user>\w+)@(?P<host>[\w.]+)", "a@b.com")
print(m.group("user"), m.groupdict())

# --- re sub ---
import re

print(re.sub(r"\s+", " ", "a   b\tc"))
print(re.split(r"[,;]", "a,b;c"))
print(re.findall(r"ada", "ADA", flags=re.I))

# --- re flags ---
import re

pat = re.compile(
    r"""
    (?P<year>\d{4})
    -
    (?P<month>\d{2})
""",
    re.VERBOSE,
)
print(pat.search("2025-03").groupdict())
