# 032. io
#
# StringIO, BytesIO, and TextIOWrapper.
#
# Run: python 032_io_mod/main.py

# --- io stringio ---
from io import StringIO

import sys

buf = StringIO()
old = sys.stdout
sys.stdout = buf
print("captured")
sys.stdout = old
print(buf.getvalue().strip())

# --- io bytesio ---
from io import BytesIO

buf = BytesIO()
buf.write(b"hello")
print(buf.getvalue(), buf.tell())
buf.seek(0)
print(buf.read(2))

# --- io text ---
from io import BytesIO, TextIOWrapper

raw = BytesIO()
f = TextIOWrapper(raw, encoding="utf-8", newline="\n")
f.write("café\n")
f.flush()
print(raw.getvalue())
