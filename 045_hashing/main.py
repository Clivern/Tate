# 045. Hashing and encoding
#
# hashlib, hmac, uuid, base64, and binascii.
#
# Run: python 045_hashing/main.py

# --- hashlib ---
import hashlib

h = hashlib.sha256(b"hello")
print(h.hexdigest()[:16])
print(hashlib.md5(b"hello").hexdigest())

# --- hmac ---
import hmac

import hashlib

sig = hmac.new(b"key", b"msg", hashlib.sha256).hexdigest()
print(len(sig), hmac.compare_digest(sig, sig))

# --- uuid mod ---
import uuid

u = uuid.uuid4()
print(u, u.version)
print(uuid.uuid5(uuid.NAMESPACE_DNS, "example.com"))

# --- base64 ---
import base64

print(base64.b64encode(b"hello"))
print(base64.b64decode("aGVsbG8="))
print(base64.urlsafe_b64encode(b"\xff\xfe"))

# --- binascii ---
import binascii

print(binascii.hexlify(b"hi"))
print(binascii.unhexlify("6869"))
print(binascii.crc32(b"hello"))
