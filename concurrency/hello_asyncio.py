
import asyncio


async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")


async def main():
    counters = (count() for _ in range(10))
    await asyncio.gather(*counters)


if __name__ == "__main__":
    asyncio.run(main())
