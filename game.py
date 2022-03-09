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
SHEET_WIDTH = 1440
SHEET_HEIGHT = 1480
COLUMNS = 6
ROWS = 5
SHEET_URL = "https://www.cs.rhul.ac.uk/courses/CS1830/sprites/runnerSheet.png"
time = 1

class Wheel:
    def __init__(self, SHEET_URL, WIDTH, HEIGHT, COLUMNS, ROWS, radius=50):
        
        self.SHEET_URL = simplegui.load_image(SHEET_URL)
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.COLUMNS = COLUMNS
        self.ROWS = ROWS

        self.frame_width = self.WIDTH/COLUMNS
        self.frame_height = self.HEIGHT/ROWS
        self.frame_centre_x = self.frame_width/2
        self.frame_centre_y = self.frame_height/2
        
        self.frame_index = [4, 1]
        
        self.radius = max(radius, 10)
        
        self.vel = Vector()

        self.width_height = Vector(self.frame_width, self.frame_height)        
        self.pos = Vector(0,0)
        
        
        self.radius = max(radius, 10)
        self.clockwise = None
        self.health = 100
        self.wrapped = False 
        self.distance = 0
        self.dead = False
        
    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.COLUMNS
        if self.frame_index[0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.ROWS

    def last_frame(self):
        self.frame_index[0] = (self.frame_index[0] - 1) % self.COLUMNS
        if self.frame_index[0] == 0:
            self.frame_index[1] = (self.frame_index[1] - 1) % self.ROWS



    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.85)
        self.wrap()
        if self.pos.x > WIDTH:
            self.vel.multiply(-1.5)
            
        if self.pos.x < 0:
            self.vel.multiply(-1.5)
            
        if self.pos.y > HEIGHT:
            self.vel.multiply(-1.5)         
            
        if self.pos.y < 0:
            self.vel.multiply(-1.5)
            
        if self.ground_check() == False:
            self.vel.y += GRAVITY
        else:
            self.vel.y = 0
        if self.vel.x > 1:
            self.distance += 1
          
           
           


    def wrap(self):
        position = self.pos.get_p()
        if position[0] + self.radius > WIDTH: #wrap r -> l
            self.pos = Vector(0 + self.radius, position[1])
            self.wrapped = True
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
        self.pos = Vector(0,350)
            
        
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
    
class clock:
    def __init__(self, time):
        self.time = time
        
    def tick(self):
        self.time = self.time + 1
            
    def transition(self, frame_duration):
        if self.time % frame_duration == 0:
            return True
        else:
            return False
        
class Interaction:

    def __init__(self, wheel, keyboard, menu, clock):
        self.wheel = wheel
        self.clock = clock
        self.keyboard = keyboard
        self.menu = menu
        self.collision = False
        self.circles = []
        self.projectiles = []
   

           
                      
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
    
    def draw(self, canvas):
        centre = (self.wheel.frame_width * self.wheel.frame_index[0] + self.wheel.frame_centre_x,
                self.wheel.frame_height * self.wheel.frame_index[1] + self.wheel.frame_centre_y)
        if menu.active == False:
            
            if self.keyboard.right and self.clock.transition(time):
                self.wheel.vel.add(Vector(1, 0))
                self.wheel.next_frame()
                self.wheel.update()
                self.wheel.clockwise = True
                
            if self.keyboard.left and self.clock.transition(time):
                self.wheel.vel.add(Vector(-1,0))
                self.wheel.last_frame()
                self.wheel.update()
                self.wheel.clockwise = False
                
            if self.keyboard.space:
                if self.wheel.ground_check() == True:
                    self.keyboard.space = False
                    self.wheel.vel.add(Vector(0,-50))
                    self.wheel.next_frame()
                    self.wheel.update()

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
                
            wheel.update()
            dest_size = (100,100)
            self.clock.tick()
            canvas.draw_text(('Distance:' + str(self.wheel.distance)), (20, 50), 50, 'Blue')
            canvas.draw_image(self.wheel.SHEET_URL, centre, self.wheel.width_height.get_p(), self.wheel.pos.get_p(), dest_size)
            circles = self.circles
            for circle in circles:
                circle.draw(canvas)
   
        else:
            if self.keyboard.p:
                wheel.reset_wheel()
                self.generate()
                menu.set_inactive()
            elif self.keyboard.q:
                quit()
            menu.draw(canvas)
         

kbd = Keyboard()
wheel = Wheel(SHEET_URL, SHEET_WIDTH, SHEET_HEIGHT, COLUMNS, ROWS)
menu = Menu()
clock = clock(time)
inter = Interaction(wheel, kbd, menu, clock)


    
frame = simplegui.create_frame('Interactions', WIDTH, HEIGHT)
frame.set_draw_handler(inter.draw)
frame.set_canvas_background('#31CAF3')
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
