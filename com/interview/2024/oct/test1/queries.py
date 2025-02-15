"""

Python3 Task:
You are monitoring the building density in a district of houses. The district is represented as a number line, where each house is located at some integer along the line. Imagine that some of the houses are gradually being destroyed over time.
You are given houses, an array of integers representing the initial locations of all houses in the district. You are also given queries, an array of integers representing the locations of the houses which will be destroyed, sorted by the order in which they are destroyed. After each house is destroyed, your task is to find the number of house segments remaining within the district. House segments are defined as one or more adjacent houses which do not have neighbors on either side.
Return an array of integers representing the number of house segments after each house from queries is destroyed.
NOTE: It's guaranteed that all houses are in distinct locations. The locations of all houses in queries are present in houses, and also distinct.
Example
• For houses = [1, 2, 3, 6, 7, 9] and queries = [6, 3, 7, 2, 9, 1] , the output should be solution (houses, queries) = [3, 3, 2, 2, 1, 0] .
• Expand to see the example video.
Initially, there are 6 houses in the district at positions 1, 2, 3, 6, 7, and 9, which form three house segments: [1, 2, 3], [6, 7] , and [9] . Let's consider what happens after each step in queries
• After queries [0] = 6, the house at location 6 is removed, and the remaining houses are in three segments: [1, 2, 3] , [7], and [9], so the output is 3 .
• After queries [1] = 3, the house at location 3 is removed, and the remaining houses are still in three segments: [1, 2] , [7] , and [9], so the output is also 3 .
• After queries [2] = 7, the house at location 7 is removed, and the remaining houses are now in two segments: [1, 2] and [9], so the output is 2 .
• After queries [3] = 2, the house at location 2 is removed, and the remaining houses are still in two segments: [1] and [9] , so the output is 2
• After queries [4] = 9, only one house in position 1 remains, which can only be in one segment, so the output is 1.
• After queries [5] = 1, there are no more houses in the district, so the output is o .
Altogether, the final answer is [3, 3, 2, 2, 1, 0] .
• For houses = [2, 4, 5, 6, 7] and queries = [5, 6, 2], the output should be solution (houses, queries) = [3, 3, 2] .
• Expand to see the example video.
Initially there are two house segments: [2] and [4, 5, 6, 7]. Let's consider what happens after each step in queries :
• After queries [0] = 5, the house at location 5 is removed, and the remaining houses are now in three segments: [2], [4] and [6, 7] , so the output is 3 .
• After queries 111 = 6, the house at location 6 is removed, and the remaining houses are stil in three segments: 121 14] and 171, so the output is 3
• After queries [2] = 2, the house at location 2 is removed, and the remaining houses are now in two segments: [4] and [7], so the output is 2

Altogether, the final answer is [3, 3, 2]
Input/Output
• [execution time limit] 4 seconds (py3)
• [memory limit] 1 GB
• [input] array.integer houses
A list of unique integers representing the coordinates of houses in the district.
Guaranteed constraints:
1 ≤ houses. length ≤ 10 power 5
-10 power 9 ≤ houses [i] ≤ 10 power 9
• [input] array.integer queries
A list representing the coordinates of the houses scheduled to be destroyed. It is guaranteed that all the coordinates are unique and are present in houses .
Guaranteed constraints:
1 ≤ queries. length ≤ houses. length .
• [output] array.integer
Return a list of size queries. length such that the ith element contains the number of house segments (described above) after the ith query.

"""


def solution(houses, queries):
    # Sort houses for efficient processing
    houses.sort()

    # Create a set for quick lookup and removal
    house_set = set(houses)

    # Initialize segments
    segments = count_segments(houses)

    result = []
    for query in queries:
        # Remove the house
        house_set.remove(query)

        # Update segments
        left = query - 1 in house_set
        right = query + 1 in house_set

        if left and right:
            segments += 1
        elif not left and not right:
            segments -= 1

        result.append(segments)

    return result


def count_segments(houses):
    if not houses:
        return 0

    segments = 1
    for i in range(1, len(houses)):
        if houses[i] - houses[i - 1] > 1:
            segments += 1

    return segments


def main():
    # Test case 1
    houses1 = [1, 2, 3, 6, 7, 9]
    queries1 = [6, 3, 7, 2, 9, 1]
    result1 = solution(houses1, queries1)
    print("Test case 1:", result1)
    assert result1 == [3, 3, 2, 2, 1, 0], "Test case 1 failed"

    # Test case 2
    houses2 = [2, 4, 5, 6, 7]
    queries2 = [5, 6, 2]
    result2 = solution(houses2, queries2)
    print("Test case 2:", result2)
    assert result2 == [3, 3, 2], "Test case 2 failed"

    # Additional test case: Edge case with single house
    houses3 = [1]
    queries3 = [1]
    result3 = solution(houses3, queries3)
    print("Test case 3:", result3)
    assert result3 == [0], "Test case 3 failed"

    # Additional test case: Large data set
    houses4 = list(range(1, 100001))
    queries4 = list(range(100000, 0, -1))
    result4 = solution(houses4, queries4)
    print("Test case 4: Large data set processed successfully")
    assert result4[-1] == 0, "Test case 4 failed"

    print("All test cases passed!")


if __name__ == "__main__":
    main()
