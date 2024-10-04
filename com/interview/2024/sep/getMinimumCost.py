#!/bin/python3
# A grid-like representation of an image is divided into n rows and m columns, with each cell containing pixel intensity values. The aim is to improve the visibility of specific objects in the image.
# Each pixel located at position (i, j) within the grid corresponds to a specific element in the image, where O≤i<nand 0 ≤j < m. The pixel's intensity or value is denoted by pixelintensitylil].
# The goal is to adjust the intensity of each pixel to ensure that no pixel in the previous rows, where 0≤ i < i in the same column, has a brightness higher or equal to the given pixel. To achieve this, a pixel's intensity can be increased at a cost of one unit per unit of increase.
# Determine the minimum cost to achieve the desired intensity in all n * m pixels.
# Example
# A grid with three rows and two columns is given: pixellntensity = [[2, 5], [7, 41, [3, 511.
# Currently, the intensity levels in cells (1, 1), (2, 0), and (2, 1) are not appropriate.
# 2
# 5
# 2
# 5
# 7
# 4
# 7
# 6
# 3
# 5
# 8
# 7
# Add 5 to the third row of the first column to get values 2, 7, and 8. Add 2 to the second and third rows in the second column to get values 5, 6, and 7. Both columns are now strictly increasing from top to
# bottom as required. The cost of the enhancements is 5 + 2 + 2 = 9, which is the minimum possible.
# Function Description
# Complete the function getMinimumCost in the editor below.
# getMinimumCost takes the following arguments:
# int pixellntensity[n][m]: a 2-D array representing the brightness of the image pixels
# Returns
# long_int: a long value denoting the minimum cost to achieve the desired visibility
#
#
# Constraints
# • 1 ≤ n, m≤ 105
# • 1 ≤ pixellntensity[illi]≤ 109
# • It is guaranteed that n * m ≤ 106
# • Input Format For Custom Testing
# The first line contains an integer n, representing the number of rows in the grid.
# The next line contains an integer m, representing the number of columns in the grid.
# Each of the following n lines represents the n rows, starting from top to bottom. Each line contains m space-separated integers, where the jth integer represents the intensity of the pixel located at the jth column of that row, where o≤j< m.
# • Sample Case 0
# Sample Input For Custom Testing
# STDIN
# ーーーーー
# 3
# 3
# 246
# 427
# 647
# FUNCTION
# →
# →
# →
# pixelIntensityl] size n = 3
# pixelIntensity[][] size m = 3
# pixelIntensity = 112, 4, 61, 14, 2, 71, 16, 4, 7111
# Sample Output
# 6
# Explanation
# Currently, the brightness levels in the cells (1, 1), (2, 1), and (2, 2) are not appropriate. Adding 3, 2, and 1 to those cells, respectively, is optimal.
# 2
# 4
# 6
# 2
# 4
# 6
# 4
# 2
# 7
# →
# 4
# 5
# 7
# 6
# 4
# 7
# 8
# 6
# 8
#
# • Sample Case 1
# Sample Input For Custom Testing
# STDIN
# FUNCTION
# - - -
# pixelIntensityl] size n = 3
# pixelIntensity][] size m = 5
# pixelIntensity = 112, 4, 6, 2, 91, 12, 8, 10, 2, 71, 18,
# 3
# 5
# 24629
# 10, 11, 8, 211
# 281027
# 8 10 11 8 2
# Sample Output
# 14
# Explanation
# Currently, the brightness levels in the cells (1, 0), (1, 3), (1, 4), and (2, 4) are not appropriate. Add 1, 1 3, and 9 to those cells, respectively, to get the desired visibility.
# 2
# 4
# 6
# 2
# 8
# 10
# 2
# 2
# 8
# 10
# 11
# 8
# 7
# 2
# →
# 2
# 3
# 8
# 4
# 8
# 6
# 2
# 3
# 9
# 10
# 10
# 11
# 10
# 8
# 11

class Solution:
    def getMinimumCost(self, pixelIntensity):
        n = len(pixelIntensity)
        m = len(pixelIntensity[0])
        total_cost = 0

        for j in range(m):
            max_intensity = 0
            for i in range(n):
                if pixelIntensity[i][j] <= max_intensity:
                    cost = max_intensity + 1 - pixelIntensity[i][j]
                    total_cost += cost
                    pixelIntensity[i][j] = max_intensity + 1
                max_intensity = pixelIntensity[i][j]

        return total_cost


def main():
    # Test cases
    test_cases = [
        [[2, 5], [7, 4], [3, 5]],
        [[2, 4, 6], [4, 2, 7], [6, 4, 7]],
        [[2, 4, 6, 2, 9], [2, 8, 10, 2, 7], [8, 10, 11, 8, 2]]
    ]

    solution = Solution()

    for i, case in enumerate(test_cases):
        result = solution.getMinimumCost(case)
        print(f"Test case {i + 1}: {result}")


if __name__ == "__main__":
    main()
