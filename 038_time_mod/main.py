# 038. time
#
# time.time, sleep, monotonic, and perf_counter.
#
# Run: python 038_time_mod/main.py

# --- time mod ---
import time

t0 = time.monotonic()
time.sleep(0.01)
print(round(time.monotonic() - t0, 3) >= 0.01)
print(int(time.time()) > 1_700_000_000)

# --- time perf ---
import time

t0 = time.perf_counter()
sum(range(10000))
dt = time.perf_counter() - t0
print(dt >= 0, time.process_time() >= 0)
