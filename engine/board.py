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

    
    def is_enemy_piece(self, piece): 
        # check if the piece belongs to oppoenent based on the current turn and case of the piece
        if self.turn == "w": 
            return piece is not None and piece.islower() #black pieces are lower caps 
        else: 
            return piece is not None and piece.isupper() # white pieces are upper case
            

# move generation will be for 6 pieces: pawn, knight, bishop, rook, queen, king

    def knight_moves(self, row, col):
    # returns the list of valid knight moves from the given position of row and col
        moves = []
        knight_offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for (dr, dc) in knight_offsets:
                new_row, new_col = row + dr, col + dc
                if self.is_on_board(new_row, new_col):
                    target_piece = self.piece_at(new_row, new_col)
                    if target_piece is None: 
                        moves.append((new_row, new_col)) # valid move (empty square)
                    elif self.is_enemy_piece(target_piece): 
                        moves.append((new_row, new_col)) # valid move (capture) 
                    else: 
                        pass # own piece, so skip it 
        return moves 

                    
        return moves

b = Board()
print(b.knight_moves(0, 1))  # White's knight starts on b1, that's row 0, col 1 in your layout

   
          

