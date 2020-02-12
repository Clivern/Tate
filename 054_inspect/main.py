# 054. inspect, ast, dis
#
# Signatures, AST, and bytecode.
#
# Run: python 054_inspect/main.py

# --- inspect mod ---
import inspect


def greet(name: str, times: int = 1) -> str:
    return name * times


print(inspect.signature(greet))
print(inspect.isfunction(greet))

# --- ast mod ---
import ast

tree = ast.parse("a = 1 + 2")
print(type(tree.body[0]).__name__)
print(ast.literal_eval("[1, {'a': 2}]"))

# --- dis mod ---
import dis


def add(a, b):
    return a + b


print("BINARY" in dis.Bytecode(add).dis() or True)
print(list(dis.Bytecode(add))[0].opname)
