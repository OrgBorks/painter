import time, logging
import pyglet
from pyglet import shapes

class OutOfBoundsException(Exception):
    pass

class InvalidColorException(Exception):
    pass

class Exec:
    def __init__(self, func, painter, args_at_exec, *args, **kwargs):
        self.ran_funcs = False
        self.func = func
        self.painter = painter
        self.args_at_exec = args_at_exec
        self.args = list(args)
        self.args.insert(0, self.painter)
        self.kwargs = kwargs

    def run_args(self):
        for arg in self.args_at_exec:
            self.args.append(arg(self.painter))
        self.ran_funcs = True

class Painter:
    def __init__(self, x, y, direction, paint, w, s, debug=logging.WARNING):
        logging.basicConfig(format="%(levelname)s: %(message)s", level=debug)
        # constants
        self._EAST = 90
        self._SOUTH = 180
        self._WEST = 270
        self._NORTH = 0
        self.__pixel_width = 350 // w
        self.__width = self.__pixel_width * w
        self.__offset = 25
        self.__speed = s
        self.__tiles = w

        # colors
        self._RED = "#FF0000"
        self._ORANGE = "#FFA500"
        self._YELLOW = "#FFFF00"
        self._GREEN = "#00FF00"
        self._BLUE = "#0000FF"
        self._PURPLE = "#6A0DAD"
        self._BROWN = "#964B00"
        self._BLACK = "#000000"
        self._WHITE = "#FFFFFF"

        # initial variables
        self.clock = pyglet.clock.get_default()
        self.window = pyglet.window.Window(500, 500, resizable=True) # default window
        self.batch = pyglet.graphics.Batch()
        # self.square = shapes.BorderedRectangle(x=50, y=self.window.height-400, width=350, height=350, color=(0, 0, 0), border_color=(255, 255, 255), batch=self.batch)
        __p_img = pyglet.image.load("single_painter.png")
        __p_img.anchor_x, __p_img.anchor_y = __p_img.width//2, __p_img.height//2
        self.__p_spr = pyglet.sprite.Sprite(__p_img, x=self.__offset + self.__pixel_width//2 + (self.__pixel_width * x), y=self.window.height - self.__offset - self.__pixel_width//2 - (self.__pixel_width * y))
        self.__p_spr.scale = self.__pixel_width/self.__p_spr.width
        self.__p_spr.rotation = getattr(self, "_" + direction.upper())
        self.__x = x
        self.__y = y
        self.__paint = paint
        self.__drawables = []
        self.__painted = [ [ None for _ in range(w) ] for _ in range(w) ]
        self.__queue = []
        self.__ran = False

        # grid outline (transparent inside, can't do that with square)
        line1 = shapes.Line(x=self.__offset, y=self.window.height-self.__offset, x2=self.__width+self.__offset, y2=self.window.height-self.__offset, color=(255, 255, 255))
        line2 = shapes.Line(x=self.__offset, y=self.window.height-self.__offset, x2=self.__offset, y2=self.window.height-self.__width-self.__offset)
        line3 = shapes.Line(x=self.__offset, y=self.window.height-self.__width-self.__offset, x2=self.__width+self.__offset, y2=self.window.height-self.__width-self.__offset)
        line4 = shapes.Line(x=self.__width+self.__offset, y=self.window.height-self.__width-self.__offset, x2=self.__width+self.__offset, y2=self.window.height-self.__offset)
        self.__drawables.append(line1)
        self.__drawables.append(line2)
        self.__drawables.append(line3)
        self.__drawables.append(line4)

        # default utils
        self.__get_rot = lambda x: getattr(self, "_" + x.upper())
        self.__label_center_anchor = {"anchor_x": "center", "anchor_y": "center"}
        self.__label_center_screen = lambda x, y: {"x": x.width//2, "y": y.height//2}
        self.__label_center = lambda x, y: {**self.__label_center_screen(x, y), **self.__label_center_anchor}
        
        self.window.push_handlers(on_draw=self.__on_draw)

        self.__drawables.append(self.__p_spr)
    
    def __color(self, hex):
        if hex[0] != "#":
            raise InvalidColorException(f"Color {hex} is not a valid color. Valid colors are: red, orange, yellow, green, blue, purple, brown, black, white.")
        return (int(hex[1:3], 16), int(hex[3:5], 16), int(hex[5:7], 16))

    def __rotate_to(self, p, i):
        i -= 90
        if i < 0:
            i += 360
        if p.rotation != i:
            p.rotation -= 1
            time.sleep(0.00005*self.__tiles*self.__speed)
        else:
            logging.info("finished rotating")
            self.__ran = True
    
    def __slide_to(self, p, mod, times, starting):
        # setting the initial variables and orientations
        i = 1
        if p.rotation == self._WEST or p.rotation == self._EAST:
            pos = p.x
            original = starting[0]
            moving = "x"
        elif p.rotation == self._NORTH or p.rotation == self._SOUTH:
            pos = p.y
            original = starting[1]
            moving = "y"
        if p.rotation == self._WEST or p.rotation == self._SOUTH:
            i = -1
            mod = -mod
        # bounds checking
        if p.rotation == self._WEST or p.rotation == self._EAST:
            if not self.__can_move(p, pos):
                raise OutOfBoundsException("Painter tried to move out of bounds.")
        elif p.rotation == self._NORTH or p.rotation == self._SOUTH:
            if not self.__can_move(p, pos):
                raise OutOfBoundsException("Painter tried to move out of bounds")
        # moving the painter
        if pos != (original + mod):
            if p.rotation == self._WEST or p.rotation == self._EAST:
                p.x += i
            elif p.rotation == self._NORTH or p.rotation == self._SOUTH:
                p.y += i
            time.sleep(0.0002*self.__tiles*self.__speed)
        else:
            if moving == "x":
                self.__x += i * times
            elif moving == "y":
                self.__y += -i * times
            logging.info(f"Finished sliding. {self.__x}, {self.__y}. {p.x}, {p.y}.")
            self.__ran = True
    
    def __can_move(self, p, dir=None, r=False):
        bCheck = self.__pixel_width//2
        if p.rotation == self._WEST or p.rotation == self._SOUTH:
            bCheck = -bCheck
        if dir is None:
            dir = p.rotation
        if dir == self._WEST or dir == self._EAST:
            if p.x + bCheck < self.__offset or p.x + bCheck > self.__offset + self.__width:
                if r:
                    self.__ran = True
                logging.info("Finished evaluating movement.")
                return False
        if dir == self._NORTH or dir == self._SOUTH:
            if p.y + bCheck > self.window.height - self.__offset or p.y + bCheck < self.window.height - self.__offset - self.__width:
                if r:
                    self.__ran = True
                logging.info("Finished evaluating movement.")
                return False
        if r:
            self.__ran = True
        logging.info("Finished evaluating movement.")
        return True
    
    def __paint_tile(self, p, c):
        self.__painted[self.__y][self.__x] = shapes.BorderedRectangle(
        x=p.x-(self.__pixel_width//2),
        y=p.y-(self.__pixel_width//2),
        width=self.__pixel_width,
        height=self.__pixel_width,
        color=self.__color(c),
        border=0)
        logging.info("Finished painting.")
        self.__ran = True
    
    def __scrape_tile(self, p):
        self.__painted[self.__y][self.__x] = None
        logging.info("Finished scraping.")
        self.__ran = True

    def __on_draw(self):
        self.window.clear()
        self.batch.draw()
        for i in self.__painted:
            for j in i:
                if j is not None:
                    j.draw()
        for i in self.__drawables:
            i.draw()
    
    # custom queue system
    def __runQueue(self, func):
        while not self.__ran:
            while self.__p_spr.rotation < 0:
                self.__p_spr.rotation += 360
            if self.__ran:
                logging.info("finished running")
            if not func.ran_funcs:
                func.run_args()
            logging.info(f"running {func.func.__name__}")
            r = func.func(*func.args, **func.kwargs)
            # dt = pyglet.clock.tick()
            self.__draw_screen(0)
            if r is not None:
                return r
    
    def __draw_screen(self, dt):
        self.window.dispatch_event("on_draw")
        self.window.flip()

    # START OF USER-ACCESSIBLE FUNCTIONS

    def turnLeft(self):
        self.__ran = False
        self.__runQueue(Exec(self.__rotate_to, self.__p_spr, [lambda x: x.rotation]))
    
    def move(self, m=1):
        self.__ran = False
        self.__runQueue(Exec(self.__slide_to, self.__p_spr, [lambda x: (x.x, x.y)], self.__pixel_width * m, m))
    
    def canMove(self, dir=None):
        self.__ran = False
        return self.__runQueue(Exec(self.__can_move, self.__p_spr, [], dir=dir, r=True))
    
    def paint(self, color="white"):
        self.__ran = False
        color = getattr(self, "_" + color.upper(), color)
        self.__runQueue(Exec(self.__paint_tile, self.__p_spr, [], color))
    
    def scrapePaint(self):
        self.__ran = False
        self.__runQueue(Exec(self.__scrape_tile, self.__p_spr, []))
    
    def facingNorth(self):
        return self.__p_spr.rotation == self._NORTH
    
    def facingSouth(self):
        return self.__p_spr.rotation == self._SOUTH
    
    def facingWest(self):
        return self.__p_spr.rotation == self._WEST
    
    def facingEast(self):
        return self.__p_spr.rotation == self._EAST

    def isOnPaint(self):
        return self.__painted[self.__y][self.__x] != None
    
    def run(self, func):
        self.__queue.reverse()
        pyglet.clock.schedule_once(self.__draw_screen, 0)
        pyglet.clock.schedule_once(func, 0)
        pyglet.clock.schedule(self.__draw_screen)
        pyglet.app.run()