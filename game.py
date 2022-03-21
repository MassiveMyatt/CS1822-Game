from user304_rsf8mD0BOQ_1 import Vector

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math
import time
import random

WIDTH = 1200
HEIGHT = 600
STEP = 0.5
SHEET_WIDTH = 1440
SHEET_HEIGHT = 1480
COLUMNS = 6
ROWS = 5
SHEET_URL = "https://i.imgur.com/GQy2YrF.png"
time = 1

class Menu:
    def __init__(self):
        self.active = True
        self.scores = []
    
    def draw(self, canvas):
        canvas.draw_text('Insert Cool Game Name Here', (50, 50), 50, 'Red')
        canvas.draw_text('Press P To Play', (100, HEIGHT / 2), 30, 'Red')
        canvas.draw_text('Press Q to exit',(100, HEIGHT - 30), 30, 'Red')
        if len(self.scores) > 0:
            self.scores = list(dict.fromkeys(self.scores))
            self.scores.sort()
            canvas.draw_text('High Score: ' + str(self.scores[len(self.scores) - 1]), (100, HEIGHT / 3), 30, 'Yellow')
            canvas.draw_text('YOU DIED!', (WIDTH / 2, HEIGHT / 2), 50, 'Red')

    def set_inactive(self):
        self.active = False
        
        
    def set_active(self):
        self.active = True
        

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

class Player:
    def __init__(self, SHEET_URL, WIDTH, HEIGHT, COLUMNS, ROWS, radius = 30):
        self.pos = Vector(0,0)
        self.vel = Vector(0,0)
        self.radius = 30
        self.lives = 3
        self.wrapped = False
        self.levels_completed = 0
        self.time_reduction = 1
        self.time_elapsed = 30
        self.distance = 0
        
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
    
    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.COLUMNS
        if self.frame_index[0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.ROWS

    def last_frame(self):
        self.frame_index[0] = (self.frame_index[0] - 1) % self.COLUMNS
        if self.frame_index[0] == 0:
            self.frame_index[1] = (self.frame_index[1] - 1) % self.ROWS
        
    
    def update(self):
        self.damage_taken = False
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

            
        if self.vel.x > 1:
            self.distance += 1
        if player.pos.y > HEIGHT:
            self.take_damage()
        if self.time_elapsed <= 0:
            self.lives = 0
    

    def bottom(self):
        return self.pos + Vector(0, self.radius)
    
    def top(self):
        return self.pos - Vector(0, self.radius)
    
    def take_damage(self):
        self.lives -= 1
        self.damage_taken = True
        self.vel = Vector(0,0)
    
    def wrap(self):
        position = self.pos.get_p()
        if position[0] + self.radius > WIDTH and self.pos.y > 0: #wrap r -> l
            self.pos = Vector(50, HEIGHT - 50)
            self.wrapped = True
            self.levels_completed += 1
            self.time_reduction += 1
            self.vel = Vector(0,0)
        else:
            self.wrapped = False
     
    
    def reset(self):
        self.alive = True
        self.pos = Vector(100, HEIGHT / 2) 
        self.vel = Vector(0,0)
        self.wrapped = False
        self.levels_completed = 0
        self.damage_taken = False
        self.lives = 3
        self.time_elapsed = 30
        self.time_reduction = 1
        timer.stop()
    
        
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
    def __init__(self, player, keyboard, menu, clock):
        self.player = player
        self.keyboard = keyboard
        self.menu = menu
        self.clock = clock
        self.platforms = []
        self.maxDistance = 300
        self.maxHeight = 300
        self.minDistance = 150
        
    
    def draw(self, canvas):
        centre = (self.player.frame_width * self.player.frame_index[0] + self.player.frame_centre_x,
                self.player.frame_height * self.player.frame_index[1] + self.player.frame_centre_y)
        dest_size = (100,100)
        if self.menu.active == False:
            self.update()
            canvas.draw_image(self.player.SHEET_URL, centre, self.player.width_height.get_p(), self.player.pos.get_p(), dest_size)
            canvas.draw_text(('LEVELS COMPLETED:' + str(self.player.levels_completed)), (20, 50), 50, 'Red')
            canvas.draw_text(('LIVES:' + str(self.player.lives)), (20, 100), 50, 'Red')
            canvas.draw_text(('TIME LEFT: ' + str(self.player.time_elapsed)),(20, 150), 50, 'Red')
            for platform in self.platforms:
                platform.draw(canvas)
        else:
            self.update()
            self.menu.draw(canvas)

    def update(self): 
        if self.menu.active == False:
            self.player.update()
            
            if self.player.damage_taken == True:
                self.player.pos = Vector(50, HEIGHT - 50)
            
            if self.player.lives <= 0:
                self.menu.scores.append(self.player.levels_completed)
                self.player.reset()
                self.reset_difficulty()
                self.menu.set_active()
                self.platforms = []
            
            if self.player.wrapped == True:
                self.increase_difficulty()
                self.platforms = []
                self.generate_platforms()
                self.player.time_elapsed = 30 - self.player.time_reduction
           
            on_platform = False

            for platform in self.platforms:
                on_platform |= platform.interact(player)
                platform.update()
                
            if on_platform:   
                if self.keyboard.right and self.clock.transition(time):
                    self.player.vel.add(Vector(1, 0))
                    self.player.next_frame()
                    self.player.update()
                    self.player.clockwise = True
                
                if self.keyboard.left and self.clock.transition(time):
                    self.player.vel.add(Vector(-1,0))
                    self.player.last_frame()
                    self.player.update()
                    self.player.clockwise = False
                
                if self.keyboard.space:
                    self.keyboard.space = False
                    self.player.vel.add(Vector(0,-65))
                    self.player.next_frame()
                    self.player.update()
                self.player.vel.multiply(0.9)
            else:
                if self.keyboard.right and self.clock.transition(time):
                    self.player.vel.add(Vector(1, 0))
                    self.player.next_frame()
                    self.player.update()
                    self.player.clockwise = True
                
                if self.keyboard.left and self.clock.transition(time):
                    self.player.vel.add(Vector(-1,0))
                    self.player.last_frame()
                    self.player.update()
                    self.player.clockwise = False
                
                self.player.vel.add(Vector(0, 1))
                self.player.vel.multiply(0.93)
                
        else:
            if self.keyboard.p:
                timer.start()
                self.generate_platforms()
                self.menu.set_inactive()
            elif self.keyboard.q:
                quit()
                    

     
    def generate_platforms(self):
        xstartprev = 50
        yprev = HEIGHT - 50
        platform_start = Platform(HEIGHT - 50, 0, 150, 0)  
        self.platforms.append(platform_start)
        amount = random.randint(5, 15)
        for platform in range (0, amount):
            y = yprev + random.uniform(-250.5,250.5 )
            if y > HEIGHT:
                y = HEIGHT - 100
            xstart = xstartprev + random.uniform(self.minDistance, self.maxDistance)
            length = random.randint(50, 150)
            xend = xstart + length + random.randint(10,50)
            xstartprev = xstart
            yprev = y
            velocity = random.uniform(-2.5, 2.5)
            platform = Platform(y, xstart, xend, velocity)
            self.platforms.append(platform)
     
    
    def increase_difficulty(self):
        self.maxHeight = self.maxHeight * 1.05
        self.maxDistance = self.maxDistance * 1.05
        self.minDistance = self.minDistance * 1.02
    
    def reset_difficulty(self):
        self.maxHeight = 300
        self.maxDistance = 300
        self.minDistance = 300
    
    def timer(self):
        self.player.time_elapsed -= 1
            

class Platform:
    def __init__(self, y, xstart, xend, vel):
        self.y = y
        self.y_copy = self.y
        self.xstart = xstart
        self.xend = xend 
        self.width = 20
        self.top = self.y - self.width / 2
        self.colour = "#C970F3"
        self.bottom = self.y + self.width / 2
        self.in_collision = set()
        self.vel = vel
    
    def draw(self, canvas):
        canvas.draw_line((self.xstart, self.y),(self.xend, self.y),self.width,self.colour)
    
    def hit(self, player):
        bottom = player.bottom()
        top = player.top()
        return (bottom.y > self.top and self.xstart < bottom.x
                and bottom.x < self.xend and top.y < self.bottom)
    
    def interact(self, player): 
        if self.hit(player):
            if not player in self.in_collision:
                self.in_collision.add(player)
                if player.vel.y >= 0:
                    player.vel.y = 0
                    player.pos.y = self.top - player.radius
                    return True
                else:
                    player.vel.y = 0
        else:
            self.in_collision.discard(player)
        return False
    
    
    def update(self):
        
        self.xstart += self.vel
        self.xend += self.vel
        
        if self.xend >= WIDTH:
            self.vel *= -1
        
        elif self.xstart <= 0:
            self.vel *= -1
    
        
        
menu = Menu()            
keyboard = Keyboard()
clock = clock(time)
player = Player(SHEET_URL, SHEET_WIDTH, SHEET_HEIGHT, COLUMNS, ROWS)
interaction = Interaction(player, keyboard, menu, clock)

frame = simplegui.create_frame('Interactions', WIDTH, HEIGHT)
frame.set_draw_handler(interaction.draw)
frame.set_canvas_background('Blue')
frame.set_keydown_handler(keyboard.keyDown)
frame.set_keyup_handler(keyboard.keyUp)
timer = simplegui.create_timer(1000, interaction.timer)
frame.start()
