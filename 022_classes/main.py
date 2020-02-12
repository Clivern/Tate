# 022. Classes
#
# class, __init__, methods, self, class attributes, staticmethod, classmethod, and
# property.
#
# Run: python 022_classes/main.py

# --- classes ---
class Point:
    pass


p = Point()
p.x = 3
p.y = 4
print(p.x, p.y, type(p).__name__)
print(p.__dict__)


# --- init ---
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


a = Person("Ada", 36)
print(a.name, a.age)


# --- methods ---
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self):
        return (self.x**2 + self.y**2) ** 0.5


print(Point(3, 4).dist())


# --- self ---
class Box:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value


print(Box(9).get())


# --- class attr ---
class Counter:
    created = 0

    def __init__(self):
        Counter.created += 1


Counter()
Counter()
print(Counter.created)


# --- static method ---
class Temp:
    @staticmethod
    def c_to_f(c):
        return c * 9 / 5 + 32


print(Temp.c_to_f(0), Temp().c_to_f(100))


# --- class method ---
class Person:
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_pair(cls, first, last):
        return cls(f"{first} {last}")


print(Person.from_pair("Ada", "Lovelace").name)


# --- property ---
class Temp:
    def __init__(self, c):
        self._c = c

    @property
    def c(self):
        return self._c

    @property
    def f(self):
        return self._c * 9 / 5 + 32


t = Temp(100)
print(t.c, t.f)
