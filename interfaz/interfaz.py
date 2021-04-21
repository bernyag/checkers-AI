import pygame
from .constantes import LARGO, ALTO, FILAS, COLS, CUADRO, DORADO, BLANCO, CLARO, AZUL, GRIS, CORONA

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
        return self.num_blancos - self.num_dorados + (self.reyes_blancos * 3 - self.reyes_dorados * 3)

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


class Juego:
    def __init__(self, ventana):
        self._init()
        self.ventana = ventana
    
    def update(self):
        self.tablero.draw(self.ventana)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.tablero = Tablero()
        self.turn = DORADO
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

    def change_turn(self):
        self.movimientos_validos = {}
        if self.turn == DORADO:
            self.turn = BLANCO
        else:
            self.turn = DORADO

    def get_tablero(self):
        return self.tablero

    def ai_movimiento(self, tablero):
        self.tablero = tablero
        self.change_turn()