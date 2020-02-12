# 001. Hello and scripts
#
# A .py file is a module. Running it as a script executes the top-level code. print writes
# a line to stdout.
#
# Run: python 001_hello/main.py

print("Hello, Python")
print("hello on stderr", file=__import__("sys").stderr)
print("Hello, Python")

# stderr is for diagnostics, stdout is for the result.
