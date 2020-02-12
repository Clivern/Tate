# 048. asyncio
#
# async/await, gather, tasks, Queue, and timeout.
#
# Run: python 048_asyncio/main.py

# --- asyncio hello ---
import asyncio


async def main():
    await asyncio.sleep(0)
    return "ok"


print(asyncio.run(main()))


async def twice():
    await asyncio.sleep(0)
    await asyncio.sleep(0)
    return "ok"


print(asyncio.run(twice()))

# --- asyncio gather ---
import asyncio


async def n(x):
    await asyncio.sleep(0)
    return x


async def main():
    return await asyncio.gather(n(1), n(2), n(3))


print(asyncio.run(main()))

# --- asyncio task ---
import asyncio


async def main():
    t = asyncio.create_task(asyncio.sleep(0, result=7))
    return await t


print(asyncio.run(main()))

# --- asyncio queue ---
import asyncio


async def main():
    q = asyncio.Queue()
    await q.put("a")
    return await q.get()


print(asyncio.run(main()))

# --- asyncio timeout ---
import asyncio


async def main():
    try:
        async with asyncio.timeout(0.01):
            await asyncio.sleep(0)
            return "ok"
    except TimeoutError:
        return "late"


print(asyncio.run(main()))
