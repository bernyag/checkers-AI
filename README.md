# DAMAS - IA
## Integrantes
- Bernardo Altamirano (167881)
- Eduardo Pesqueira Zorrilla (176065)
- Ian Zaidenweber (176705)
- Antonino Garcia (180164)

## Objetivo
Damas es un juego de dos jugadores cuyo objetivo es comerse todas las fichas del rival o atrapar a estas, para que el rival se quede sin movimientos. Se juega en un tablero de 8x8 empezando cada jugador en renglones opuestos, y se llenan los 3 primeros renglones de cada jugador situando las fichas en un solo color. Hay un total de 3x4 (3 renglones, 4 fichas por renglon)= 12 fichas por jugador. Este programa, por medio del algoritmo alfa-beta pruning, crea un jugador de damas y con la interfaz presenta un tablero de juego para jugar contra un usuario, intentando vencerlo. El usuario podrá elegir entre 3 niveles de dificultad: "Fácil", "Intermedio" y "Dificil".

## Requerimientos
Para correr exitosamente el programa se requeiere `Python`, `Pygame` y `Tkinter`. Siendo los ultimos dos paquetes para crear la interfaz de juego.
El programa está compuesto de dos partes: el frontend (Pygame, Tkinter) y el backend (Python). 


## Manual de uso
1. Abrir el proyecto Damas-IA en Python
3. Correr el proyecto
4. Elegir un nivel de dificultad entre: "Fácil", "Intermedio" y "Dificil".
5. Iniciar la partida haciendo click en la ficha que desea mover, y posteriormente click en el cuadro (posición) a la que desea mover la ficha seleccionada.
6. Tras hacer su movimiento, la computadora calculará su mejor movimiento, analizando las opciones dependiendo del nivel de dificultad elegido, y movera su ficha.

## Validaciones
Hay algunas validaciones para evitar que se trate de resolver un estado que no esté bien definido:
- Se utiliza la operacion de mod, para mover las fichas correctamente de un cuadro a otro.
- Se crean deepcopy's de los tableros al analizar los posibles movimientos para evitar modificar el tablero de juego actual.


