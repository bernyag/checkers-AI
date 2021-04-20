import pygame

LARGO, ALTO = 800, 800
FILAS, COLS = 8, 8
CUADRO = LARGO//COLS
COLO = (200,0,0)
COLO2 = (0,0,200)
##ventana donde se mostrara el tablero
VENT2 = pygame.display.set_mode((600, 400))
##nombre del tablero
pygame.display.set_caption('Dificultad')
VENT2.fill(COLO)
pygame.display.flip()

pygame.draw.rect(VENT2, COLO2, (50, 50, 200, 200))

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False



