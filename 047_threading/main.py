# 047. Threading and futures
#
# queue, Thread, Lock, Event, ThreadPoolExecutor, and as_completed.
#
# Run: python 047_threading/main.py

# --- queue mod ---
from queue import Queue

q = Queue()
q.put("a")
q.put("b")
print(q.get(), q.get(), q.empty())

# --- threading ---
import threading

box = []


def work(n):
    box.append(n)


t = threading.Thread(target=work, args=(7,))
t.start()
t.join()
print(box)

# --- locks ---
import threading

lock = threading.Lock()
n = 0


def bump():
    global n
    with lock:
        n += 1


ts = [threading.Thread(target=bump) for _ in range(8)]
for t in ts:
    t.start()
for t in ts:
    t.join()
print(n)

# --- events ---
import threading

ev = threading.Event()


def go():
    ev.wait(timeout=1)
    print("released")


t = threading.Thread(target=go)
t.start()
ev.set()
t.join()

# --- concurrent ---
from concurrent.futures import ThreadPoolExecutor


def square(n):
    return n * n


with ThreadPoolExecutor(max_workers=3) as pool:
    print(list(pool.map(square, [1, 2, 3, 4])))

# --- futures wait ---
from concurrent.futures import ThreadPoolExecutor, as_completed


def work(n):
    return n * 10


with ThreadPoolExecutor(max_workers=2) as pool:
    futs = [pool.submit(work, n) for n in range(4)]
    print(sorted(f.result() for f in as_completed(futs)))
