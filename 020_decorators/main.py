# 020. Decorators
#
# @deco is f = deco(f). Argument-taking decorators return the real decorator.
#
# Run: python 020_decorators/main.py

# --- decorators ---
def trace(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        print(fn.__name__, args, result)
        return result

    return wrapper


@trace
def add(a, b):
    return a + b


add(2, 3)


# --- decorator args ---
def repeat(times):
    def deco(fn):
        def wrapper(*args, **kwargs):
            return [fn(*args, **kwargs) for _ in range(times)]

        return wrapper

    return deco


@repeat(3)
def hi():
    return "hi"


print(hi())
