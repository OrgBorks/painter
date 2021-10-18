# example painter project

from painter import Painter

p = Painter(10, 2, 1, "east", 100)

p.paint("blue")
p.move()
p.paint("#44a67a")
p.turnLeft()
p.turnLeft()
p.turnLeft()
p.move()
p.paint("red")
print(p.isOnPaint())
p.turnLeft()
p.turnLeft()
p.move()
p.scrapePaint()
p.turnLeft()
p.paint("green")
p.faceSouth()
while p.canMove():
    c = p.getColor()
    p.move()
    if c == "green":
        p.paint("orange")
    else:
        p.paint("green")
p.turnLeft()
p.move()
p.paint("#FF7777")
print(p.isOnPaint())
p.turnLeft()
p.turnLeft()
p.move()
print(p.isOnPaint())
