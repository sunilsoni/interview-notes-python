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
def summarize_ranges(nums):
    if not nums:
        return []

    result = []
    start = nums[0]
    prev = nums[0]

    # For input [1,2,2,3,5]
    for num in nums[1:]:
        # If current number is same as previous, skip it
        if num == prev:
            continue  # Skip duplicate numbers
        # If current number follows previous number (consecutive)
        elif num == prev + 1:
            prev = num
        else:
            # Sequence breaks
            if start == prev:
                result.append(str(start))
            else:
                result.append(f"{start}→{prev}")
            start = num
            prev = num

    # Handle final range
    if start == prev:
        result.append(str(start))
    else:
        result.append(f"{start}→{prev}")

    return result
