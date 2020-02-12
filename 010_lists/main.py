# 010. Lists
#
# list is a mutable sequence. Methods, slicing, and slice assignment.
#
# Run: python 010_lists/main.py

# --- lists ---
xs = [1, 2, 3]
xs.append(4)
xs.extend([5, 6])
print(xs[0], xs[-1], xs[1:3])
print(xs.pop(), xs)
print([0] * 3)
print(xs[:])

xs.insert(0, 0)
print(xs.pop(0), xs)
xs.remove(5)
print(xs, xs.index(2), xs.count(2))

nums = [3, 1, 2]
print(nums.sort(), nums)
print(sorted([3, 1, 2], reverse=True))
words = ["pear", "Fig", "apple"]
words.sort(key=str.lower)
print(words)
print(list(reversed([1, 2, 3])))

nested = [[1], [2]]
copied = nested.copy()
copied.append([3])
nested[0].append(9)
print(nested, copied)

a = [1, 2]
b = a
a = a + [3]
c = [1, 2]
d = c
c += [3]
print(a, b, c, d)

row = [0] * 3
grid = [row, row]
grid[0][0] = 1
print(grid)
print([[0] * 3 for _ in range(2)])

span = [0, 1, 2, 3, 4]
span[1:4] = [8, 9]
print(span)
del span[1:3]
print(span)

stack = []
stack.append("a")
stack.append("b")
print(stack.pop(), stack.pop(), stack)
xs.clear()
print(xs)

# --- slicing ---
s = list(range(8))
print(s[2:5], s[:3], s[5:], s[::2], s[::-1])
s[1:3] = [10, 11, 12]
print(s)
