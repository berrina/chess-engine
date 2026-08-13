from engine.board import Board
from engine.search import find_best_move


b = Board()
print(b.pawn_moves(1, 4))  # e2 pawn, starting position -- no enemy diagonally, so still just forward moves