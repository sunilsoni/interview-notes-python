# ================================================
# 1. QUESTION DETAILS
# ================================================
# Demonstrate how Python decorators work along with yield and generators.
# A decorator adds extra functionality to a function without changing its code.
# A generator is a special function that yields values one at a time instead of returning all at once.

# We will:
# - Create a decorator to measure execution time of a generator function.
# - Use 'yield' inside the generator to produce values one by one.
# - Test the decorator and generator with different datasets.
# ================================================

import time  # used to measure how long a function takes

# ================================================
# 2. DECORATOR DEFINITION
# ================================================

def measure_time(func):
    """A decorator to measure execution time of any function."""

    # Wrapper function that adds timing functionality
    def wrapper(*args, **kwargs):
        start = time.time()  # record start time
        result = func(*args, **kwargs)  # call the actual function
        end = time.time()  # record end time
        print(f"[INFO] Execution time: {end - start:.6f} seconds")
        return result  # return the result from the function

    return wrapper  # return the wrapped function


# ================================================
# 3. GENERATOR FUNCTION USING 'yield'
# ================================================

@measure_time  # apply our decorator to this generator
def generate_squares(n):
    """
    A generator function that yields squares of numbers from 1 to n.
    Using 'yield' makes it memory efficient, suitable for large inputs.
    """
    for i in range(1, n + 1):  # loop through numbers 1 to n
        yield i * i  # yield (not return) each square one by one


# ================================================
# 4. FUNCTION TO TEST RESULTS
# ================================================

def test_generate_squares():
    """Test the generator and decorator with different inputs."""
    test_cases = [
        (5, [1, 4, 9, 16, 25]),  # small input
        (1, [1]),                 # single value
        (0, []),                  # edge case: zero input
    ]

    for idx, (n, expected) in enumerate(test_cases, 1):
        # Convert generator output to a list
        result = list(generate_squares(n))
        # Compare with expected output
        if result == expected:
            print(f"Test Case {idx}: PASS ✅ (Input={n})")
        else:
            print(f"Test Case {idx}: FAIL ❌ (Input={n}, Got={result}, Expected={expected})")


# ================================================
# 5. LARGE DATA TESTING
# ================================================

def test_large_data():
    """Test generator performance and memory handling for large data."""
    n = 10**6  # 1 million numbers
    print(f"\n[INFO] Testing large input: n={n}")
    gen = generate_squares(n)  # get generator object
    count = 0
    total = 0
    # Process elements one by one using yield (no memory explosion)
    for val in gen:
        count += 1
        total += val
    # Simple sanity check
    print(f"[RESULT] Processed {count} numbers successfully, Total sum: {total}")


# ================================================
# 6. MAIN METHOD FOR EXECUTION
# ================================================

if __name__ == "__main__":
    print("=== Running Small Test Cases ===")
    test_generate_squares()

    print("\n=== Running Large Data Test ===")
    test_large_data()
