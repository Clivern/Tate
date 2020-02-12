# 028. os
#
# getcwd, listdir, path helpers, walk, and environ.
#
# Run: python 028_os_mod/main.py

# --- os mod ---
import os

print(os.name, os.sep)
print(os.getcwd())
print(len(os.listdir(".")))

# --- os path ---
import os

p = os.path.join("a", "b", "c.py")
print(p, os.path.split(p), os.path.splitext(p))
print(os.path.exists("."), os.path.isdir("."))

# --- os walk ---
import os

n = 0
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in {".git", ".venv", "__pycache__", ".gen"}]
    n += len(files)
    if n > 20:
        break
print("saw at least", n, "files")

# --- os environ ---
import os

print(os.environ.get("PATH", "")[:20], "...")
os.environ["LEARN_PYTHON"] = "1"
print(os.environ["LEARN_PYTHON"])
