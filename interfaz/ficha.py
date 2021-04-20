from .constantes import DORADO, BLANCO, CUADRO, GRIS, CORONA
import pygame

class Ficha:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, fila, col, color):
        self.fila = fila
        self.col = col
        self.color = color
        self.rey = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = CUADRO * self.col + CUADRO // 2
        self.y = CUADRO * self.fila + CUADRO // 2

    def hacer_rey(self):
        self.rey = True
    
    def draw(self, ventana):
        radius = CUADRO//2 - self.PADDING
        pygame.draw.circle(ventana, GRIS, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(ventana, self.color, (self.x, self.y), radius)
        if self.rey:
            ventana.blit(CORONA, (self.x - CORONA.get_width()//2, self.y - CORONA.get_height()//2))

    def movimiento(self, fila, col):
        self.fila = fila
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)