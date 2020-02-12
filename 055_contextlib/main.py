# 055. contextlib and weakref
#
# contextmanager, suppress, ExitStack, and weakref.
#
# Run: python 055_contextlib/main.py

# --- contextlib ---
from contextlib import contextmanager


@contextmanager
def tag(name):
    print(f"<{name}>")
    try:
        yield name
    finally:
        print(f"</{name}>")


with tag("p") as n:
    print("hi", n)

# --- suppress ---
from contextlib import suppress, closing

from io import StringIO

with suppress(FileNotFoundError):
    open("/no/such/file")
print("ok")
with closing(StringIO("x")) as f:
    print(f.read())

# --- exitstack ---
from contextlib import ExitStack

from io import StringIO

with ExitStack() as stack:
    f = stack.enter_context(StringIO("hi"))
    stack.callback(lambda: print("done"))
    print(f.read())

# --- weakref ---
import weakref


class T:
    pass


t = T()
r = weakref.ref(t)
print(r() is t)
del t
print(r() is None)
