# 044. random and secrets
#
# random for simulations, secrets for tokens. Distributions and samples.
#
# Run: python 044_random_mod/main.py

# --- random mod ---
import random

random.seed(0)
print(random.randint(1, 6), random.choice("abc"))
xs = [1, 2, 3, 4]
print(random.sample(xs, 2))

# --- secrets ---
import secrets

print(len(secrets.token_hex(16)))
print(secrets.compare_digest("ab", "ab"))
print(secrets.randbelow(10) < 10)

# --- random sample ---
import random

random.seed(1)
print(round(random.uniform(0, 1), 3))
print(round(random.gauss(0, 1), 3))
print(random.randrange(0, 10, 2) % 2 == 0)
