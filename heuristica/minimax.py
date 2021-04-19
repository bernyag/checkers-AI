from copy import deepcopy
import pygame

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

def minimax(pos, profundidad, max_player, juego):
    if profundidad == 0 or pos.ganador() != None:
        return pos.evaluate(), pos
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(pos, WHITE, juego):
            evaluation = minimax(move, profundidad-1, False, juego)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(pos, RED, juego):
            evaluation = minimax(move, profundidad-1, True, juego)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board, juego, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, juego):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            draw_moves(juego, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, juego, skip)
            moves.append(new_board)
    
    return moves


def draw_moves(juego, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(juego.win)
    pygame.draw.circle(juego.win, (0,255,0), (piece.x, piece.y), 50, 5)
    juego.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)

