"""
### Problem Overview
You need to create an algorithm to manage a one-way bridge that has a maximum weight capacity. Cars waiting in line have specific weights, and the goal is to determine the minimum number of cars that must turn back to prevent the total weight on the bridge from exceeding its limit.

### Assumptions
1. **N**: An integer representing the number of cars, within the range [1..100,000].
2. **weight**: An array of integers representing the weights of the cars, where each element is within the range [1..1,000,000,000].
3. **U**: An integer representing the maximum weight limit of the bridge, within the range [1..1,000,000,000].

### Input/Output Requirements
- **Input**:
  - An integer **U** (the weight limit of the bridge).
  - An array **weight** containing the weights of the cars waiting to cross the bridge.
- **Output**:
  - The minimum number of drivers that must turn back.

### Examples
1. **For** `U = 9` and `weight = [5, 3, 8, 1, 8, 7, 7, 6]`:
   - The function should return `4`. After some cars turn back, the remaining weights can safely cross.

2. **For** `U = 7` and `weight = [7, 6, 5, 2, 7, 4, 5, 4]`:
   - The function should return `5`.

3. **For** `U = 7` and `weight = [3, 4, 3, 1]`:
   - The function should return `0`.

4. **For** `U = 2` and `weight = [8, 7, 5, 5, 6, 3, 9, 10, 8, 4]`:
   - The function should return `10`.

### Algorithm Design
You need to implement a function within a class structure:

```java
class Solution {
    public int solution(int U, int[] weight) {
        // Your implementation goes here
    }
}
```

### Key Considerations
- At most two cars can be on the bridge at the same time.
- The cars must enter the bridge in the order they are queued.
- When a driver turns back, all drivers behind them move closer to the bridge, and the driver who turns back does not attempt to cross again.
"""

def solution(U, weight):
    cars_to_turn_back = 0
    bridge = []

    for car in weight:
        # Remove a car from the bridge if it's full
        if len(bridge) == 2:
            bridge.pop(0)

        # Try to add the current car
        current_bridge_weight = sum(bridge) if bridge else 0
        if current_bridge_weight + car <= U and len(bridge) < 2:
            bridge.append(car)
        else:
            cars_to_turn_back += 1

    return cars_to_turn_back


def test_solution():
    test_cases = [
        (9, [5, 3, 8, 1, 8, 7, 7, 6], 4),  # First car sequence
        (7, [7, 6, 5, 2, 7, 4, 5, 4], 5),  # Second car sequence
        (7, [3, 4, 3, 1], 0),  # All cars can pass
        (2, [8, 7, 5, 5, 6, 3, 9, 10, 8, 4], 10),  # All cars must turn back
        (1000000000, [1] * 100000, 0),  # Large input test
        (1, [1000000000] * 100000, 100000),  # Another large input test
    ]

    for i, (U, weight, expected) in enumerate(test_cases):
        result = solution(U, weight)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test case {i + 1}: {status}")
        print(f"  Input: U = {U}, weight = {weight[:10]}{'...' if len(weight) > 10 else ''}")
        print(f"  Expected: {expected}")
        print(f"  Got: {result}")
        print()


if __name__ == "__main__":
    test_solution()