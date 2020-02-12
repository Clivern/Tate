# 024. Dunder methods
#
# __len__, __eq__, __hash__, __repr__, __str__, context managers, with, iterators,
# getitem, and call.
#
# Run: python 024_dunder/main.py

# --- dunder ---
class Bag:
    def __init__(self, items):
        self.items = list(items)

    def __len__(self):
        return len(self.items)

    def __add__(self, other):
        return Bag(self.items + other.items)


print(len(Bag([1, 2])), (Bag([1]) + Bag([2])).items)


# --- eq hash ---
class User:
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


print(User(1) == User(1), len({User(1), User(1), User(2)}))


# --- repr str ---
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x!r}, {self.y!r})"

    def __str__(self):
        return f"({self.x}, {self.y})"


p = Point(1, 2)
print(repr(p), str(p), f"{p!r}")


# --- context mgr ---
class Tag:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"<{self.name}>")
        return self

    def __exit__(self, *exc):
        print(f"</{self.name}>")
        return False


with Tag("p"):
    print("hello")

# --- with stmt ---
from io import StringIO

with StringIO() as f:
    f.write("hi")
    captured = f.getvalue()
print(captured)


# --- iter proto ---
class Count:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        self.i += 1
        return self.i


print(list(Count(3)))

# --- next fn ---
it = iter([10, 20])
print(next(it), next(it), next(it, "empty"))


# --- getitem ---
class FirstLast:
    def __init__(self, items):
        self.items = list(items)

    def __getitem__(self, i):
        if i == 0:
            return self.items[0]
        if i == -1:
            return self.items[-1]
        raise IndexError(i)


fl = FirstLast([10, 20, 30])
print(fl[0], fl[-1])


# --- call ---
class Adder:
    def __init__(self, n):
        self.n = n

    def __call__(self, x):
        return x + self.n


add3 = Adder(3)
print(add3(10), callable(add3))
