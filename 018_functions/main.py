# 018. Functions
#
# def, return, positional and keyword arguments, defaults, *args, **kwargs, lambda,
# walrus, and pass.
#
# Run: python 018_functions/main.py

# --- functions ---
def add(a, b):
    return a + b


def greet(name):
    print(f"hi {name}")


print(add(2, 3))
greet("Ada")
print(greet("Alan"))
print(add(10, 20))


# --- return ---
def divmod_like(a, b):
    if b == 0:
        return None
    return a // b, a % b


print(divmod_like(7, 3))
print(divmod_like(7, 0))


# --- args ---
def repeat(text, times):
    return text * times


print(repeat("ab", 3))


# --- defaults ---
def append_one(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


print(append_one(1))
print(append_one(2))
print(append_one(3, [0]))


# --- kwargs ---
def greet(name, greeting="hi"):
    return f"{greeting} {name}"


print(greet("Ada"))
print(greet(name="Alan", greeting="hello"))


def dump(**kwargs):
    return sorted(kwargs.items())


print(dump(a=1, b=2))


# --- starargs ---
def total(*nums):
    return sum(nums)


print(total(1, 2, 3, 4))
print(total(*range(5)))


# --- keyword only ---
def connect(host, *, timeout=1.0, tls=True):
    return host, timeout, tls


print(connect("db", timeout=2.5))


# --- positional only ---
def dist(x, y, /):
    return (x**2 + y**2) ** 0.5


print(dist(3, 4))

# --- lambda ---
add = lambda a, b: a + b
print(add(2, 3))
print(sorted(["aa", "b", "ccc"], key=lambda s: len(s)))

# --- walrus ---
import re

text = "id=42"
if m := re.search(r"id=(\d+)", text):
    print(m.group(1))
print(n := 3, n + 1)


# --- pass ellipsis ---
def todo():
    pass


def stub() -> int: ...


print(todo(), stub(), ...)
