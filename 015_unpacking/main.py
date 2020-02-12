# 015. Unpacking
#
# *rest captures leftover items. * and ** in calls splat sequences and mappings.
#
# Run: python 015_unpacking/main.py

first, *mid, last = [1, 2, 3, 4, 5]
print(first, mid, last)
print([*mid, last])
print("{x} {y}".format(**{"x": 1, "y": 2}))
