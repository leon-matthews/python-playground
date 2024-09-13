"""
Use a mixture of synchronous and asynchronous functions together.
"""

import asyncio
import time


def sync_sleep(seconds: float) -> float:
    """
    Ordinary, blocking, and synchronous sleep function.

    Very annoying to find this here in an otherwise fully-asyncio program!
    """
    time.sleep(seconds)
    return seconds


async def sync_sleep_wrapper(seconds: float) -> float:
    """
    Wrap blocking function in a new thread to make it act asynchronously.
    """
    retval = asyncio.to_thread(sync_sleep, seconds)
    await retval
    return seconds


async def async_sleep(seconds: float) -> float:
    await asyncio.sleep(seconds)
    return seconds


async def gather(seconds: float) -> float:
    """
    Create then await tasks them to finish running together.

    Return:
        Sum of all function return values
    """
    tasks = asyncio.gather(
        async_sleep(seconds),
        async_sleep(seconds),
        async_sleep(seconds),
        sync_sleep_wrapper(seconds),
        sync_sleep_wrapper(seconds),
    )
    returned = await tasks
    return sum(returned)


async def groups(seconds: float) -> float:
    """
    The same as `gather` but using new `TaskGroup` context manager.

    Available only from Python 3.11 onwards.
    """
    tasks = []
    async with asyncio.TaskGroup() as group:
        tasks.append(group.create_task(async_sleep(seconds)))
        tasks.append(group.create_task(async_sleep(seconds)))
        tasks.append(group.create_task(async_sleep(seconds)))
        tasks.append(group.create_task(sync_sleep_wrapper(seconds)))
        tasks.append(group.create_task(sync_sleep_wrapper(seconds)))

    return sum([task.result() for task in tasks])


async def main(seconds: float) -> None:
    waited = await groups(seconds)
    waited += await gather(seconds)
    print(f"Waited a total of {waited:,} seconds")


if __name__ == "__main__":
    asyncio.run(main(1))
