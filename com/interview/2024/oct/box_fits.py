class Solution:
    def solution(self, operations):
        rectangles = []
        results = []

        def box_fits(box, rectangle):
            return (box[0] <= rectangle[0] and box[1] <= rectangle[1]) or \
                   (box[1] <= rectangle[0] and box[0] <= rectangle[1])

        for op in operations:
            if op[0] == 0:  # Create rectangle
                rectangles.append((op[1], op[2]))
            else:  # Check if box fits
                fits_all = all(box_fits((op[1], op[2]), rect) for rect in rectangles)
                results.append(fits_all)

        return results

# Test cases
s = Solution()
print(s.solution([[1, 1, 1]]))  # [True]
print(s.solution([[0, 100000, 100000]]))  # []
print(s.solution([[0, 3, 3], [0, 5, 2], [1, 3, 2], [1, 2, 4]]))  # [True, False]
