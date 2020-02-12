# 056. subprocess and process
#
# run, pipes, platform, atexit, and signal.
#
# Run: python 056_subprocess/main.py

# --- platform mod ---
import platform

print(platform.system(), platform.machine())
print(platform.python_version())

# --- subprocess ---
import subprocess, sys

r = subprocess.run(
    [sys.executable, "-c", "print(1+1)"], capture_output=True, text=True, check=True
)
print(r.stdout.strip(), r.returncode)

# --- subprocess pipe ---
import subprocess, sys

r = subprocess.run(
    [sys.executable, "-c", "import sys; print(sys.stdin.read().upper())"],
    input="hi",
    capture_output=True,
    text=True,
    check=True,
)
print(r.stdout.strip())

# --- atexit mod ---
import atexit

atexit.register(lambda: None)
print("registered")

# --- signal mod ---
import signal

print(signal.SIGINT)
old = signal.getsignal(signal.SIGINT)
print(old is not None)
