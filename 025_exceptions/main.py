# 025. Exceptions
#
# try/except/else/finally, raise, custom exceptions, and assert.
#
# Run: python 025_exceptions/main.py

# --- exceptions ---
def parse(s):
    try:
        return int(s)
    except ValueError as e:
        print(type(e).__name__, e)
        return None


print(parse("3"), parse("no"))


# --- raise ---
def must_positive(n):
    if n <= 0:
        raise ValueError("n must be > 0")
    return n


try:
    must_positive(-1)
except ValueError as e:
    print(e)


# --- finally ---
def work(ok):
    try:
        if not ok:
            raise RuntimeError("no")
        return "ok"
    finally:
        print("cleanup")


print(work(True))
try:
    work(False)
except RuntimeError:
    print("caught")


# --- else try ---
def load(s):
    try:
        n = int(s)
    except ValueError:
        print("bad")
    else:
        print("got", n)


load("4")
load("x")


# --- custom exc ---
class NotFound(Exception):
    pass


class UserNotFound(NotFound):
    def __init__(self, user_id):
        super().__init__(f"user {user_id} missing")
        self.user_id = user_id


try:
    raise UserNotFound(9)
except NotFound as e:
    print(e, e.user_id)


# --- assert stmt ---
def area(w, h):
    assert w > 0 and h > 0, "sizes must be positive"
    return w * h


print(area(3, 4))
try:
    area(0, 2)
except AssertionError as e:
    print(e)
