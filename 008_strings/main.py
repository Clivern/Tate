# 008. Strings
#
# str is an immutable Unicode sequence. Methods, f-strings, format specs, raw strings, and
# encodings.
#
# Run: python 008_strings/main.py

# --- strings ---
s = "Ada Lovelace"
print(s.upper(), s.lower(), s.title(), s[0], s[-1])
print(s.split(), "Ada" in s, s[::-1])
print("-".join(["a", "b", "c"]))
print("  hi  ".strip().replace("hi", "hello"))

csv = "a,b,c,d"
print(csv.split(","), csv.split(",", maxsplit=1), csv.rsplit(",", maxsplit=1))
print("  a   b\tc  ".split())
print("a/b/c.py".rsplit("/", maxsplit=1))
print("a\nb\r\nc\n".splitlines())
print("user@host".partition("@"), "a:b:c".rpartition(":"))

print("xxhelloxx".strip("x"), "  hi  ".lstrip(), "  hi  ".rstrip())
print("abracadabra".find("bra"), "abracadabra".rfind("bra"), "banana".count("ana"))
print("aa-aa-aa".replace("aa", "b", 1))
print("Ada3".isalpha(), "42".isdigit(), "A3".isalnum(), "name_1".isidentifier())
print("notes.tar.gz".endswith((".gz", ".zip")))
print("hi".center(6, "."), "42".zfill(5), "-42".zfill(5))
print("test_mod.py".removesuffix(".py"), "test_mod.py".removeprefix("test_"))

table = str.maketrans({"a": "4", "e": "3", "o": None})
print("adobe".translate(table))
print("a\tb\tc".expandtabs(4))
print("hello world")
print("{name} {year}".format_map({"name": "Ada", "year": 1815}))

try:
    s[0] = "p"
except TypeError as e:
    print(type(e).__name__)

# --- fstrings ---
name = "Ada"
n = 3
print(f"{name} {n:02d}")
print(f"{n=}")
print(f"{1 / 3:.3f}")

# --- format spec ---
print(format(42, "08d"), f"{42:x}", f"{3.14159:6.2f}")
print(f"{'hi':>6}", f"{0.25:.1%}")
print("{0} {1}".format("a", "b"))

# --- raw strings ---
print(r"\n", len(r"\n"))
print(r"C:\temp\x")
import re

print(re.findall(r"\d+", "a12b3"))

# --- unicode ---
print(ord("A"), chr(65), "café")
print(len("é"), "é".encode("utf-8"))
print("a\u0301", len("a\u0301"))

# --- encoding ---
s = "café"
print(s.encode("utf-8"))
print(s.encode("utf-8").decode("utf-8"))
print(b"\xff".decode("latin-1"))
