# 021. Comprehensions and generators
#
# List/set/dict comprehensions, generator expressions, yield, yield from, and send.
#
# Run: python 021_comprehensions/main.py

# --- list comp ---
print([n * n for n in range(6) if n % 2 == 0])
print([f"{a}{b}" for a in "ab" for b in "12"])

# --- set comp ---
print({n % 3 for n in range(10)})
print({(n, n * n) for n in range(4)})

# --- dict comp ---
words = ["Ada", "Alan", "Alonzo"]
print({w[0]: w for w in words})
print({w: len(w) for w in words if w.startswith("Al")})

# --- genexp ---
it = (n * n for n in range(5))
print(next(it), next(it))
print(sum(n * n for n in range(5)))


# --- generators ---
def countdown(n):
    while n > 0:
        yield n
        n -= 1


print(list(countdown(3)))
g = countdown(2)
print(next(g), next(g))


# --- yield from ---
def chain(*iters):
    for it in iters:
        yield from it


print(list(chain(range(2), "ab", [9])))


# --- send ---
def accumulator():
    total = 0
    while True:
        n = yield total
        if n is None:
            continue
        total += n


g = accumulator()
print(next(g))
print(g.send(5), g.send(7))
