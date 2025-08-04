"""

### 🧩 Problem Statement

Given a **sorted** array of unique integers, return the **fewest list of ranges**, sorted, where:

1. A **range** describes consecutive numbers **from start to end** (inclusive).
2. Each number in the input array must appear in **exactly one range**.
3. The ranges must **not** include any numbers that **aren't in the input array**.

---

### 📝 Range Formatting Rules

For each **range**:

* If it covers **multiple numbers** (`start ≠ end`), format it as `"start→end"`.
* If it covers a **single number**, format it as just that number.

---

### 🔍 Example

**Input:** `[1, 2, 3, 5, 6, 8, 9]`
**Output:** `["1→3", "5→6", "8→9"]`

---"""
def summarize_ranges(nums):  # define the function taking a sorted list of ints
    """
    Return the minimal list of ranges covering all numbers in 'nums',
    where each range is either "n" or "start→end".
    """
    # If the input list is empty, there are no ranges to return
    if not nums:
        return []  # return an empty list immediately

    result = []  # initialize the list that will hold our formatted ranges
    start = nums[0]  # mark the beginning of the current range
    prev = nums[0]   # keep track of the previous number in the current range

    # iterate over the rest of the numbers to build ranges
    for num in nums[1:]:
        # if current number continues the consecutive sequence
        if num == prev + 1:
            prev = num  # extend the current range by updating 'prev'
        else:
            # the sequence has broken: close out the previous range
            if start == prev:
                # single number range; format as just "n"
                result.append(str(start))
            else:
                # multi-number range; format as "start→prev"
                result.append(f"{start}→{prev}")
            # start a new range at the current number
            start = num
            prev = num

    # after the loop, we must add the final range (same logic as above)
    if start == prev:
        result.append(str(start))           # single number
    else:
        result.append(f"{start}→{prev}")    # start→end format

    return result  # return the completed list of ranges


def main():  # define the entry point for testing
    # list of test cases with 'nums' input and expected 'expected' output
    test_cases = [
        {"nums": [1, 2, 3, 5, 6, 8, 9], "expected": ["1→3", "5→6", "8→9"]},
        {"nums": [], "expected": []},                       # empty list
        {"nums": [5], "expected": ["5"]},                   # singleton
        {"nums": [1, 3, 5, 7], "expected": ["1", "3", "5", "7"]},  # all gaps
        {"nums": [1, 2, 3, 4, 5], "expected": ["1→5"]},     # one big range
    ]

    # add a large stress test: 1 through 100,000 should become one range
    large_start, large_end = 1, 100000
    large_nums = list(range(large_start, large_end + 1))  # generate large consecutive list
    expected_large = [f"{large_start}→{large_end}"]       # expected single-range output
    test_cases.append({"nums": large_nums, "expected": expected_large})

    # run each test and report PASS or FAIL
    for i, case in enumerate(test_cases, 1):
        nums = case["nums"]                   # unpack input
        expected = case["expected"]           # unpack expected output
        result = summarize_ranges(nums)       # compute actual output

        if result == expected:
            print(f"Test case {i}: PASS")    # success message
        else:
            # detailed failure message for debugging
            print(f"Test case {i}: FAIL")
            print(f"  Input:    {nums}")
            print(f"  Expected: {expected}")
            print(f"  Got:      {result}")


# ensure that main() runs when this script is executed directly
if __name__ == "__main__":
    main()