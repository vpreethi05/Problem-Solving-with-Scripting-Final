# utils/decorators.py

import time

def timing_decorator(func):
    """
    A simple decorator that measures how long a function takes.
    Used to measure optimization run time.
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        elapsed = end - start
        print(f"Execution time: {elapsed:.4f} seconds")

        return result

    return wrapper
