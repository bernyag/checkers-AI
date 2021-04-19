from copy import deepcopy
import pygame

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

def minimax(pos, profundidad, max_player, juego):
    if profundidad == 0 or pos.ganador() != None:
        return pos.calcula_costo(), pos
    
    if max_player:
        maxEval = float('-inf')
        movimiento_optimo = None
        for movimiento in get_movimientos(pos, BLANCO, juego):
            evaluacion = minimax(movimiento, profundidad-1, False, juego)[0]
            maxEval = max(maxEval, evaluacion)
            if maxEval == evaluacion:
                movimiento_optimo = movimiento
        
        return maxEval, movimiento_optimo
    else:
        minEval = float('inf')
        movimiento_optimo = None
        for movimiento in get_movimientos(pos, RED, juego):
            evaluacion = minimax(movimiento, profundidad-1, True, juego)[0]
            minEval = min(minEval, evaluacion)
            if minEval == evaluacion:
                movimiento_optimo = movimiento
        
        return minEval, movimiento_optimo


def simula_movimiento(pieza, movimiento, tablero, juego, skip):
    tablero.movimiento(pieza, movimiento[0], movimiento[1])
    if skip:
        tablero.remove(skip)

    return tablero


def get_movimientos(tablero, color, juego):
    movimientos = []

    for pieza in tablero.get_all_pieces(color):
        movimientos_validos = tablero.get_movimientos_validos(pieza)
        for movimiento, skip in movimientos_validos.items():
            dibuja_movimientos(juego, tablero, pieza)
            temp_tablero = deepcopy(tablero)
            temp_pieza = temp_tablero.get_pieza(piece.row, pieza.col)
            nuevo_tablero = simula_movimiento(temp_pieza, movimiento, temp_tablero, juego, skip)
            movimientos.append(nuevo_tablero)
    
    return movimientos


def dibuja_movimientos(juego, tablero, pieza):
    movimientos_validos = tablero.get_movimientos_validos(pieza)
    tablero.draw(juego.win)
    pygame.draw.circle(juego.win, (0,255,0), (pieza.x, pieza.y), 50, 5)
    juego.draw_movimientos_validos(movimientos_validos.keys())
    pygame.display.update()
    #pygame.time.delay(100)

