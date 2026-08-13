from engine.board import Board

def minimax(board, depth, maximizing): 
        if depth == 0: 
            return board.evaluate()

        moves = board.legal_moves() 

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
    for move in board.legal_moves(): 
        child = board.make_move(move) 
        score = minimax(child, depth - 1, maximizing= False)
        if score > best_score: 
            best_score = score 
            best_move = move 
        return best_move 



