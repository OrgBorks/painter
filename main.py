import logging
from painter import Painter

p = Painter(0, 0, "east", 20, 20, 0)
    
def main(dt):
    p.turnLeft()
    p.move()

p.run(main)