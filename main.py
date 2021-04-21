import pygame
from interfaz.constantes import LARGO, ALTO, CUADRO, DORADO, BLANCO
from interfaz.interfaz import Juego
from heuristica.heuristicas import ab_pruning
import time

##cte de velocidad que se utilizara para que mueva la computadora
velocidad = 60

##ventana donde se mostrara el tablero
VENTANA = pygame.display.set_mode((LARGO, ALTO))
##nombre del tablero
pygame.display.set_caption('MaraDamas')

def posicion_mouse(pos):
    x, y = pos
    fila = y // CUADRO
    col = x // CUADRO
    return fila, col

def main():
    ejec = True
    clock = pygame.time.Clock()
    juego = Juego(VENTANA)

    while ejec:
        clock.tick(velocidad)
        
        if juego.turn == BLANCO:
            inicio = time.time()
            value, new_board = ab_pruning(juego.get_tablero(), 10, BLANCO, juego, -10000000, 1000000)
            juego.ai_movimiento(new_board)
            fin = time.time()
            print('Tiempo en evaluar: {}s'.format(round(fin - inicio, 7)))

        if juego.ganador() != None:
            if str(juego.turn) == (246, 181, 6):
                print('El ganador es: BLANCO')
            else:
                print('El ganador es: DORADO')
            ejec = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejec = False
            ##hace movimientos acorde al click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                fila, col = posicion_mouse(pos)
                juego.select(fila, col)
        juego.update()
    pygame.quit()
main()