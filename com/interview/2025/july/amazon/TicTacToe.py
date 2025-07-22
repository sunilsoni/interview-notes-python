class TicTacToe:
    """
    A class representing the Tic-Tac-Toe game engine.
    Handles game logic, move validation, and winner determination.
    """

    def __init__(self):
        """Initialize an empty 3x3 game board and set first player"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.moves_count = 0

    def make_move(self, row: int, col: int) -> bool:
        """
        Attempt to make a move at the specified position
        Returns True if move is valid, False otherwise
        """
        if not (0 <= row < 3 and 0 <= col < 3):
            return False

        if self.board[row][col] != ' ':
            return False

        self.board[row][col] = self.current_player
        self.moves_count += 1
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_winner(self) -> str:
        """
        Check if there's a winner
        Returns: 'X' or 'O' if there's a winner, 'Draw' if game is drawn,
        'Ongoing' if game is still in progress
        """
        # Check rows
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != ' ':
                return row[0]

        # Check columns
        for col in range(3):
            if (self.board[0][col] == self.board[1][col] ==
                    self.board[2][col] != ' '):
                return self.board[0][col]

        # Check diagonals
        if (self.board[0][0] == self.board[1][1] ==
                self.board[2][2] != ' '):
            return self.board[0][0]

        if (self.board[0][2] == self.board[1][1] ==
                self.board[2][0] != ' '):
            return self.board[0][2]

        if self.moves_count == 9:
            return 'Draw'

        return 'Ongoing'

    def display_board(self):
        """Print the current state of the game board"""
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)


def main():
    """Main function to test the TicTacToe implementation"""

    def run_test_case(moves, expected_result):
        game = TicTacToe()
        for row, col in moves:
            game.make_move(row, col)
        result = game.check_winner()
        print(f"\nTest Case: {moves}")
        game.display_board()
        print(f"Expected: {expected_result}, Got: {result}")
        print(f"Test {'PASSED' if result == expected_result else 'FAILED'}")

    # Test Cases
    test_cases = [
        # Horizontal win
        ([(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)], 'X'),

        # Vertical win
        ([(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 'X'),

        # Diagonal win
        ([(0, 0), (1, 0), (1, 1), (2, 0), (2, 2)], 'X'),

        # Draw game
        ([(0, 0), (0, 1), (0, 2), (1, 1), (1, 0),
          (1, 2), (2, 1), (2, 0), (2, 2)], 'Draw'),

        # Ongoing game
        ([(0, 0), (1, 1)], 'Ongoing')
    ]

    print("Running Test Cases...")
    for moves, expected in test_cases:
        run_test_case(moves, expected)


if __name__ == "__main__":
    main()
