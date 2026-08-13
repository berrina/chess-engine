from engine.board import Board

def minimax(board, depth, maximizing): 
        # a recursive function that implement the minimax algorithm to find the best move for the current player 
        # builds a tree of possible moves and assumes one player is trying to maximize their score while the otehr is trying to minimze it [in this case they are trying to minimze the opponent's score]
        # at a maximizer level, the parent node will choose the highest value child, and at minimizer level it picks the lowest value child. 
        if depth == 0: 
            return board.evaluate()

        moves = board.get_truly_legal_moves() 

        if maximizing: 
            best = float('-inf') 

            for move in moves: 
                child = board.make_move(move) 
                score = minimax(child, depth - 1, maximizing= False)

                best = max(best, score)

            return best
        else: 
            best = float('inf') 

            for move in moves: 
                child = board.make_move(move) 
                score = minimax(child, depth - 1, maximizing= True)

                best = min(best, score)

            return best

def find_best_move(board, depth): 
    best_score = float('-inf')
    best_move = None
    for move in board.get_truly_legal_moves(): 
        child = board.make_move(move) 
        score = minimax(child, depth - 1, maximizing= False)
        if score > best_score: 
            best_score = score 
            best_move = move 
        return best_move 




