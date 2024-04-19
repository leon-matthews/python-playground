#!/usr/bin/env python3

"""
Threadpool for concurrent jobs.
"""

from concurrent import futures
import random
import time


class SlowTask:
    def __init__(self, number, min_delay=0.1, max_delay=1.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.number = number
        self.waited = None

    def main(self):
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)
        self.waited = delay
        return self

    def __call__(self):
        return self.main()


def make_jobs(number):
    jobs = []
    for num in range(1, (number + 1)):
        jobs.append(SlowTask(num))
    print(f"{len(jobs)} jobs created")
    return jobs


if __name__ == '__main__':
    runner = futures.ThreadPoolExecutor(max_workers=20)
    jobs = make_jobs(40)
    running = []
    for job in jobs:
        future = runner.submit(job)
        running.append(future)

    new_num = 100
    start = time.perf_counter()
    completed = []
    for future in futures.as_completed(running):
        job = future.result()

        if job.number % 2 == 0:
            future = runner.submit(SlowTask(new_num))
            running.append(future)
            new_num += 1

        print(f"Task {job.number:>2} took {job.waited:.2f} seconds")
        completed.append(job)

    elapsed = time.perf_counter() - start
    print(f"All jobs completed in {elapsed:.2f} seconds")
