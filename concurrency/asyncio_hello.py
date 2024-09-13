"""
The 'hello world' of asyncio coroutines and tasks.
"""

import asyncio


async def count() -> None:
    print("One")
    await asyncio.sleep(1)
    print("Two")


async def main() -> None:
    # Create several coroutines by calling `count()`
    counters = (count() for _ in range(10))

    # Calling `gather()` creates running tasks then waits for them to finish
    await asyncio.gather(*counters)


if __name__ == "__main__":
    asyncio.run(main())
