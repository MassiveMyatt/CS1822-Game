from user304_rsf8mD0BOQ_1 import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    
WIDTH = 600
HEIGHT = 400
frameNo = 0
GRAVITY = 0.5
IMG_CENTRE = Vector(256, 256)
IMG_DIMS = Vector(512, 512)
img_dest_dim = Vector(128,128)
img_pos = Vector(WIDTH/2, 300)
ground = Vector(WIDTH/2, 300)
IMG = simplegui.load_image('http://www.cs.rhul.ac.uk/courses/CS1830/sprites/coach_wheel-512.png')

                
class Wheel:
    def __init__(self, IMG, IMG_CENTRE, IMG_DIMS, img_pos, img_dest_dim):
        self.IMG = IMG
        self.IMG_CENTRE = IMG_CENTRE
        self.IMG_DIMS = IMG_DIMS
        self.img_pos = img_pos
        self.img_dest_dim = img_dest_dim
        self.vel = Vector()
        self.img_rot = 0
        

    def draw(self, canvas):
        self.img_rot = self.img_rot + kbd.get_step() 
        canvas.draw_image(IMG, IMG_CENTRE.get_p(), IMG_DIMS.get_p(), img_pos.get_p(), img_dest_dim.get_p(), self.img_rot)
        
    def on_ground(self):
        onGround = True
        if self.img_pos.y > 300 :
            onGround = True
        else:
            onGround = False
         
        return onGround 
        
    def update(self):
        self.img_pos.add(self.vel)
        self.vel.multiply(0.85)
        if self.img_pos.x > WIDTH:
            self.vel.multiply(-1.5)
            
        if self.img_pos.x < 0:
            self.vel.multiply(-1.5)
            
        if self.img_pos.y > HEIGHT:
            self.vel.multiply(-1.5)         
            
        if self.img_pos.y < 0:
            self.vel.multiply(-1.5)
        
        if self.on_ground() == False:
            self.vel.y += GRAVITY
            
            
class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.space = False
        self.step = 0

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
            self.step = -1
        if key == simplegui.KEY_MAP['left']:
            self.left = True
            self.step = 1
        if key == simplegui.KEY_MAP['up']:
            self.up = True
            self.step = 0
        if key == simplegui.KEY_MAP['down']:
            self.down = True
            self.step = 0
        if key == simplegui.KEY_MAP['space']:
            self.space = True
            self.step = 0
            
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
            self.step = 0
        if key == simplegui.KEY_MAP['left']:
            self.left = False
            self.step = 0
        if key == simplegui.KEY_MAP['up']:
            self.up = False
            self.step = 0
        if key == simplegui.KEY_MAP['down']:
            self.down = False
            self.step = 0
        if key == simplegui.KEY_MAP['space']:
            self.space = False
            self.step = 0
     
    def get_step(self):
        return self.step
            
class Interaction:
    def __init__(self, wheel, keyboard):
        self.wheel = wheel
        self.keyboard = keyboard

    def update(self):
        if self.keyboard.right:
            self.wheel.vel.add(Vector(1, 0))
            
        if self.keyboard.left:
            self.wheel.vel.add(Vector(-1, 0))
         
        if self.keyboard.up:
            self.wheel.vel.add(Vector(0,-1))
            
        if self.keyboard.down:
            self.wheel.vel.add(Vector(0,1))
        
        if self.keyboard.space:
            self.wheel.vel = Vector(0,-12)
        

kbd = Keyboard()
wheel = Wheel(IMG, IMG_CENTRE, IMG_DIMS, img_pos, img_dest_dim)
inter = Interaction(wheel, kbd)

def draw(canvas):
    inter.update()
    wheel.update()
    wheel.draw(canvas)


frame = simplegui.create_frame('Interactions', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)


frame.set_canvas_background('#2C6A6A')


frame.start()
