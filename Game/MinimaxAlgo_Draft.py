import math


def Minimax(Board, MaxDepth, Depth):
    if board.IsGameOver() or Depth == MaxDepth:
        return ...?

        BestMove = None

        if Depth % 2 == 0:
            BestScore = (math.inf) * -1  # If acting as Opponant
        else:
            BestScore = math.inf

        for X in Board.PossibleMoves:

            NewBoard = Board.MakeMove(X)
            CurrScore, _ = Minimax(NewBoard, MaxDepth, Depth + 1)

            if Depth % 2 == 0:
                if CurrScore > BestScore:
                    BestScore = CurrScore
                    BestMove = X
            else:
                if CurrScore < BestScore:
                    BestScore = CurrScore
                    BestMove = X

        return BestScore, BestMove

    #   Depth = 0 for the current game state?
    #   Depth = 1, 3, 5... when predicting opponants actions
