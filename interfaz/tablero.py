import pygame

from .constantes import NEGRO, ROJO, BLANCO, FILAS, CUADRO, COLS
from .ficha import Ficha

class Tablero:
    def __init__(self):
        self.tablero = []
        self.num_rojos = self.num_blancos = 12
        self.reyes_rojos = self.reyes_blancos = 0
        self.Tablero()
    
    def draw_squares(self, ventana):
        ventana.fill(NEGRO)
        for fila in range(FILAS):
            for col in range(fila % 2, COLS, 2):
                pygame.draw.rect(ventana, BLANCO, (fila*CUADRO, col *CUADRO, CUADRO, CUADRO))

    def evalua(self):
        return self.num_blancos - self.num_rojos + (self.reyes_blancos * 0.5 - self.reyes_rojos * 0.5)

    def get_todas_fichas(self, color):
        fichas = []
        for fila in self.tablero:
            for ficha in fila:
                if ficha != 0 and ficha.color == color:
                    fichas.append(ficha)
        return fichas

    def movimiento(self, ficha, fila, col):
        self.tablero[ficha.fila][ficha.col], self.tablero[fila][col] = self.tablero[fila][col], self.tablero[ficha.fila][ficha.col]
        ficha.movimiento(fila, col)

        if fila == FILAS - 1 or fila == 0:
            ficha.make_king()
            if ficha.color == BLANCO:
                self.reyes_blancos += 1
            else:
                self.reyes_rojos += 1 

    def get_ficha(self, fila, col):
        return self.tablero[fila][col]

    def Tablero(self):
        for fila in range(FILAS):
            self.tablero.append([])
            for col in range(COLS):
                if col % 2 == ((fila +  1) % 2):
                    if fila < 3:
                        self.tablero[fila].append(Ficha(fila, col, BLANCO))
                    elif fila > 4:
                        self.tablero[fila].append(Ficha(fila, col, ROJO))
                    else:
                        self.tablero[fila].append(0)
                else:
                    self.tablero[fila].append(0)
        
    def draw(self, ventana):
        self.draw_squares(ventana)
        for fila in range(FILAS):
            for col in range(COLS):
                ficha = self.tablero[fila][col]
                if ficha != 0:
                    ficha.draw(ventana)

    def elimina(self, fichas):
        for ficha in fichas:
            self.tablero[ficha.fila][ficha.col] = 0
            if ficha != 0:
                if ficha.color == ROJO:
                    self.num_rojos -= 1
                else:
                    self.num_blancos -= 1
    
    def ganador(self):
        if self.num_rojos <= 0:
            return BLANCO
        elif self.num_blancos <= 0:
            return ROJO
        
        return None 
    
    def get_movimientos_validos(self, ficha):
        movimientos = {}
        izq = ficha.col - 1
        derecha = ficha.col + 1
        fila = ficha.fila

        if ficha.color == ROJO or ficha.rey:
            movimientos.update(self._traverse_left(fila -1, max(fila-3, -1), -1, ficha.color, izq))
            movimientos.update(self._traverse_right(fila -1, max(fila-3, -1), -1, ficha.color, derecha))
        if ficha.color == BLANCO or ficha.rey:
            movimientos.update(self._traverse_left(fila +1, min(fila+3, FILAS), 1, ficha.color, izq))
            movimientos.update(self._traverse_right(fila +1, min(fila+3, FILAS), 1, ficha.color, derecha))
    
        return movimientos

    def _traverse_left(self, start, stop, step, color, izq, skipped=[]):
        movimientos = {}
        last = []
        for r in range(start, stop, step):
            if izq < 0:
                break
            
            current = self.tablero[r][izq]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    movimientos[(r, izq)] = last + skipped
                else:
                    movimientos[(r, izq)] = last
                
                if last:
                    if step == -1:
                        fila = max(r-3, 0)
                    else:
                        fila = min(r+3, FILAS)
                    movimientos.update(self._traverse_left(r+step, fila, step, color, izq-1,skipped=last))
                    movimientos.update(self._traverse_right(r+step, fila, step, color, izq+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            izq -= 1
        
        return movimientos

    def _traverse_right(self, start, stop, step, color, derecha, skipped=[]):
        movimientos = {}
        last = []
        for r in range(start, stop, step):
            if derecha >= COLS:
                break
            
            current = self.tablero[r][derecha]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    movimientos[(r,derecha)] = last + skipped
                else:
                    movimientos[(r, derecha)] = last
                
                if last:
                    if step == -1:
                        fila = max(r-3, 0)
                    else:
                        fila = min(r+3, FILAS)
                    movimientos.update(self._traverse_left(r+step, fila, step, color, derecha-1,skipped=last))
                    movimientos.update(self._traverse_right(r+step, fila, step, color, derecha+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            derecha += 1
        
        return movimientos