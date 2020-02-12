# 016. if, else, and match
#
# if/elif/else, ternary expressions, and match/case with guards and star patterns.
#
# Run: python 016_control/main.py

# --- if else ---
n = 4
if n % 2 == 0:
    print("even")
else:
    print("odd")

# --- elif ---
score = 76
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("D")

# --- ternary ---
n = 5
label = "pos" if n > 0 else "nonpos"
print(label, "even" if n % 2 == 0 else "odd")


# --- match ---
def kind(x):
    match x:
        case 0:
            return "zero"
        case int() as n if n > 0:
            return "pos int"
        case str() as s:
            return f"str {s}"
        case _:
            return "other"


print(kind(0), kind(3), kind("hi"), kind(1.2))


# --- match guard ---
def grade(n):
    match n:
        case int() if n >= 90:
            return "A"
        case int() if n >= 70:
            return "B"
        case int():
            return "C"
        case _:
            return "?"


print(grade(95), grade(71), grade(10), grade("x"))


# --- star pattern ---
def head_tail(xs):
    match xs:
        case [head, *tail]:
            return head, tail
        case []:
            return None, []
        case _:
            return None, None


print(head_tail([1, 2, 3]), head_tail([]))
