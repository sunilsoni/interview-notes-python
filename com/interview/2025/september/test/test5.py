# Python 3 code: Decorator that wraps a generator and demonstrates yield behavior

from functools import wraps  # import wraps to preserve function metadata (name, docstring)
from time import perf_counter  # high-resolution timer for measuring execution time


def trace_yield(transform=lambda x: x, label="TRACE", log_every=1):
    """
    Decorator factory for generator functions.

    Parameters:
      transform: a function f(x) -> y to transform each yielded item (default: identity)
      label:     short tag printed in logs to identify this wrapper instance
      log_every: log frequency; 1 = log every item, 0 = disable per-item logs, N = log every Nth item

    Returns:
      A decorator that, when applied to a generator function, wraps it with logging, timing, and transformation.
    """
    # We return an actual decorator from this factory so callers can configure behavior.
    def decorator(gen_func):
        # wraps ensures the wrapper keeps the original function's name and help().
        @wraps(gen_func)
        def wrapper(*args, **kwargs):
            # Start a timer to measure total generator runtime.
            start = perf_counter()  # record start time for timing
            # Optional: print a start banner (skip if log_every == 0 to reduce noise in big runs).
            if log_every != 0:
                print(f"[{label}] start {gen_func.__name__}(args={args}, kwargs={kwargs})")  # start log
            # Call the original generator function to obtain a generator object.
            gen = gen_func(*args, **kwargs)  # underlying generator
            # Keep a count of how many items we yield.
            count = 0  # number of items yielded so far
            try:
                # Iterate lazily over the underlying generator.
                for item in gen:  # pull next value from original generator as needed
                    count += 1  # increment yield counter
                    # Apply the transform to the item (identity if not provided).
                    out = transform(item)  # transform the yielded item
                    # Log either every item or every Nth item, or not at all.
                    if log_every != 0 and (count % log_every == 0):  # conditional logging
                        print(f"[{label}] yield #{count}: in={item} out={out}")  # per-yield log line
                    # Yield the (possibly transformed) item to the caller.
                    yield out  # re-yield lazily so we remain a generator
            finally:
                # Always log total time and count when the generator finishes or is closed.
                duration = perf_counter() - start  # compute elapsed time
                if log_every != 0:  # print completion banner when logging is on
                    print(f"[{label}] done {gen_func.__name__}: yielded={count} in {duration:.6f}s")  # end log
        # Return the wrapper generator function.
        return wrapper  # this function now behaves like the original but with tracing/transform
    # Return the configured decorator to be applied with @trace_yield(...)
    return decorator  # the outer factory returns the decorator


# Example 1: count numbers 1..n, then SQUARE them via the decorator's transform.
@trace_yield(transform=lambda x: x * x, label="SQUARE", log_every=1)  # decorate: square each yielded value, log every item
def count_up(n):
    # Guard against bad inputs: treat negatives as 0.
    n = int(n)  # ensure integer input
    if n < 0:   # handle negative case by early return (no yields)
        return  # returning from a generator before yield produces an empty generator
    # Yield numbers from 1 to n inclusive.
    for i in range(1, n + 1):  # loop from 1 to n
        yield i  # yield the raw number; decorator will square it


# Example 2: yield EVEN numbers up to n; decorator will DOUBLE them.
@trace_yield(transform=lambda x: x * 2, label="DOUBLE", log_every=1)  # decorate: double each even number
def evens_up_to(n):
    # Normalize and guard input.
    n = int(n)  # ensure integer input
    if n < 2:   # if less than 2, there are no positive even numbers
        return  # early return: generator yields nothing
    # Yield only even numbers up to and including n.
    for i in range(2, n + 1, 2):  # step by 2 to generate evens: 2, 4, 6, ...
        yield i  # yield each even; decorator will double it


# Example 3: identity stream (no transform), but SILENT during large runs (log_every=0).
@trace_yield(label="IDENTITY_SILENT", log_every=0)  # decorate with identity transform and no per-item logging
def identity_up_to(n):
    # Normalize and guard input.
    n = int(n)  # ensure integer input
    if n <= 0:  # zero or negative yields nothing
        return  # empty generator
    # Yield numbers 1..n (identity, not changed by decorator).
    for i in range(1, n + 1):  # loop from 1 to n
        yield i  # yield unchanged; decorator is identity and silent


# Helper to collect a limited number of items from a generator (used in small tests).
def collect(gen):
    # Convert a generator/iterable to a list (only used for small expected outputs).
    return list(gen)  # materialize items into a list for comparison in tests


def run_tests():
    """
    Simple PASS/FAIL test harness (no unittest).
    Verifies small, edge, and large streaming scenarios.
    """
    # Store (name, actual_value, expected_value, comparator) tuples for unified PASS/FAIL printing.
    results = []  # list to hold each test result

    # --- Small tests: exact sequence checks ---
    actual = collect(count_up(5))  # SQUARE transform applied to 1..5 -> [1,4,9,16,25]
    expected = [1, 4, 9, 16, 25]  # expected squares
    results.append(("count_up(5) squares", actual, expected, lambda a, e: a == e))  # add test case

    actual = collect(evens_up_to(10))  # evens doubled: evens=2,4,6,8,10 -> doubled=4,8,12,16,20
    expected = [4, 8, 12, 16, 20]  # expected doubled evens
    results.append(("evens_up_to(10) doubled", actual, expected, lambda a, e: a == e))  # add test case

    # --- Edge cases ---
    actual = collect(count_up(0))  # 0 yields nothing -> []
    expected = []  # empty
    results.append(("count_up(0) empty", actual, expected, lambda a, e: a == e))  # add test case

    actual = collect(count_up(-3))  # negative yields nothing -> []
    expected = []  # empty
    results.append(("count_up(-3) empty", actual, expected, lambda a, e: a == e))  # add test case

    # --- Large streaming test: avoid materializing all items ---
    N = 200_000  # choose a large N to test performance without using too much memory
    # Sum streamed values (identity) without building a list.
    streamed_sum = 0  # initialize running sum
    for x in identity_up_to(N):  # iterate lazily, no per-item logging
        streamed_sum += x  # accumulate

    # Expected sum of 1..N is N(N+1)/2.
    expected_sum = N * (N + 1) // 2  # closed-form sum to compare
    results.append((f"identity_up_to({N}) sum", streamed_sum, expected_sum, lambda a, e: a == e))  # add test case

    # Print PASS/FAIL report.
    passed = 0  # count how many tests passed
    total = len(results)  # total number of tests
    print("\n=== TEST RESULTS ===")  # header
    for name, actual, expected, cmp_fn in results:  # iterate each test case
        ok = cmp_fn(actual, expected)  # evaluate comparator
        status = "PASS" if ok else "FAIL"  # build status string
        if ok:  # passed test
            print(f"[PASS] {name}")  # print success line
            passed += 1  # increment pass counter
        else:  # failed test
            print(f"[FAIL] {name} | actual={actual} | expected={expected}")  # print diagnostic

    # Print a final summary line.
    print(f"Summary: {passed}/{total} tests passed")  # concise summary


# Standard Python entry point: run tests when executed as a script.
if __name__ == "__main__":  # only run when this file is executed directly
    run_tests()  # execute our simple PASS/FAIL test suite