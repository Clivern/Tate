# 017. Loops
#
# for, while, break, continue, else on loops, range, enumerate, and zip.
#
# Run: python 017_loops/main.py

# --- for ---
for ch in "py":
    print(ch)
for i, name in [(0, "Ada"), (1, "Alan")]:
    print(i, name)

# --- while ---
n = 3
while n > 0:
    print(n)
    n -= 1
print("done")

# --- break continue ---
for n in range(8):
    if n % 2 == 0:
        continue
    if n > 5:
        break
    print(n)

# --- else loops ---
for n in [2, 4, 6]:
    if n % 2 == 1:
        print("odd")
        break
else:
    print("all even")

# --- range ---
print(list(range(4)))
print(list(range(2, 8, 2)))
print(list(range(5, 0, -1)))
print(len(range(1000)))

# --- enumerate ---
for i, ch in enumerate("abc", start=1):
    print(i, ch)

# --- zip ---
names = ["Ada", "Alan"]
years = [1815, 1912]
print(list(zip(names, years)))
pairs = [(1, 2), (3, 4)]
print(list(zip(*pairs)))
