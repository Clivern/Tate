# 031. Files and globs
#
# shutil, glob, fnmatch, tempfile, filecmp, and linecache.
#
# Run: python 031_files/main.py

# --- shutil ---
import shutil

from pathlib import Path

print(shutil.which("python3") or shutil.which("python"))
u = shutil.disk_usage(Path.cwd())
print(u.total > u.free)

# --- glob mod ---
import glob

print(glob.glob("*.md"))
print(len(list(glob.iglob("**/*.py", recursive=True))) >= 0)

# --- fnmatch ---
import fnmatch

names = ["main.py", "test_main.py", "README.md"]
print(fnmatch.filter(names, "*.py"))
print(fnmatch.fnmatch("Foo.PY", "*.py"))

# --- tempfile ---
import tempfile

from pathlib import Path

with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "note.txt"
    p.write_text("hello", encoding="utf-8")
    print(p.read_text(encoding="utf-8"), p.exists())
print("gone")

# --- filecmp ---
import filecmp, tempfile

from pathlib import Path

with tempfile.TemporaryDirectory() as d:
    a, b = Path(d) / "a.txt", Path(d) / "b.txt"
    a.write_text("x", encoding="utf-8")
    b.write_text("x", encoding="utf-8")
    print(filecmp.cmp(a, b, shallow=False))

# --- linecache ---
import linecache, tempfile

from pathlib import Path

with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "x.py"
    p.write_text("a\nb\n", encoding="utf-8")
    print(linecache.getline(str(p), 2).strip())
