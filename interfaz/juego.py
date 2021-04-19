import pygame
from .constantes import ROJO, BLANCO, AZUL, CUADRO
from .tablero import Tablero

class Juego:
    def __init__(self, ventana):
        self._init()
        self.ventana = ventana
    
    def update(self):
        self.tablero.draw(self.ventana)
        self.draw_movimientos_validos(self.movimientos_validos)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.tablero = Tablero()
        self.turn = ROJO
        self.movimientos_validos = {}

    def ganador(self):
        return self.tablero.ganador()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._movimiento(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        ficha = self.tablero.get_ficha(row, col)
        if ficha != 0 and ficha.color == self.turn:
            self.selected = ficha
            self.movimientos_validos = self.tablero.get_movimientos_validos(ficha)
            return True
            
        return False

    def _movimiento(self, row, col):
        ficha = self.tablero.get_ficha(row, col)
        if self.selected and ficha == 0 and (row, col) in self.movimientos_validos:
            self.tablero.movimiento(self.selected, row, col)
            skipped = self.movimientos_validos[(row, col)]
            if skipped:
                self.tablero.elimina(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_movimientos_validos(self, movimientos):
        for movimiento in movimientos:
            row, col = movimiento
            pygame.draw.circle(self.ventana, BLUE, (col * CUADRO + CUADRO//2, row * CUADRO + CUADRO//2), 15)

    def change_turn(self):
        self.movimientos_validos = {}
        if self.turn == ROJO:
            self.turn = BLANCO
        else:
            self.turn = ROJO

    def get_tablero(self):
        return self.tablero

    def ai_movimiento(self, tablero):
        self.tablero = tablero
        self.change_turn()