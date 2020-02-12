# 026. Typing
#
# Annotations, dataclasses, enums, TypedDict, Protocol, ABC, generics, aliases, Literal,
# Annotated, and NewType.
#
# Run: python 026_typing/main.py

# --- annotations ---
def greet(name: str, times: int = 1) -> str:
    return " ".join([f"hi {name}"] * times)


print(greet("Ada", 2))
print(greet.__annotations__)

# --- dataclasses ---
from dataclasses import dataclass


@dataclass
class User:
    name: str
    id: int = 0


a = User("Ada", 1)
b = User("Ada", 1)
print(a, a == b, a.name)
print(a.name, a.id)

# --- enums ---
from enum import Enum, auto


class Status(Enum):
    NEW = auto()
    DONE = auto()


print(Status.NEW, Status.NEW.name, Status.NEW.value)
print(list(Status))
print(Status.NEW is Status.NEW)

# --- namedtuple ---
from collections import namedtuple

Point = namedtuple("Point", "x y")
p = Point(3, 4)
print(p.x, p[1], p._asdict())
print(p._replace(y=5))

# --- typeddict ---
from typing import TypedDict


class User(TypedDict):
    name: str
    year: int


u: User = {"name": "Ada", "year": 1815}
print(u["name"], dict(u))

# --- protocol ---
from typing import Protocol, runtime_checkable


@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...


class Handle:
    def close(self) -> None:
        print("closed")


print(isinstance(Handle(), Closeable))
Handle().close()

# --- abc ---
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self) -> float:
        return self.side**2


print(Square(3).area())


# --- generics ---
def first[T](items: list[T]) -> T:
    return items[0]


print(first([1, 2, 3]), first(["a", "b"]))

# --- type alias ---
type UserId = int
type JSON = dict[str, object]


def find(user: UserId) -> JSON:
    return {"id": user}


print(find(7))

# --- cast any ---
from typing import Any, cast


def read() -> Any:
    return "42"


n = cast(int, int(read()))
print(n, n + 1)

# --- typing union ---
from typing import get_args, get_origin

T = int | str
print(get_origin(T), get_args(T))
print(isinstance(3, get_args(T)))

# --- enum flag ---
from enum import Flag, auto


class Perm(Flag):
    R = auto()
    W = auto()
    X = auto()


rw = Perm.R | Perm.W
print(Perm.R in rw, bool(rw & Perm.X), rw)

# --- dataclasses field ---
from dataclasses import dataclass, field


@dataclass
class Bag:
    items: list[int] = field(default_factory=list)
    note: str = field(default="", compare=False)


print(Bag() is not Bag())
print(Bag([1], "a") == Bag([1], "b"))

# --- dataclasses frozen ---
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int


p = Point(1, 2)
print(p, hash(p) != 0, Point(0, 0) < p)

# --- abc abstract ---
from abc import ABC, abstractmethod


class Drawable(ABC):
    @abstractmethod
    def draw(self): ...


class ThirdParty:
    def draw(self):
        return "ok"


Drawable.register(ThirdParty)
print(isinstance(ThirdParty(), Drawable))

# --- typing literal ---
from typing import Final, Literal

MODE: Final[Literal["dev", "prod"]] = "dev"


def run(mode: Literal["dev", "prod"]) -> str:
    return mode


print(run(MODE))

# --- typing annotated ---
from typing import Annotated, get_args

Port = Annotated[int, "tcp port"]
print(get_args(Port))

# --- typing newtype ---
from typing import NewType

UserId = NewType("UserId", int)
uid = UserId(7)
print(uid + 1, type(uid) is int)

# --- collections abc ---
from collections.abc import Mapping, Sequence, Iterable

print(isinstance({"a": 1}, Mapping))
print(isinstance([1], Sequence) and isinstance(range(3), Iterable))
