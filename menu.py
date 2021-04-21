from tkinter import *
import tkinter.font as font
import mains

def facil():
    mains.main1()

def intermedio():
    mains.main2()

def dificil():
    mains.main3()

root = Tk()
root.title("Seleccione un nivel de dificultad")
frame = Frame(root)
frame.pack()
root.geometry('750x250')
myfont= font.Font(size=30)


bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

botonfacil = Button(frame, text="Fácil", command=facil, height=5, width=10, bg="green", fg="black")
botonfacil["font"]=myfont
botonfacil.pack( side = LEFT)

botonintermedio = Button(frame, text="Intermedio", command=intermedio, height=5, width=10, bg="yellow", fg="black")
botonintermedio["font"]=myfont
botonintermedio.pack( side = LEFT )

botondificil = Button(frame, text="Difícil",command=dificil, height=5, width=10, bg="red", fg="black")
botondificil["font"]=myfont
botondificil.pack( side = LEFT )


root.mainloop()



    