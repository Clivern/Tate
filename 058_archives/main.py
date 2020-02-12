# 058. Archives and compression
#
# tomllib, zipfile, tarfile, gzip, lzma, and bz2.
#
# Run: python 058_archives/main.py

# --- tomllib ---
import tomllib

data = tomllib.loads('name = "learn"\nversion = "0.1.0"\n')
print(data["name"], data["version"])

# --- zipfile ---
import zipfile

from io import BytesIO

buf = BytesIO()
with zipfile.ZipFile(buf, "w") as z:
    z.writestr("hello.txt", "hi")
buf.seek(0)
with zipfile.ZipFile(buf) as z:
    print(z.read("hello.txt"), z.namelist())

# --- tarfile ---
import tarfile, io, time

buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w") as t:
    data = b"hello"
    info = tarfile.TarInfo("a.txt")
    info.size = len(data)
    info.mtime = time.time()
    t.addfile(info, io.BytesIO(data))
print(buf.tell() > 0)

# --- gzip mod ---
import gzip

blob = gzip.compress(b"hello " * 20)
print(len(blob) < 100)
print(gzip.decompress(blob)[:5])

# --- lzma mod ---
import lzma

blob = lzma.compress(b"hello " * 50)
print(len(blob) < 80)
print(lzma.decompress(blob)[:5])

# --- bz2 mod ---
import bz2

blob = bz2.compress(b"hello " * 50)
print(len(blob) < 80)
print(bz2.decompress(blob)[:5])
