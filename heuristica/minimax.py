from copy import deepcopy
import pygame

CLARO = (117,173,224)
BLANCO = (255, 255, 255)

def minimax(pos, profundidad, max_player, juego):
    if profundidad == 0 or pos.ganador() != None:
        return pos.evalua(), pos
    
    if max_player:
        maximo = float('-100000000')
        movimiento_optimo = None
        for movimiento in get_movimientos(pos, BLANCO, juego):
            evaluacion = minimax(movimiento, profundidad-1, False, juego)[0]
            maximo = max(maximo, evaluacion)
            if maximo == evaluacion:
                movimiento_optimo = movimiento
        
        return maximo, movimiento_optimo
    else:
        minimo = float('100000000')
        movimiento_optimo = None
        for movimiento in get_movimientos(pos, CLARO, juego):
            evaluacion = minimax(movimiento, profundidad-1, True, juego)[0]
            minimo = min(minimo, evaluacion)
            if minimo == evaluacion:
                movimiento_optimo = movimiento
        
        return minimo, movimiento_optimo


def simula_movimiento(ficha, movimiento, tablero, juego, skip):
    tablero.movimiento(ficha, movimiento[0], movimiento[1])
    if skip:
        tablero.elimina(skip)
    return tablero


def get_movimientos(tablero, color, juego):
    movimientos = []

    for ficha in tablero.get_todas_fichas(color):
        movimientos_validos = tablero.get_movimientos_validos(ficha)
        for movimiento, skip in movimientos_validos.items():
            temp_tablero = deepcopy(tablero)
            temp_ficha = temp_tablero.get_ficha(ficha.fila, ficha.col)
            nuevo_tablero = simula_movimiento(temp_ficha, movimiento, temp_tablero, juego, skip)
            movimientos.append(nuevo_tablero)
    return movimientos