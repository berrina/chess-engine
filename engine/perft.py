from engine.board import Board

def perft(board, depth):
    # a recursive function that counts the number of possible moves from a given board position up to a certaind depth 
    if depth == 0:
        return 1
    count = 0
    for move in board.get_truly_legal_moves():
        child = board.make_move(move)
        count += perft(child, depth - 1)
    return count

if __name__ == "__main__":
    b = Board()
    for d in range(1, 4):
        print(f"depth {d}: {perft(b, d)}")