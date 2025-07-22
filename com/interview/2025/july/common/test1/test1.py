#!/usr/bin/env python3
"""
Question: Given n processes with start times starts[] and end times ends[],
find the minimum number of processes to drop so that the remaining processes
form a synchronized set (i.e., there is at least one process whose interval
overlaps with every other in the set).

Input: two lists of integers, starts and ends, each of length n.
Output: integer, minimum drops.

Example 1:
starts = [2,3,2,6,4]
ends   = [3,4,4,7,6]
Answer = 1

Example 2:
starts = [1,3,4,6,9]
ends   = [2,8,5,7,10]
Answer = 2
"""


"""
### 🔧 Problem: Minimum Process Drops for Synchronization

A team of developers at Amazon is working on process synchronization. One way to achieve process synchronization is through effective inter-process communication. Processes can communicate with each other through shared memory, i.e., by accessing the same resources while executing simultaneously.

---

### 🧩 Definition:

A **set of processes is synchronized** if **there is at least one process** in the set whose **execution time overlaps** with the execution times of **all other processes** in the set.

---

### 🧪 Your Task:

Given the starting and ending times of execution of `n` processes in the arrays `starts[]` and `ends[]`, determine the **minimum number of processes** that must be dropped so the remaining processes form a synchronized set.

> **Note**: A set containing only one process is considered to be synchronized.

---

### 🧾 Function Signature:

```python
def findMinimumProcessDrops(starts: List[int], ends: List[int]) -> int:
```

**Parameters**:

* `starts[]`: List of integers representing start times of the processes.
* `ends[]`: List of integers representing end times of the processes.

**Returns**:

* Integer representing the **minimum number of processes to remove** to leave a synchronized set.

---

### ✅ Constraints:

* $1 \leq n \leq 2 \times 10^5$
* $1 \leq \text{starts[i]} \leq \text{ends[i]} \leq 10^9$
* No two intervals have identical `[start, end]` pairs.

---

### 📥 Input Format:

* The first line contains an integer `n`, the size of `starts[]`.
* The next `n` lines each contain an integer `starts[i]`.
* Then another integer `n` indicating the size of `ends[]`.
* The next `n` lines each contain an integer `ends[i]`.

---

### 💡 Example 1:

#### Input:

```
5
2
3
2
6
4
5
3
4
4
7
6
```

#### Output:

```
1
```

#### Explanation:

Execution intervals:

```
[2, 3], [3, 4], [2, 4], [6, 7], [4, 6]
```

* Remove interval `[6, 7]` → Remaining: `[2, 3], [3, 4], [2, 4], [4, 6]`
* `[2, 4]` intersects with all other intervals. ✅

---

### 💡 Example 2:

#### Input:

```
5
1
3
4
6
9
5
2
8
5
7
10
```

#### Output:

```
2
```

#### Explanation:

Execution intervals:

```
[1, 2], [3, 8], [4, 5], [6, 7], [9, 10]
```

* Remove `[1, 2]` and `[9, 10]`
* Remaining: `[3, 8], [4, 5], [6, 7]` → `[3, 8]` overlaps with all others ✅

---


"""

import bisect
import random
import time

def findMinimumProcessDrops(starts, ends):
    n = len(starts)
    starts_sorted = sorted(starts)
    ends_sorted = sorted(ends)
    max_keep = 0
    for s, e in zip(starts, ends):
        # count intervals with start <= e
        cnt1 = bisect.bisect_right(starts_sorted, e)
        # count intervals with end < s
        cnt2 = bisect.bisect_left(ends_sorted, s)
        keep = cnt1 - cnt2
        if keep > max_keep:
            max_keep = keep
    return n - max_keep

def main():
    tests = [
        # sample case 1
        ([2, 3, 2, 6, 4], [3, 4, 4, 7, 6], 1),
        # sample case 0
        ([1, 3, 4, 6, 9], [2, 8, 5, 7, 10], 2),
        # single interval
        ([5], [10], 0),
        # disjoint intervals
        ([1, 3, 5], [2, 4, 6], 2),
        # all overlapping
        ([1, 2, 3], [10, 5, 4], 0),
    ]
    all_pass = True
    for i, (s, e, exp) in enumerate(tests, 1):
        res = findMinimumProcessDrops(s, e)
        status = "PASS" if res == exp else "FAIL"
        print(f"Test {i}: {status} (got={res}, expected={exp})")
        if res != exp:
            all_pass = False
    print("All tests passed." if all_pass else "Some tests failed.")

    # large random test
    n = 200000
    starts = [random.randint(1, 10**9) for _ in range(n)]
    ends = [s + random.randint(0, 1000) for s in starts]
    t0 = time.time()
    drops = findMinimumProcessDrops(starts, ends)
    t1 = time.time()
    print(f"Large test: n={n}, drops={drops}, time={(t1 - t0):.3f}s")

if __name__ == "__main__":
    main()