# 006. Booleans
#
# True and False are bool, a subclass of int. and/or short-circuit and return an operand.
#
# Run: python 006_bools/main.py

x = 3
print(True, False, True + True)
print(1 < x < 5)
print("a" or "b")
print("" or "b")
print(0 and "no")

one = 1
print(True + True, False * 10, issubclass(bool, int))
print(True == one, True is not one)
print(bool([]), bool([0]), bool("0"))
