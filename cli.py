from engine.board import Board
from engine.search import find_best_move
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_help():
    print("Enter moves as: from_row,from_col to_row,to_col  (e.g. 1,4 3,4)")
    print("Rows/cols are 0-7. Type 'quit' to exit.")

def parse_move(text):
    try:
        from_part, to_part = text.strip().split(" ")
        from_row, from_col = map(int, from_part.split(","))
        to_row, to_col = map(int, to_part.split(","))
        return ((from_row, from_col), (to_row, to_col))
    except Exception:
        return None

def main():
    board = Board()
    print_help()
    print(board)

    while True:
        if board.turn == "w":
            text = input("\nYour move (White): ")
            if text.strip().lower() == "quit":
                break
            move = parse_move(text)
            if move is None or move not in board.get_truly_legal_moves():
                print("Invalid move, try again.")
                continue
            board = board.make_move(move)
        else:
            print("\nEngine thinking...")
            move = find_best_move(board, depth=3)
            if move is None:
                print("No legal moves -- game over.")
                break
            print(f"Engine plays: {move}")
            board = board.make_move(move)

        print(board)

if __name__ == "__main__":
    main()

# to run the program on terminal 
# input coordinates of piece you want to move and to where 
# ex: 1,4 3,4 
# to rerun the board do : python3 cli.py