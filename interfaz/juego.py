import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board

class Game:
    def __init__(self, ventana):
        self._init()
        self.ventana = ventana
    
    def update(self):
        self.board.draw(self.ventana)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
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

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.ventana, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()