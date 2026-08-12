# engine/board.py

class Board:
    def __init__(self):
        # 8x8 grid: self.squares[row][col]
        # Use None for empty, or a piece string like "wP", "bK", "wN", etc.
        # row 0 = rank 8 (black's back rank), row 7 = rank 1 (white's back rank) -- pick a convention and stay consistent
        self.squares = self._create_starting_position()

        self.turn = "w"  # "w" or "b"

        self.castling_rights = {
            "wK": True, "wQ": True,   # white kingside / queenside
            "bK": True, "bQ": True,
        }

        self.en_passant_target = None  # None, or a (row, col) tuple

        self.halfmove_clock = 0

    def _create_starting_position(self):
        # return the standard starting 8x8 layout
        return [
        # uppercase = white, lowercase = black
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "n", "b", "q", "k", "b", "n", "r"]
        ]
        

    def piece_at(self, row, col):
        # return whatever's at self.squares[row][col]
        return self.squares[row][col]

    def is_on_board(self, row, col):
        # bounds check -- 0 <= row < 8 and 0 <= col < 8
        return 0 <= row < 8 and 0 <= col < 8 
    # index of rows and columns is till 7, (0-7) so we make sure that the piece is valid 

    def __str__(self):
        # return a readable text representation for debugging
        # to print the board constantly while testing
        board_str = ""
        for row in self.squares:  
            for square in row: 
                if square is None: 
                    board_str += ". " # empty square 
                else: 
                    board_str += square + " " # piece 
            board_str += "\n" # new line after each row 
        return board_str 

b = Board()
print(b)