# 023. Inheritance
#
# Subclassing, super(), MRO, mixins, and __slots__.
#
# Run: python 023_inheritance/main.py

# --- inheritance ---
class Animal:
    def speak(self):
        return "..."


class Dog(Animal):
    def speak(self):
        return "woof"


d = Dog()
print(d.speak(), isinstance(d, Animal), issubclass(Dog, Animal))


# --- super ---
class A:
    def __init__(self):
        self.a = 1


class B(A):
    def __init__(self):
        super().__init__()
        self.b = 2


print(B().a, B().b)


# --- mro ---
class A:
    pass


class B(A):
    pass


class C(A):
    pass


class D(B, C):
    pass


print([c.__name__ for c in D.__mro__])


# --- multiple inherit ---
class JSONMixin:
    def to_json(self):
        return {"name": self.name}


class User(JSONMixin):
    def __init__(self, name):
        self.name = name


print(User("Ada").to_json())


# --- slots ---
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


p = Point(1, 2)
print(p.x, p.y)
print(hasattr(p, "__dict__"))
