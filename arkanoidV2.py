import time
import pygame
from random import randint
import os

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

ball = Picture(os.path.join('assets', 'ball.png'),160,200,50,50)

start_x_ball = ball.rect.x
start_y_ball = ball.rect.y
platform = Picture(os.path.join('assets','platform.png'),platfrom_x,platfrom_y,100,30)


#defining the time counter
timer = Label(15,450,55,50)
timer.set_text("0",35, DARK_BLUE)

#probably we are going to make these buttons a for loop with a list, and every position to be taken as a certain button. 
#defining the buttons after end screen
leave_buttton = Label(200,250,100,25,YELLOW)
leave_buttton.set_text("Leave Game", tbold=True)

play_again = Label(200,200,100,25,YELLOW)
play_again.set_text("Play again", tbold=True)

play_button = Label(200,200,100,25,YELLOW)
play_button.set_text("Play ", tbold=True)

# definning the start screen images
arkanoid_img = Picture(os.path.join("assets","AlgoLogo.png"), 105, 100, 225, 83)

# initializing the speed for the platform
start_x = 5
start_y = 5 

#initializing the list = monsters
monsters = []

# initializing for the movement of the ball
dx = 5
dy = 5

#creating the game loop with the logic
# running[0] = the game loop loop
# running[1] = the actual game loop 
# running[2] = the game state, did tha player win or lose?
# running[3] = Start screen
running = [True,False,True,True]
while running[0]:

    while running[3]:
        mw.fill(BACKDROP)
        arkanoid_img.display()
        play_button.outline(10)
        play_button.drawtext(5,5)

        leave_buttton.n_color(YELLOW)
        leave_buttton.outline(10)
        leave_buttton.drawtext(5,5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if leave_buttton.collidepoint(x,y):
                    leave_buttton.n_color(GREEN)
                    leave_buttton.drawtext(5,5)
                    pygame.display.update()
                    pygame.quit()
                    
                elif play_button.collidepoint(x, y):
                    play_button.n_color(GREEN)
                    play_button.drawtext(5,5)
                    running[1] = True # enable the game loop
                    running[3] = False # leave the current loop

        pygame.display.update()
        clock.tick(40)

    # defaulting some stuff before playing
    if running[1] == True:
        mw.fill(BACKDROP)
        monsters.clear()

        # initializing for the for loops
        count = 9
        rows = 3

        #initializing the monsters
        for i in range(rows):
            y = start_y + (55 * i)
            x = start_x + (25 * i)
            for j in range(count):
                mon = Picture(os.path.join('assets','enemy.png'), x,y,50,50)
                monsters.append(mon)
                x += 55
            count -= 1
        
        # resseting the movemnent
        move_right = False
        move_left = False

        # defaulting the ball and the platofrom
        platform.rect.y = platfrom_y
        platform.rect.x = platfrom_x
        ball.rect.x = start_x_ball
        ball.rect.y = start_y_ball

        #initializing the time
        start_time = time.time()
        cur_time = start_time

        # resseting timer - displaying the resseted timer
        timer.set_text('0',35, DARK_BLUE)
        timer.drawtext()
        

    while running[1] == True:
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
            ball.rect.y = 0
            dy *= -1
        if ball.rect.x > 450 or ball.rect.x < 0:
            dx *= -1

        # moving the platform from collision
        if platform.rect.x < 0:
            platform.rect.x = 0
        if platform.rect.x > 500-platform.rect.width:
            platform.rect.x = 501-platform.rect.width
    
        #check winning state
        if ball.rect.y > 350:
            running[1] = False #leaving the current loop
            running[2] = False #updating the state to lost
        if len(monsters) == 0:
            running[1] = False #leaving the current loop
            running[2] = True #updating the state to lost
        if ball.rect.colliderect(platform.rect):
            dy *= -1
        # displaying the sprites
        for m in monsters:
            if m.rect.colliderect(ball.rect):
                monsters.remove(m)
                dy *= -1

        #displaying time new_time -  start_time
        new_time = time.time()
        if int(new_time - cur_time) == 1:
            timet = new_time -  start_time
            timer.set_text(str(int(timet/60)) + 'm - ' + str(int(timet%60)) +' s' if timet > 59 else str(int(timet))+' s', 35, DARK_BLUE)
            cur_time = new_time

        for i in monsters:
            i.display()
        platform.display()
        ball.fill()
        ball.outline()
        ball.display()
        timer.drawtext(0,0)

        #updates the screen
        pygame.display.update()
        clock.tick(40)

    if running[0]:
        #making the screen to play again or leave
        mw.fill(BACKDROP)
        
        show_state_game = Label(70,110,360,30,RED if running[2]==False else GREEN)
        show_state_game.set_text('You missed the ball...' if running[2]==False else 'You won the invasion of the monsters!!!', 20,tbold=True)
        if running[2]:
            resul_time = Label(100, 150, 300,20)
            timet = new_time - start_time
            resul_time.set_text("Completion time: " + str(str(int(timet/60)) + 'mins' + str(timet%60) + 'sec') if timet > 60 else str(int(timet)),tcolor=DARK_BLUE)
            resul_time.drawtext(2,2)
        show_state_game.drawtext(2,2)

        play_again.n_color(YELLOW)
        play_again.outline(10)
        play_again.drawtext(5,5)

        leave_buttton.n_color(YELLOW)
        leave_buttton.outline(10)
        leave_buttton.drawtext(5,5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if leave_buttton.collidepoint(x,y):
                    leave_buttton.n_color(GREEN)
                    leave_buttton.drawtext(5,5)
                    running[0] = False # leave the game loop loop
                    
                elif play_again.collidepoint(x, y):
                    play_again.n_color(GREEN)
                    play_again.drawtext(5,5)
                    running[1] = True # enable the game loop

        pygame.display.update()
        clock.tick(40)
