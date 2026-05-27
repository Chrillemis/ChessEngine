from libs.Training import *
from stockfish import Stockfish
from pathlib import Path


def play(Elo):
    #load best model
    saved_model = Model()

    script_dir = Path(__file__).resolve().parent

    #load best model path from your file
    with open(script_dir.parent / "data" / "savedModels" / "bestModel.txt", "r") as f:
        bestLoss = float(f.readline())
        model_path = Path(f.readline().strip())

    if not model_path.is_absolute():
        model_path = (script_dir / model_path).resolve()

    saved_model.load_state_dict(torch.load(str(model_path)))
    # test elo  against stockfish
    ELO_RATING = int(Elo)

    stockfish = Stockfish(path=r"C:\Users\lorentsen\Documents\AML\Project\stockfish\stockfish-windows-x86-64-avx2.exe")
    stockfish.reset_engine_parameters()
    stockfish.set_elo_rating(ELO_RATING)
    stockfish.set_skill_level(0)
    board = chess.Board()
    allMoves = [] #list of strings for saving moves for setting pos for stockfish

    MAX_NUMBER_OF_MOVES = 150
    for i in tqdm(range(MAX_NUMBER_OF_MOVES)): #set a limit for the game
    #first my ai move
        try:
            move = saved_model.predict(board)
            board.push(move)
            allMoves.append(str(move)) #add so stockfish can see
        except Exception as e:
            if str(e) == "object of type 'LegalMoveGenerator' has no len()":
                print("game over. You lost in", i, "moves")
            else:
                print("An error occurred:", str(e))
            break

        # #then get stockfish move
        stockfish.set_fen_position(board.fen())
        stockfishMove = stockfish.get_best_move_time(1)
        allMoves.append(stockfishMove)
        stockfishMove = chess.Move.from_uci(stockfishMove)
        board.push(stockfishMove)

    return board

if __name__ == "__main__":
    # create_main_screen()
    user_input = input("Please enter an integer of elo you want to play against:")
    try:
        ChessBoard = play(user_input)
    except Exception as e:
        print("An error occurred:", str(e))