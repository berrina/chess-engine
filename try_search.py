from engine.board import Board
from engine.search import find_best_move

b = Board()
move = find_best_move(b, depth=2)
print(move)