#!/usr/bin/env python3
"""
Tic-Tac-Toe Game Engine
Production-quality, with move validation, win/draw detection,
and simple main() PASS/FAIL test harness.
"""

from typing import List, Optional, Tuple


class InvalidMoveError(Exception):
    """Raised when a move is illegal (out of bounds or cell occupied)."""
    pass


class TicTacToeGame:
    """Encapsulates a 3x3 Tic-Tac-Toe board and game logic."""

    def __init__(self) -> None:
        """Initialize an empty board and no winner."""
        # 3×3 board, each cell is ' ', 'X', or 'O'
        self.board: List[List[str]] = [[' ' for _ in range(3)] for _ in range(3)]
        self.winner: Optional[str] = None  # 'X', 'O', 'Draw', or None

    def make_move(self, row: int, col: int, player: str) -> None:
        """
        Place player's symbol at (row, col).
        Raises InvalidMoveError if move is illegal or game over.
        Updates self.winner if this move ends the game.
        """
        # Check if game already over
        if self.winner is not None:
            raise InvalidMoveError(f"Game has finished with result: {self.winner}")

        # Check valid row/col
        if not (0 <= row < 3 and 0 <= col < 3):
            raise InvalidMoveError(f"Move ({row},{col}) out of bounds")
        # Check cell is free
        if self.board[row][col] != ' ':
            raise InvalidMoveError(f"Cell ({row},{col}) is already occupied")

        # Place symbol
        self.board[row][col] = player

        # Check for win
        if self._check_win(player):
            self.winner = player
        # Check for draw (board full, no winner)
        elif all(self.board[r][c] != ' ' for r in range(3) for c in range(3)):
            self.winner = 'Draw'

    def _check_win(self, player: str) -> bool:
        """
        Return True if player has 3 in a row.
        Checks rows, columns, and two diagonals.
        """
        b = self.board
        # Check rows and columns
        for i in range(3):
            if all(b[i][j] == player for j in range(3)):  # row i
                return True
            if all(b[j][i] == player for j in range(3)):  # col i
                return True
        # Check main diagonal
        if all(b[i][i] == player for i in range(3)):
            return True
        # Check anti-diagonal
        if all(b[i][2 - i] == player for i in range(3)):
            return True
        return False

    def get_winner(self) -> Optional[str]:
        """
        Returns 'X' or 'O' if there is a winner,
        'Draw' if board is full with no winner,
        or None if game is still in progress.
        """
        return self.winner

    def reset(self) -> None:
        """Clear the board and reset the game."""
        self.__init__()


def main():
    """Run a suite of test cases and report PASS/FAIL."""
    TestCase = Tuple[List[Tuple[int, int, str]], Optional[str]]
    test_cases: List[TestCase] = [
        # X wins horizontally on top row
        ([(0,0,'X'), (1,0,'O'),
          (0,1,'X'), (1,1,'O'),
          (0,2,'X')], 'X'),
        # O wins on anti-diagonal
        ([(0,0,'X'), (0,2,'O'),
          (1,1,'X'), (1,1,'O'),  # invalid: same cell -> catch exception
         ], None),
        # Draw game
        ([(0,0,'X'), (0,1,'O'), (0,2,'X'),
          (1,1,'O'), (1,0,'X'), (1,2,'O'),
          (2,1,'X'), (2,0,'O'), (2,2,'X')], 'Draw'),
        # X wins vertically
        ([(0,2,'X'), (0,0,'O'),
          (1,2,'X'), (1,0,'O'),
          (2,2,'X')], 'X'),
        # Invalid move out of bounds
        ([(3,3,'X')], None),
    ]

    for idx, (moves, expected) in enumerate(test_cases, 1):
        game = TicTacToeGame()
        result: Optional[str] = None
        passed = True
        try:
            for row, col, player in moves:
                game.make_move(row, col, player)
            result = game.get_winner()
        except InvalidMoveError as e:
            result = None
        finally:
            # Compare result to expected
            if result != expected:
                passed = False
            status = "PASS" if passed else "FAIL"
            print(f"Test {idx}: Expected={expected!r}, Got={result!r} → {status}")

if __name__ == '__main__':
    main()