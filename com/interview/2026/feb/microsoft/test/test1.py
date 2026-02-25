class Connect4: # Define the blueprint class for our Connect 4 game
    def __init__(self): # The constructor method that sets up a new game
        self.rows = 6 # Set the standard number of rows to 6
        self.cols = 7 # Set the standard number of columns to 7
        self.board = [] # Initialize an empty list that will become our 2D matrix
        for r in range(self.rows): # Loop 6 times, once for each row
            row_list = [] # Create a new empty list to represent a single row
            for c in range(self.cols): # Loop 7 times, once for each column spot
                row_list.append('.') # Add a dot '.' to represent an empty space
            self.board.append(row_list) # Add the completed row to our main board list

    def drop_piece(self, col, piece): # Method to handle a player dropping a piece
        if col < 0 or col >= self.cols: # Check if the chosen column is outside the board limits
            return False # Return False because the move is invalid
        for r in range(self.rows - 1, -1, -1): # Loop backwards from the bottom row (5) up to the top row (0)
            if self.board[r][col] == '.': # Check if the current spot in this column is empty
                self.board[r][col] = piece # If empty, place the player's piece ('R' or 'Y') here
                return True # Return True to indicate a successful move
        return False # Return False if the loop finishes without finding an empty spot (column is full)

    def check_win(self, piece): # Method to check if a specific player has won
        # 1. Check Horizontal win
        for c in range(self.cols - 3): # Loop through columns where a horizontal win can start (0, 1, 2, 3)
            for r in range(self.rows): # Loop through every row on the board
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece: # Check if 4 adjacent horizontal spots match the piece
                    return True # If we found 4 in a row, return True (Player wins)

        # 2. Check Vertical win
        for c in range(self.cols): # Loop through every column on the board
            for r in range(self.rows - 3): # Loop through rows where a vertical win can start (0, 1, 2)
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece: # Check if 4 adjacent vertical spots match the piece
                    return True # If we found 4 in a column, return True (Player wins)

        # 3. Check Diagonal (sloping up-right) win
        for c in range(self.cols - 3): # Loop through valid starting columns for this diagonal (0, 1, 2, 3)
            for r in range(3, self.rows): # Loop through valid starting rows (3, 4, 5) because we go UP the board (decreasing row index)
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece: # Check the diagonal spots
                    return True # If we found 4 diagonally, return True (Player wins)

        # 4. Check Diagonal (sloping down-right) win
        for c in range(self.cols - 3): # Loop through valid starting columns for this diagonal (0, 1, 2, 3)
            for r in range(self.rows - 3): # Loop through valid starting rows (0, 1, 2) because we go DOWN the board (increasing row index)
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece: # Check the diagonal spots
                    return True # If we found 4 diagonally, return True (Player wins)

        return False # If all checks finish and no win is found, return False


def run_tests():  # Define a function to hold our test cases
    print("Running Tests...")  # Print a starting message

    # Test 1: Basic Drop and Vertical Win
    game1 = Connect4()  # Create a fresh game board
    game1.drop_piece(0, 'R')  # Drop Red in col 0
    game1.drop_piece(0, 'R')  # Drop Red in col 0
    game1.drop_piece(0, 'R')  # Drop Red in col 0
    game1.drop_piece(0, 'R')  # Drop Red in col 0
    if game1.check_win('R') == True:  # Check if Red won vertically
        print("Test 1 (Vertical Win): PASS")  # Print pass message
    else:  # If it doesn't return True
        print("Test 1 (Vertical Win): FAIL")  # Print fail message

    # Test 2: Horizontal Win
    game2 = Connect4()  # Create a fresh game board
    game2.drop_piece(2, 'Y')  # Drop Yellow in col 2
    game2.drop_piece(3, 'Y')  # Drop Yellow in col 3
    game2.drop_piece(4, 'Y')  # Drop Yellow in col 4
    game2.drop_piece(5, 'Y')  # Drop Yellow in col 5
    if game2.check_win('Y') == True:  # Check if Yellow won horizontally
        print("Test 2 (Horizontal Win): PASS")  # Print pass message
    else:  # If it doesn't return True
        print("Test 2 (Horizontal Win): FAIL")  # Print fail message

    # Test 3: Diagonal Win and Boundary check
    game3 = Connect4()  # Create a fresh game board
    # Building a diagonal requires dropping pieces to create height
    game3.drop_piece(0, 'R')  # Col 0 height 1

    game3.drop_piece(1, 'Y')  # Col 1 height 1
    game3.drop_piece(1, 'R')  # Col 1 height 2

    game3.drop_piece(2, 'Y')  # Col 2 height 1
    game3.drop_piece(2, 'Y')  # Col 2 height 2
    game3.drop_piece(2, 'R')  # Col 2 height 3

    game3.drop_piece(3, 'Y')  # Col 3 height 1
    game3.drop_piece(3, 'Y')  # Col 3 height 2
    game3.drop_piece(3, 'Y')  # Col 3 height 3
    game3.drop_piece(3, 'R')  # Col 3 height 4 (completes diagonal)

    if game3.check_win('R') == True:  # Check if Red won diagonally
        print("Test 3 (Diagonal Win): PASS")  # Print pass message
    else:  # If it doesn't return True
        print("Test 3 (Diagonal Win): FAIL")  # Print fail message

    # Test 4: Full Column (Large Data / Edge Case)
    game4 = Connect4()  # Create a fresh game board
    for _ in range(6):  # Loop 6 times to fill a column completely
        game4.drop_piece(0, 'R')  # Drop Red in col 0
    is_dropped = game4.drop_piece(0, 'Y')  # Try to drop a 7th piece in the full column
    if is_dropped == False:  # Check if the game correctly rejected the move
        print("Test 4 (Full Column Reject): PASS")  # Print pass message
    else:  # If it allowed the move
        print("Test 4 (Full Column Reject): FAIL")  # Print fail message


if __name__ == "__main__":  # Standard Python line to check if this file is run directly
    run_tests()  # Execute our test function