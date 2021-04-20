import pygame

from .constantes import CLARO, DORADO, BLANCO, FILAS, CUADRO, COLS
from .ficha import Ficha

class Tablero:
    #funcion que crea un tablero
        ##12 fichas por color y 0 reyes
    def __init__(self):
        self.tablero = []
        self.num_dorados = self.num_blancos = 12
        self.reyes_dorados = self.reyes_blancos = 0
        self.Tablero()
    
    #funcion que dibuja el tablero
        ##primero llena todo de azul claro
        ##para renglones pares + 0: 0 mod 2 = 0, llena cuadro 0 de blanco y va de 2 en 2 
        ##para renglones impares: 1 mod 2 = 1, llena cuadro 1 de blanco y va de 2 en 2
    def draw_squares(self, ventana):
        ventana.fill(CLARO)
        for fila in range(FILAS):
            for col in range(fila % 2, COLS, 2):
                #utiliza tamanos como coordenadas para colorear cuadros
                pygame.draw.rect(ventana, BLANCO, (fila*CUADRO, col*CUADRO, CUADRO, CUADRO))

    #funcion 
    def evalua(self):
        return self.num_blancos - self.num_dorados + (self.reyes_blancos * 0.5 - self.reyes_dorados * 0.5)

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
            ficha.hacer_rey()
            if ficha.color == BLANCO:
                self.reyes_blancos += 1
            else:
                self.reyes_dorados += 1 

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
                        self.tablero[fila].append(Ficha(fila, col, DORADO))
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
                if ficha.color == DORADO:
                    self.num_dorados -= 1
                else:
                    self.num_blancos -= 1
    
    def ganador(self):
        if self.num_dorados <= 0:
            return BLANCO
        elif self.num_blancos <= 0:
            return DORADO
        
        return None 
    
    def get_movimientos_validos(self, ficha):
        movimientos = {}
        izq = ficha.col - 1
        derecha = ficha.col + 1
        fila = ficha.fila

        if ficha.color == DORADO or ficha.rey:
            movimientos.update(self._mueve_izquierda(fila -1, max(fila-3, -1), -1, ficha.color, izq))
            movimientos.update(self._mueve_derecha(fila -1, max(fila-3, -1), -1, ficha.color, derecha))
        if ficha.color == BLANCO or ficha.rey:
            movimientos.update(self._mueve_izquierda(fila +1, min(fila+3, FILAS), 1, ficha.color, izq))
            movimientos.update(self._mueve_derecha(fila +1, min(fila+3, FILAS), 1, ficha.color, derecha))
    
        return movimientos

    def _mueve_izquierda(self, start, stop, step, color, izq, skipped=[]):
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
                    movimientos.update(self._mueve_izquierda(r+step, fila, step, color, izq-1,skipped=last))
                    movimientos.update(self._mueve_derecha(r+step, fila, step, color, izq+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            izq -= 1
        
        return movimientos

    def _mueve_derecha(self, start, stop, step, color, derecha, skipped=[]):
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
                    movimientos.update(self._mueve_izquierda(r+step, fila, step, color, derecha-1,skipped=last))
                    movimientos.update(self._mueve_derecha(r+step, fila, step, color, derecha+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            derecha += 1
        
        return movimientos