import turtle

# exceptions
class OutOfBoundsException(Exception):
    pass

class OutOfPaintError(Exception):
    pass

class NotPaintedError(Exception):
    pass

class InvalidDirectionError(Exception):
    pass

# main painter class
class Painter:
    def __init__(self, w, x, y, d, p):
        self.__screen = turtle.getscreen()
        self.__canvas = self.__screen.getcanvas()
        # self.__screen.screensize(self.__canvas.winfo_screenwidth(), self.__canvas.winfo_screenheight())
        self.__t = self.__screen.turtles()[0]
        t = self.__t
        self.__border = turtle.Turtle()
        self.__border.ht()
        self.__w = w
        self.x = x + 1
        self.y = y + 1
        t.color("red")
        self.__speed = 6
        self.paintLeft = p
        self.__pixelWidth = 200/w
        t.shapesize(self.__pixelWidth/10, self.__pixelWidth/10)
        if x >= w or y >= w:
            raise OutOfBoundsException(f"Starting coordanates ({x}, {y}) are out of bounds.")
        self.__start()
        self.__paintedSquares = []
        for i in range(w):
            self.__paintedSquares.append([])
            for j in range(w):
                self.__paintedSquares[i].append(None)
        t.seth(self.__toDegree(d.lower()))
    
    def __toDegree(self, d):
        if d == "east":
            return 0
        elif d == "west":
            return 180
        elif d == "north":
            return 90
        elif d == "south":
            return 270
        else:
            raise InvalidDirectionError(f"Direction \"{d}\" is not a valid direction.")
    
    def __toCoords(self, x, y):
        return -100 + (self.__pixelWidth * x), 100 - (self.__pixelWidth * y)
    
    def setSpeed(self, s):
        """Set the speed of the painter.

        Args:
            s - Number from 1-10. 1 is the slowest speed, 10 is the fastest speed."""
        self.__t.speed(s)
        self.__speed = s
    
    def canMove(self, d=None):
        if not d:
            d = self.__t.heading()
        else:
            d = self.__toDegree(d.lower())
        o = self.__t.heading()
        try:
            self.__t.seth(d)
            self.move()
        except:
            self.__t.seth(o)
            return False
        self.__t.bk(self.__pixelWidth)
        if self.facingEast():
            self.x -= 1
        elif self.facingWest():
            self.x += 1
        elif self.facingNorth():
            self.y += 1
        elif self.facingSouth():
            self.y -= 1
        self.__t.seth(o)
        return True
    
    def isOnPaint(self):
        """Checks if the square the painter is currently standing on is painted or not. Returns True or False."""
        return self.__paintedSquares[self.y][self.x] != None
    
    def getColor(self):
        """Returns the color of the square the painter is currently standing of. If the square is empty, None is returned."""
        return self.__paintedSquares[self.y][self.x]
    
    def scrapePaint(self):
        """Scrapes the paint off the square the painter is currently standing on, if it's painted. No inputs or returns."""
        if self.isOnPaint():
            self.paint("white")
        else:
            raise NotPaintedError("This tile is not painted.")
    
    def hide(self):
        """Hides the painter. No inputs or returns."""
        self.__t.ht()
    
    def show(self):
        """Shows the painter. No inputs or returns."""
        self.__t.st()
    
    def facingNorth(self):
        """Check if the painter is facing north. Returns True or False."""
        return self.__t.heading() == 90

    def faceNorth(self):
        """Makes the painter face north. No inputs or returns."""
        self.__t.seth(90)
    
    def facingSouth(self):
        """Check if the painter is facing south. Returns True or False."""
        return self.__t.heading() == 270
    
    def faceSouth(self):
        """Makes the painter face south. No inputs or returns."""
        self.__t.seth(270)
    
    def facingWest(self):
        """Check if the painter is facing west. Returns True or False."""
        return self.__t.heading() == 180
    
    def faceWest(self):
        """Makes the painter face west. No inputs or returns."""
        self.__t.seth(180)
    
    def facingEast(self):
        """Check if the painter is facing west. Returns True or False."""
        return self.__t.heading() == 0
    
    def faceEast(self):
        """Makes the painter face east. No inputs or returns."""
        self.__t.seth(0)
    
    def turnLeft(self):
        """Makes the painter turn left. No inputs or returns."""
        self.__t.speed(self.__speed)
        self.__t.seth(self.__t.heading() + 90)
    
    def __start(self):
        t = self.__border
        t.speed(0)
        t.penup()
        self.__t.penup()
        t.goto(-100, 100)
        self.__square("black", 200, t=t)
        self.__t.goto(-100+(self.__pixelWidth*self.x)+(self.__pixelWidth/2), 100-(self.__pixelWidth*self.y)-(self.__pixelWidth/2))
        self.__t.speed(self.__speed)
    
    def __square(self, c, w, fill=False, t=None):
        if not t:
            t = self.__t
        t.pencolor(c)
        t.pendown()
        if fill:
            t.fillcolor(c)
            t.begin_fill()
        t.forward(w)
        t.rt(90)
        t.forward(w)
        t.rt(90)
        t.forward(w)
        t.rt(90)
        t.forward(w)
        t.rt(90)
        if fill:
            t.end_fill()
        t.penup()
        t.pen(pencolor="red", fillcolor="black")
    
    def paint(self, c):
        """Paints the square that the painter is currently on.
        
        Args:
            c - A string representing a color or hex value."""
        if self.paintLeft == 0:
            raise OutOfPaintError("The painter ran out of paint.")
        t = self.__t
        h = t.heading()
        p = t.pos()
        t.speed(0)
        t.goto(t.xcor()-(self.__pixelWidth/2), t.ycor()+(self.__pixelWidth/2))
        t.seth(0)
        try:
            self.__square(c, self.__pixelWidth, True)
        except Exception as e:
            if "bad color" in e.__str__():
                raise ValueError(f"Color \"{c}\" is not a valid color.")
        self.__paintedSquares[self.y][self.x] = c
        if (self.x == 0 or self.x == self.__w-1) or (self.y == 0 or self.y == self.__w-1):
            self.__square("black", 200, t=self.__border)
        t.goto(p)
        t.seth(h)
        t.speed(self.__speed)
        self.paintLeft -= 1

    def move(self, l=1):
        """Moves the painter.
        
        Args:
            l = An integer representing the number of squares to move by."""
        t = self.__t

        t.speed(self.__speed)
        t.fd(self.__pixelWidth*l)
        pos = t.pos()
        if not (-100 < pos[0] < 100 and -100 < pos[1] < 100):
            t.bk(self.__pixelWidth*l)
            raise OutOfBoundsException("Painter tried to move out of bounds.")
        if self.facingEast():
            self.x += l
        elif self.facingWest():
            self.x -= l
        elif self.facingNorth():
            self.y -= l
        elif self.facingSouth():
            self.y += l