import pygame
from interfaz.constantes import LARGO, ALTO, CUADRO, DORADO, BLANCO
from interfaz.juego import Juego
from heuristica.minimax import minimax

FPS = 60

VENTANA = pygame.display.set_mode((LARGO, ALTO))
pygame.display.set_caption('MaraDamas')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // CUADRO
    col = x // CUADRO
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    juego = Juego(VENTANA)

    while run:
        clock.tick(FPS)
        
        if juego.turn == BLANCO:
            value, new_board = minimax(juego.get_tablero(), 1, BLANCO, juego)
            juego.ai_movimiento(new_board)


        if juego.ganador() != None:
            print(juego.ganador())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                juego.select(row, col)
        juego.update()
    pygame.quit()
main()