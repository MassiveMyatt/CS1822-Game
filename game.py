from user304_rsf8mD0BOQ_1 import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math
import time
import random

WIDTH = 1000
HEIGHT = 400
STEP = 0.5
GRAVITY = 0.7
GROUND_Y = HEIGHT + 20

class Wheel:
    def __init__(self, pos, radius=10):
        self.pos = pos
        self.vel = Vector()
        self.radius = max(radius, 10)
        self.colour = 'White'
        self.img = simplegui.load_image('https://freesvg.org/img/8-Bit-Character-1.png')
        self.img_centre = (256, 256)
        self.img_dims = (512,512)
        self.img_dest_dim = (128, 128)
        self.img_pos = (WIDTH / 2, 2*HEIGHT / 3.)
        self.img_rot = 0
        self.clockwise = None
        self.health = 100
        self.wrapped = False 
        self.distance = 0
        self.dead = False
        

    def draw(self, canvas):
        canvas.draw_image(self.img, self.img_centre, self.img_dims, self.pos.get_p(), (self.radius, self.radius), self.img_rot)
        canvas.draw_text(('Distance:' + str(self.distance)), (20, 50), 50, 'Blue')


    def update(self):
        self.rotate()
        self.pos.add(self.vel)
        self.vel.multiply(0.85)
        self.wrap()
        if self.ground_check() == False:
            self.vel.y += GRAVITY
        else:
            self.vel.y = 0
        if self.vel.x > 1:
            self.distance += 1
          
           
            

    def rotate(self):
        if self.clockwise is not None:
            if self.clockwise == True:
                self.img_rot -= STEP
            else:
                self.img_rot += STEP
        else:
            self.img_rot = 0


    def wrap(self):
        position = self.pos.get_p()
        if position[0] + self.radius > WIDTH: #wrap r -> l
            self.pos = Vector(0 + self.radius, position[1])
            self.wrapped = True
        elif position[0] + self.radius < 0:
            self.vel.multiply(-5)
        else:
            self.wrapped = False

    def ground_check(self):
        position = self.pos.get_p()
        if position[1] + self.radius >= GROUND_Y:
            return True
        else:
            return False
        
    def take_damage(self):
        self.health = self.health - 100
        if self.health <= 0:
            self.dead = True
            
    
    
    def reset_wheel(self):
        self.dead = False
        self.health = 100
        self.distance = 0
        self.pos = Vector(WIDTH - 20, HEIGHT - 20)
            
        
    def bounce(self, normal):
        self.vel.reflect(normal)

class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.space = False
        self.p = False
        self.q = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        elif key == simplegui.KEY_MAP['left']:
            self.left = True
        elif key == simplegui.KEY_MAP['space']:
            self.space = True
        elif key == simplegui.KEY_MAP['p']:
            self.p = True
        elif key == simplegui.KEY_MAP['q']:
            self.q = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        elif key == simplegui.KEY_MAP['left']:
            self.left = False
        elif key == simplegui.KEY_MAP['space']:
            self.space = False
        elif key == simplegui.KEY_MAP['p']:
            self.p = False
        elif key == simplegui.KEY_MAP['q']:
            self.q = False



          
                     
class Menu:
    def __init__(self):
        self.active = True
        self.scores = []
    
    def draw(self, canvas):
        canvas.draw_text('Insert Cool Game Name Here', (50, 50), 50, 'Red')
        canvas.draw_text('Press P To Play', (100, HEIGHT / 2), 30, 'Red')
        canvas.draw_text('Press Q to exit',(100, HEIGHT - 30), 30, 'Red')
        if len(self.scores) > 0:
            self.scores.sort()
            canvas.draw_text('High Score: ' + str(self.scores[len(self.scores) - 1]), (100, HEIGHT / 3), 30, 'Yellow')
            canvas.draw_text('YOU DIED!', (WIDTH / 2, HEIGHT / 2), 50, 'Red')

    def set_inactive(self):
        self.active = False
        
    def set_active(self):
        self.active = True
    

class circle:
    def __init__(self, pos, radius, border, color):
        self.pos = pos
        self.radius = radius
        self.border = border
        self.color = color
        self.edge = self.radius + self.border
        
    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 2*self.border+1, self.color, self.color)
        
    def hit(self, ball):
        distance = self.pos.copy().subtract(ball.pos).length()
        distance = distance + self.edge
        return distance - ball.radius <= self.edge
    
    def normal(self, ball):
        perpendicular = self.pos.copy().subtract(ball.pos)
        return perpendicular.normalize()
    
class Interaction:

    def __init__(self, wheel, keyboard, menu):
        self.wheel = wheel
        self.keyboard = keyboard
        self.menu = menu
        self.collision = False
        self.circles = []
        self.projectiles = []
       

    def update(self):
        if menu.active == False:
            if self.keyboard.right:
                self.wheel.vel.add(Vector(1, 0))
                self.wheel.clockwise = True
            elif self.keyboard.left:
                self.wheel.vel.add(Vector(-1,0))
                self.wheel.clockwise = False
            elif self.keyboard.space:
                if self.wheel.ground_check() == True:
                    self.keyboard.space = False
                    self.wheel.vel.add(Vector(0,-30))

                self.wheel.clockwise = None
                
            else:
                self.wheel.clockwise = None
            for circle in self.circles:
                  if circle.hit(wheel) == True:
                        if not self.collision:
                            wheel.take_damage()
                            normal = circle.normal(wheel)
                            self.wheel.bounce(normal) 
                            self.collision = True
                        else:
                            self.collision = False
            if wheel.wrapped == True:
               self.circles = []
               self.generate()
               self.projectiles = []       
            if wheel.dead == True:
               menu.scores.append(wheel.distance)
               self.circles = []
               menu.set_active()    
        elif menu.active == True:
           if self.keyboard.p:
               wheel.reset_wheel()
               self.generate()
               menu.set_inactive()
           elif self.keyboard.q:
               quit()
           
                      
    def generate(self):
        xprev = 60
        amount = random.randint(5,10)
        for i in range(0, amount):
           x = xprev + random.randint(70,200)
           radius = 5 
           y = HEIGHT - radius
           i = circle(Vector(x,y),radius,7,"red")
           self.circles.append(i)
           xprev = x
            
    def spawn_proj(self):
        amount = random.randint(1,5)
        for i in range (0, amount):
            y = random.randint(50, HEIGHT)
            radius = 5
            x = WIDTH + 5
            i = circle(Vector(x,y),radius,7,"blue")
            self.projectiles.append(i)    
    
        
    
         

kbd = Keyboard()
wheel = Wheel(Vector(WIDTH - 20, HEIGHT-20), 40)
menu = Menu()
inter = Interaction(wheel, kbd, menu)

def draw(canvas):
    if menu.active == False:
        inter.update()
        wheel.update()
        wheel.draw(canvas)
        circles = inter.circles
        for circle in circles:
            circle.draw(canvas)
    else:
        inter.update()
        menu.draw(canvas)
    
frame = simplegui.create_frame('Interactions', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_canvas_background('#31CAF3')
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
