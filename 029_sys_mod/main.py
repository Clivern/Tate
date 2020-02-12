# 029. sys
#
# version, platform, argv, and sys.path.
#
# Run: python 029_sys_mod/main.py

# --- sys mod ---
import sys

print(sys.version_info[:3], sys.platform)
print(sys.executable)
print(len(sys.path))

# --- sys argv ---
import sys

print(sys.argv[0])
print(sys.argv[1:])

# --- sys path ---
import sys

print(sys.path[0])
print(any("site-packages" in p for p in sys.path))
