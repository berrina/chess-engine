# engine/board.py
import copy

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
            
    def is_own_piece(self, piece): 
        #check if piece equals to to the current turn and case of the piece 
        if self.turn == "w": 
            return piece is not None and piece.isupper() 
        else: 
            return piece is not None and piece.islower() 

        
# move generation will be for 6 pieces: pawn, knight!, bishop-, rook-, queen-, king

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
    
    def sliding_moves (self, row, col, directions): 
        # returns the list of valid sliding moves (bishop, rook, queen) from the given position of the piece at row and col, based on the provided directions
        moves = [] 
        for (dr, dc) in directions: 
           new_row, new_col = row + dr, col + dc
           while self.is_on_board(new_row, new_col):
               target_piece = self.piece_at(new_row, new_col)
               if target_piece is None: 
                   moves.append((new_row, new_col)) # valud move (empty square) 
               elif self.is_enemy_piece(target_piece): 
                   moves.append((new_row, new_col)) # valid move (capture) 
                   break # cant move past enemy space 
               else: 
                   break # own piece, so stop sliding in this direction 
               new_row += dr
               new_col += dc

        return moves  

    def rook_moves (self, row, col): 
        # rook moves horizntally and vertically, so we call upon function above (sliding_moves) 
        directions = [(-1,0), (1,0), (0,-1), (0,1)] # up, down, left, right 
        return self.sliding_moves(row, col, directions) 
    
    def bishop_moves (self, row, col): 
        # bishop moves diagonally, so we call upon same sliding function above 
        directions = [(-1,-1), (-1,1), (1,-1), (1,1)] # directions for diagonal movement 
        return self.sliding_moves(row, col, directions) 

    def queen_moves (self, row, col): 
        # queen moves like both rook and bishop, so we combine their directions 
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)] # all 8 directions 
        return self.sliding_moves(row, col, directions)


    def king_moves (self, row, col): 
        # king moves one square in any direction, so we limit to one step 
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)] 
        moves = [] 
        for (dr, dc) in directions: 
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

# the + and - matter most in terms of like moving up because pawns are the one piece where color changes the actual shape of movement, not just who owns what
# White pawns move with +row (toward row 7), Black pawns move with -row (toward row 0)

    def pawn_moves (self, row, col): 
        # returns the list fo valid pawn moves from teh given position 
        moves = []
        piece = self.piece_at(row, col)
        if piece is None: 
            return moves # no pawn at this position 
        elif piece == "P": # a white pawn 
            # move forward one square 
            if self.is_on_board(row + 1, col) and self.piece_at(row + 1, col) is None: 
                moves.append((row + 1, col))
                # move forward two squares from starting position 
                if row == 1 and self.piece_at(row + 2, col) is None: 
                    moves.append((row + 2, col)) 
        elif piece == "p": # a black pawn
            # move foward one square 
            if self.is_on_board(row - 1, col) and self.piece_at(row - 1, col) is None: 
                moves.append((row - 1, col))
                # move forward two squares from starting position 
                if row == 6 and self.piece_at(row - 2, col) is None: 
                    moves.append((row - 2, col)) 
        return moves 

    def legal_moves(self):
        # returns the list of legal moves, as ((from_row, from_col), (to_row, to_col)) pairs
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.piece_at(row, col)
                if piece is None:
                    continue
                if self.is_own_piece(piece):
                    if piece.lower() == "p":
                        destinations = self.pawn_moves(row, col)
                    elif piece.lower() == "n":
                        destinations = self.knight_moves(row, col)
                    elif piece.lower() == "b":
                        destinations = self.bishop_moves(row, col)
                    elif piece.lower() == "r":
                        destinations = self.rook_moves(row, col)
                    elif piece.lower() == "q":
                        destinations = self.queen_moves(row, col)
                    elif piece.lower() == "k":
                        destinations = self.king_moves(row, col)
                    else:
                        destinations = []

                    for destination in destinations:
                        all_moves.append(((row, col), destination))

        return all_moves

    def make_move(self, move):
        # move the piece from (from_row, from_col) to (to_row, to_col) 
        from_square, to_square = move 
        from_row, from_col = from_square 
        to_row, to_col = to_square 

        new_board = copy.deepcopy(self)

        piece = new_board.piece_at(from_row, from_col)

        new_board.squares[to_row][to_col] = piece 
        new_board.squares[from_row][from_col] = None 

        new_board.turn = "b" if new_board.turn == "w" else "w"

        return new_board         

b = Board()
move = ((1, 0), (3, 0))  # white pawn from a2 forward two squares to a4
new_b = b.make_move(move)
print(new_b)
print(new_b.turn)
print(b)  # confirm original board is UNCHANGED


          

