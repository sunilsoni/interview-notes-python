class BoxFitting:
    def solution(self, operations):
        max_width = 0
        max_height = 0
        results = []

        for operation in operations:
            op_type, a, b = operation

            if op_type == 0:
                # Adding a new rectangle
                new_width = min(a, b)
                new_height = max(a, b)

                # Update the max_width and max_height to reflect the most restrictive rectangle
                max_width = max(max_width, new_width)
                max_height = max(max_height, new_height)

            elif op_type == 1:
                # Check if a rectangle can fit into all previously added rectangles
                query_width = min(a, b)
                query_height = max(a, b)

                if query_width <= max_width and query_height <= max_height:
                    results.append(True)
                else:
                    results.append(False)

        return results


# Test cases
if __name__ == "__main__":
    bf = BoxFitting()

    # Test case 1
    operations = [[0, 3, 3], [0, 5, 2], [1, 3, 2], [1, 2, 4]]
    print(bf.solution(operations))  # Expected output: [True, False]

    # Test case 2
    operations = [[1, 1, 1]]
    print(bf.solution(operations))  # Expected output: [True]

    # Test case 3
    operations = [[0, 100000, 100000]]
    print(bf.solution(operations))  # Expected output: []

    # Test case 4: Large inputs
    operations = [[0, 100, 200], [0, 150, 100], [1, 100, 150], [1, 200, 100]]
    print(bf.solution(operations))  # Expected output: [True, True]
