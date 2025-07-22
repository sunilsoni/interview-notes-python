"""
Tic-Tac-Toe Game Engine
Object-oriented design using Strategy and Command patterns for maintainability and extensibility.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict


class InvalidMoveError(Exception):
    """Raised when a move is illegal."""
    pass


@dataclass(frozen=True)
class Move:
    row: int
    col: int
    player: str  # 'X' or 'O'


class Board:
    """Represents the Tic-Tac-Toe board."""
    SIZE = 3

    def __init__(self):
        # Initialize empty board
        self._cells: List[List[str]] = [[' ' for _ in range(self.SIZE)] for _ in range(self.SIZE)]

    def is_empty(self, row: int, col: int) -> bool:
        return self._cells[row][col] == ' '

    def place(self, move: Move) -> None:
        if not (0 <= move.row < self.SIZE and 0 <= move.col < self.SIZE):
            raise InvalidMoveError(f"Move ({move.row},{move.col}) out of bounds.")
        if not self.is_empty(move.row, move.col):
            raise InvalidMoveError(f"Cell ({move.row},{move.col}) is already occupied.")
        self._cells[move.row][move.col] = move.player

    def is_full(self) -> bool:
        return all(cell != ' ' for row in self._cells for cell in row)

    def get_cell(self, row: int, col: int) -> str:
        return self._cells[row][col]


class WinStrategy(ABC):
    """Strategy interface for win detection."""

    @abstractmethod
    def is_winner(self, board: Board, player: str) -> bool:
        pass


class RowWinStrategy(WinStrategy):
    def is_winner(self, board: Board, player: str) -> bool:
        for r in range(board.SIZE):
            if all(board.get_cell(r, c) == player for c in range(board.SIZE)):
                return True
        return False


class ColumnWinStrategy(WinStrategy):
    def is_winner(self, board: Board, player: str) -> bool:
        for c in range(board.SIZE):
            if all(board.get_cell(r, c) == player for r in range(board.SIZE)):
                return True
        return False


class DiagonalWinStrategy(WinStrategy):
    def is_winner(self, board: Board, player: str) -> bool:
        # main diagonal
        if all(board.get_cell(i, i) == player for i in range(board.SIZE)):
            return True
        # anti-diagonal
        if all(board.get_cell(i, board.SIZE - 1 - i) == player for i in range(board.SIZE)):
            return True
        return False


class GameEngine:
    """Controls game flow: applies moves, checks rules, and tracks state."""
    def __init__(self, win_strategies: List[WinStrategy]) -> None:
        self._board = Board()
        self._win_strategies = win_strategies
        self._winner: Optional[str] = None

    def make_move(self, move: Move) -> None:
        # Prevent moves after game end
        if self._winner is not None:
            raise InvalidMoveError(f"Game already finished. Winner: {self._winner}")
        # Place on board
        self._board.place(move)
        # Check for win
        if any(strategy.is_winner(self._board, move.player) for strategy in self._win_strategies):
            self._winner = move.player
        # Check for draw
        elif self._board.is_full():
            self._winner = 'Draw'

    def get_winner(self) -> Optional[str]:
        """Returns 'X', 'O', 'Draw', or None if game ongoing."""
        return self._winner

    def reset(self) -> None:
        """Resets the game to initial state."""
        self.__init__(self._win_strategies)


# --- Example usage in __main__ -------------------------------------------
if __name__ == '__main__':
    # Compose win strategies (easily extendable)
    strategies = [RowWinStrategy(), ColumnWinStrategy(), DiagonalWinStrategy()]
    engine = GameEngine(strategies)

    # Sample moves
    moves = [Move(0, 0, 'X'), Move(1, 1, 'O'), Move(0, 1, 'X'),
             Move(2, 2, 'O'), Move(0, 2, 'X')]  # X wins

    for m in moves:
        try:
            engine.make_move(m)
            if engine.get_winner():
                print(f"Game Over: {engine.get_winner()} wins!")
                break
        except InvalidMoveError as e:
            print(f"Invalid move: {e}")

    if not engine.get_winner():
        print("Game continues or draw.")
