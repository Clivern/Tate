# 019. Scope, closures, and recursion
#
# LEGB lookup, global, nonlocal, closures, nested functions, and recursion.
#
# Run: python 019_scope/main.py

# --- scope ---
x = "global"


def outer():
    x = "enclosing"

    def inner():
        print(x)

    inner()
    print(x)


outer()
print(x)

# --- global kw ---
count = 0


def bump():
    global count
    count += 1


bump()
bump()
print(count)


# --- nonlocal kw ---
def make_counter():
    n = 0

    def inc():
        nonlocal n
        n += 1
        return n

    return inc


c = make_counter()
print(c(), c(), c())


# --- closures ---
def multiply_by(factor):
    def scale(n):
        return n * factor

    return scale


double = multiply_by(2)
print(double(5), multiply_by(10)(3))


# --- nested ---
def sort_by_len(words):
    def key(w):
        return len(w), w

    return sorted(words, key=key)


print(sort_by_len(["pear", "fig", "apple"]))


# --- recursion ---
def fact(n):
    return 1 if n <= 1 else n * fact(n - 1)


print(fact(5), fact(0))
