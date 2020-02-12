# 002. Variables and bindings
#
# A name is bound to an object. There is no separate declaration. Later assignment rebinds
# the name.
#
# Run: python 002_variables/main.py

n = 3
name = "Ada"
n = n + 1
print(n, name)
print(type(n).__name__, type(name).__name__)

# Rebinding does not mutate the old object.
