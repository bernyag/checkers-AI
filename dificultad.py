import pygame
pygame.init()
  
BLANCO = (0,0,0)
res = (720,720)
  
screen = pygame.display.set_mode(res)
  
color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
width = screen.get_width()
height = screen.get_height()
smallfont = pygame.font.SysFont('Arial',50)
textDif = smallfont.render('Dificil' , True , color)
textInter= smallfont.render('Intermedio' , True , color)
textFacil = smallfont.render('Facil' , True , color)
  
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
        #checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
            #if the mouse is clicked on the
            # button the game is terminated
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+140:
                pygame.quit()
                  
    # fills the screen with a color
    screen.fill(BLANCO)
      
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
      
    # if mouse is hovered on a button it
    # changes to lighter shade 
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
        pygame.draw.rect(screen,color_light,[width/2,height/2,140,40])
          
    else:
        pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40])
      
    # superimposing the text onto our button
    screen.blit(text , (width/2+50,height/2))
      
    # updates the frames of the game
    pygame.display.update()


