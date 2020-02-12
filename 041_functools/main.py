# 041. functools
#
# partial, lru_cache, reduce, wraps, cache, and singledispatch. operator keys.
#
# Run: python 041_functools/main.py

# --- functools partial ---
from functools import partial


def power(base, exp):
    return base**exp


square = partial(power, exp=2)
print(square(5), partial(power, 2)(8))

# --- functools lru ---
from functools import lru_cache


@lru_cache(maxsize=32)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print(fib(10), fib.cache_info().hits)

# --- functools reduce ---
from functools import reduce

print(reduce(lambda a, b: a + b, [1, 2, 3, 4], 0))
print(reduce(lambda a, b: a * b, range(1, 6), 1))

# --- functools wraps ---
from functools import wraps


def deco(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper


@deco
def greet():
    """say hi"""
    return "hi"


print(greet.__name__, greet.__doc__)

# --- functools cache ---
from functools import cache, singledispatch


@cache
def twice(n):
    return n * 2


print(twice(4))


@singledispatch
def dump(x):
    return str(x)


@dump.register
def _(x: int):
    return f"int:{x}"


print(dump(3), dump("a"))

# --- functools dispatch ---
from functools import singledispatchmethod


class Printer:
    @singledispatchmethod
    def show(self, x):
        return f"obj:{x}"

    @show.register
    def _(self, x: int):
        return f"int:{x}"


p = Printer()
print(p.show(2), p.show("z"))

# --- operator mod ---
from operator import itemgetter, attrgetter, add

print(sorted([("b", 2), ("a", 1)], key=itemgetter(0)))
print(add(3, 4))


class U:
    def __init__(self, name):
        self.name = name


print(attrgetter("name")(U("Ada")))
