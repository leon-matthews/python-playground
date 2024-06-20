"""
Run then monitor subprocess using `asyncio.create_subprocess_shell()`.
"""

import asyncio


async def run(cmd: str, *args: str):
    """
    Run a single process then wait for it to finish.

    Not much of an improvement over plain old `subprocess.run()`, yet...

    For long running processes that we want to monitor, like 'ffmpeg', we need
    to improve the way to do things. Rather than use `communicate()`, which
    waits for the process to finish, it would be better to yield each line
    of stdout as it comes in, with something like `process.stdout.readline()`
    """
    process = await asyncio.create_subprocess_exec(
        cmd,
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    print(f'[{cmd!r} exited with {process.returncode}]')

    if stdout:
        print(f'[stdout]\n{stdout.decode()}')

    if stderr:
        print(f'[stderr]\n{stderr.decode()}')


if __name__ == '__main__':
    command = ['ls', '/usr/bin']
    asyncio.run(run(command[0], *command[1:]))
