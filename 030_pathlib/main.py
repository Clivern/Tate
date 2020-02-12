# 030. pathlib
#
# Path joins, parts, glob, and read/write.
#
# Run: python 030_pathlib/main.py

# --- pathlib ---
from pathlib import Path

p = Path.cwd() / "README.md"
print(p.name, p.suffix, p.exists())
print(Path("a/b/c.py").parts)
print(Path.cwd().name)

# --- path parts ---
from pathlib import Path

p = Path("/tmp/demo.tar.gz")
print(p.name, p.stem, p.suffix, p.suffixes)
print(p.parent, p.with_suffix(".txt").name)

# --- path glob ---
from pathlib import Path

hits = list(Path(".").glob("*.md"))
py = list(Path(".").glob("*.py"))
print(len(hits), "md", len(py), "py")

# --- pathlib write ---
from pathlib import Path

import tempfile

with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "a" / "b.txt"
    p.parent.mkdir(parents=True)
    p.write_text("hi", encoding="utf-8")
    print(p.read_text(encoding="utf-8"))
