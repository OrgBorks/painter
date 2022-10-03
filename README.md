# Code.org MyNeighborhood Painter

This is an unofficial port of code.org's MyNeighborhood Painter used in the AP Computer Science A course, coded in Python. I am in no way associated with code.org. Just uses python's Turtle module.

# Usage

First, make a new painter with the `Painter()` constructor.

`Painter(w, x, y, d, p, s=2)`

w: int - The width and height of the board. It can only be a square.

x: int - The initial x coordinate of the painter.

y: int - The initial y coordinate of the painter.

d: string - The initial direction of the painter. Options: "north", "east", "south", "west".

p: int - The initial amount of paint of the painter.

s: [Optional] int - The initial speed of the painter. Must be a number between 1 - 10. 0 skips animations completely.

The available commands for the painter are:

`move(l=1)`

l: [Optional] int - The number of spaces to move forward. Defaults to 1.

`setSpeed(s)`

s: int - The speed you want the painter to go, from 1 - 10.

Note: The speed is very sensitive for some reason (I don't reall know if it actually works anymore), so if you want to be able to see what you're doing, I recommend keeping it the default. Also, the more pixels there are, the faster it's gonna go. I think.
