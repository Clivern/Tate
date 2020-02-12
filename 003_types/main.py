# 003. Built-in types
#
# int, float, bool, None, str, bytes, list, tuple, set, and dict cover most day-one data.
# Everything is an object.
#
# Run: python 003_types/main.py

n = 10**40
x = 0.1 + 0.2
flag = True
missing = None
text = "Ada"
raw = b"raw"
xs = [1, 2, 3]
point = (3, 4)
tags = {"py", "learn"}
user = {"name": "Ada", "year": 1815}

values = [n, x, flag, missing, text, raw, xs, point, tags, user]
for v in values:
    print(type(v).__name__, v)

print(n.bit_length(), x, flag + flag, missing is None)
print(text.upper(), list(raw), xs[-1], point[0])
print("py" in tags, user.get("year"), user.get("city", "?"))
print([type(v).__name__ for v in values])
