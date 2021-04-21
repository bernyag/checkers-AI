from copy import deepcopy
import pygame

CLARO = (117,173,224)
BLANCO = (255, 255, 255)

def ab_pruning(pos, profundidad, max_player, juego, alpha, beta):
    if profundidad == 0 or pos.ganador() != None:
        return pos.evalua(), pos
    
    if max_player:
        maximo = float('-100000000')
        movimiento_optimo = None
        for movimiento in get_movimientos(pos, BLANCO, juego):
            evaluacion = ab_pruning(movimiento, profundidad-1, False, juego, maximo, beta)[0]
            if evaluacion > beta:
                return evaluacion, movimiento
            maximo = max(maximo, evaluacion)
            if maximo == evaluacion:
                movimiento_optimo = movimiento
        return maximo, movimiento_optimo
    else:
        minimo = float('100000000')
        movimiento_optimo = None

        #movimiento es [f1_izq] getmov [[f1_izq][f1_der][f2_izq][f2_der]]
        for movimiento in get_movimientos(pos, CLARO, juego):
            evaluacion = ab_pruning(movimiento, profundidad-1, True, juego, alpha, minimo)[0]
            
            ##en misma ficha, quieres minimo
            ##cuando acabas de checar posibles movs de una ficha, asignar el min a alfa 
            ##si ya estas en siguiente ficha, y evaluacion es mas chico que tu minimo anterior, pruneas
            #si estas checando la misma ficha
            if evaluacion < alpha:
                return evaluacion, movimiento

            minimo = min(minimo, evaluacion)
           

            #if estas checando ultimo mov de misma ficha
                #alfa = minimo            

            #if cambiaste de ficha que se esta checando
                #for movimientos de nueva ficha
                #if alfa>minimo
                # 8
                # 10 7 9 
                    #prunear -> cambiar a siguiente ficha y sus movimientos

            if minimo == evaluacion:
                movimiento_optimo = movimiento
        
        return minimo, movimiento_optimo

def ab_prunning(pos, profundidad, max_player, juego):
    if profundidad == 0 or pos.ganador() != None:
        return pos.evalua(), pos

    if max_player:
        maximo = float('-inf')
        movimiento_optimo = None
        for movimiento in get_movimientos(pos, BLANCO, juego):
            evaluacion = ab_prunning(movimiento, profundidad-1, False, juego)[0]
            maximo = max(maximo, evaluacion)
            if maximo == evaluacion:
                movimiento_optimo = movimiento

        return maximo, movimiento_optimo
    else:
        minimo = float('inf')
        movimiento_optimo = None
        for movimiento in get_movimientos(pos, CLARO, juego):
            evaluacion = ab_prunning(movimiento, profundidad-1, True, juego)[0]
            minimo = min(minimo, evaluacion)
            if minimo == evaluacion:
                movimiento_optimo = movimiento

        return minimo, movimiento_optimo

def simula_movimiento(ficha, movimiento, tablero, juego, skip):
    tablero.movimiento(ficha, movimiento[0], movimiento[1])
    if skip:
        tablero.elimina(skip)
    return tablero

#funcion para encontrar todos los movimientos de todas las fichas
def get_movimientos(tablero, color, juego):
    movimientos = []

    #for loop donde va cambiando de fichas hasta que checa todas 
    for ficha in tablero.get_todas_fichas(color):
        movimientos_validos = tablero.get_movimientos_validos(ficha)
        #for loop para cada movimiento o skip (comer ficha rival) dentro de los posibles
        for movimiento, skip in movimientos_validos.items():
            #crea un tablero temporal que es la copia del actual
            temp_tablero = deepcopy(tablero)
            temp_ficha = temp_tablero.get_ficha(ficha.fila, ficha.col)
            nuevo_tablero = simula_movimiento(temp_ficha, movimiento, temp_tablero, juego, skip)
            movimientos.append(nuevo_tablero)
    return movimientos