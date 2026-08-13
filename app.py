from flask import Flask, jsonify, request, render_template
from engine.board import Board
from engine.search import find_best_move

app = Flask(__name__)
game_board = Board()

def board_to_json(b):
    return {"squares": b.squares, "turn": b.turn}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/board")
def get_board():
    return jsonify(board_to_json(game_board))

@app.route("/api/move", methods=["POST"])
def make_move():
    global game_board
    data = request.json
    move = (tuple(data["from"]), tuple(data["to"]))

    if move not in game_board.get_truly_legal_moves():
        return jsonify({"error": "illegal move", **board_to_json(game_board)}), 400

    game_board = game_board.make_move(move)

    engine_move = None
    if game_board.turn == "b":
        engine_move = find_best_move(game_board, depth=3)
        if engine_move is not None:
            game_board = game_board.make_move(engine_move)

    return jsonify({"engine_move": engine_move, **board_to_json(game_board)})

@app.route("/api/reset", methods=["POST"])
def reset():
    global game_board
    game_board = Board()
    return jsonify(board_to_json(game_board))

if __name__ == "__main__":
    app.run(debug=True, port=5000)