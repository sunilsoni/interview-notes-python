def solution(matrix, commands):
    for cmd in commands:
        parts = cmd.split()
        action = parts[0]

        if action == "swapRows":
            r1, r2 = int(parts[1]), int(parts[2])
            matrix[r1], matrix[r2] = matrix[r2], matrix[r1]

        elif action == "swapColumns":
            c1, c2 = int(parts[1]), int(parts[2])
            for row in matrix:
                row[c1], row[c2] = row[c2], row[c1]

        elif action == "reverseRow":
            r = int(parts[1])
            matrix[r] = matrix[r][::-1]

        elif action == "reverseColumn":
            c = int(parts[1])
            col_data = [matrix[r][c] for r in range(len(matrix))]
            col_data.reverse()
            for r in range(len(matrix)):
                matrix[r][c] = col_data[r]

        elif action == "rotate90Clockwise":
            # Transpose and reverse each row
            matrix = [list(row) for row in zip(*matrix[::-1])]

    return matrix


def test():
    # Example 1
    m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    c1 = ["swapRows 0 2", "swapColumns 1 2", "reverseRow 0", "reverseColumn 2", "rotate90Clockwise"]
    exp1 = [[1, 4, 8], [3, 6, 9], [7, 5, 2]]

    # Example 2 (from screenshot)
    m2 = [[1, 4, 2], [5, 2, 7]]
    c2 = ["reverseRow 0", "swapColumns 0 2", "reverseColumn 1", "rotate90Clockwise"]
    exp2 = [[7, 1], [4, 2], [5, 2]]

    cases = [(m1, c1, exp1), (m2, c2, exp2)]

    for i, (m, c, expected) in enumerate(cases):
        res = solution(m, c)
        print(f"Test {i + 1}: {'PASS' if res == expected else 'FAIL'}")
        if res != expected:
            print(f"  Got: {res}\n  Exp: {expected}")


if __name__ == "__main__":
    test()