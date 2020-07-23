import tictactoe

board = tictactoe.Board()
board.board[0] = ['O', ' ', 'X']
board.board[1] = ['X', ' ', 'X']
board.board[2] = [' ', 'O', 'O']
maximum = board.whos_turn()
minimum = board.whos_not_turn()
minimax = tictactoe.MiniMax(board.board, 'root', maximum, minimum)

