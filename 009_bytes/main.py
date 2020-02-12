# 009. Bytes and buffers
#
# bytes, bytearray, and memoryview. encode/decode, hex, and binary split.
#
# Run: python 009_bytes/main.py

# --- bytes ---
b = "café".encode("utf-8")
print(b, list(b[:4]))
print(b.decode("utf-8"))
ba = bytearray(b)
ba[0] = 67
print(ba)

raw = bytes.fromhex("68 69")
print(raw, raw.hex(), raw.hex(" "))
print(bytes.fromhex("c3 a9").decode())

line = b"a,b,c"
print(line.split(b","), line.find(b"b"), line.replace(b",", b":"))
try:
    line.split(",")
except TypeError as e:
    print(type(e).__name__)

# --- memoryview ---
b = bytearray(b"abcdef")
v = memoryview(b)
print(bytes(v[1:4]))
v[0] = 65
print(b)

# --- bytearray mod ---
ba = bytearray()
ba.extend(b"he")
ba.extend(b"llo")
print(ba.decode(), ba[0])
ba[0] = ord("H")
print(ba)
