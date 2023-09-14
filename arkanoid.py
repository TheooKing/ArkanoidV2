import time
import pygame
from random import randint
pygame.init()

#initializing the colors
# R G B
# (Red, Green, Blue)
BACKDROP = (200,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 51)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)
BLUE = (80, 80, 255)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (250, 128, 114)
BLACK = (0,0,0)

#creating the screen
mw = pygame.display.set_mode((500,500))
mw.fill(BACKDROP)

#initializing the time
clock = pygame.time.Clock()

#initializing the game "logic"
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=BACKDROP):
        self.rect = pygame.Rect(x,y,width,height)
        self.fill_color = color
    
    def n_color(self,ncolor):
        self.fill_color = ncolor

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def outline(self, thic=1, frame_color=BLACK):
        pygame.draw.rect(mw, frame_color, pygame.Rect(self.rect.x - thic, self.rect.y - thic, self.rect.width + thic*2 , self.rect.height + thic*2), thic)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)
    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Label(Area):
    def set_text(self, text, tsize=12, tcolor=BLACK, tbold=False):
        self.image = pygame.font.SysFont('verdana', tsize, tbold).render(text, True, tcolor)

    def drawtext(self, shift_x=0, shift_y=0,fillbfr=True):
        if fillbfr == True:
            self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=BACKDROP)
        self.image = pygame.image.load(filename)
    
    def display(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

platfrom_x = 200
platfrom_y = 350
move_right = False
move_left = False

ball = Picture('ball.png',160,200,50,50)
platform = Picture('platform.png',platfrom_x,platfrom_y,100,30)

# initializing for the platform
start_x = 5
start_y = 5 

# initializing for the for loops
count = 9
rows = 3

#initializing the monsters
monsters = []
for i in range(rows):
    y = start_y + (55 * i)
    x = start_x + (25 * i)
    for j in range(count):
        mon = Picture('enemy.png', x,y,50,50)
        monsters.append(mon)
        x += 55
    count -= 1
# initializing for the movement of the ball
dx = 5
dy = 5


game_over = False
while not game_over:
    mw.fill(BACKDROP)

    # game input by the keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False

    if move_right:
        platform.rect.x += 20
    if move_left:
        platform.rect.x -= 20

    #moving the ball
    ball.rect.x += dx
    ball.rect.y += dy

    # moving the ball from collision
    if ball.rect.y < 0:
        dy *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        dx *= -1
    
    #check winning state
    if ball.rect.y > 350:
        time_text = Label(150,150,50,50)
        time_text.set_text('YOU LOSE',60, (255,0,0))
        time_text.drawtext(10, 10)
        game_over = True
    if len(monsters) == 0:
        time_text = Label(150,150,50,50)
        time_text.set_text('YOU WIN',60, (0,200,0))
        time_text.drawtext(10, 10)
        game_over = True
    if ball.rect.colliderect(platform.rect):
        dy *= -1
    # displaying the sprites
    for m in monsters:
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            dy *= -1

    for i in monsters:
        i.display()
    platform.display()
    ball.display()
    pygame.display.update()
    clock.tick(40)
