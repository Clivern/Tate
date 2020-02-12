# 052. argparse
#
# ArgumentParser, subcommands, and types.
#
# Run: python 052_argparse/main.py

# --- argparse ---
import argparse

p = argparse.ArgumentParser(prog="demo")
p.add_argument("name")
p.add_argument("-n", "--times", type=int, default=1)
ns = p.parse_args(["Ada", "-n", "3"])
print(ns.name, ns.times)
print(p.format_usage().strip())

# --- argparse sub ---
import argparse

p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="cmd", required=True)
g = sub.add_parser("greet")
g.add_argument("name")
ns = p.parse_args(["greet", "Ada"])
print(ns.cmd, ns.name)

# --- argparse types ---
import argparse

p = argparse.ArgumentParser()
p.add_argument("--port", type=int, default=8000)
p.add_argument("--mode", choices=["dev", "prod"], default="dev")
p.add_argument("files", nargs="*")
ns = p.parse_args(["--port", "9", "a.py"])
print(ns.port, ns.mode, ns.files)
