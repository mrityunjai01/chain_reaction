import pygame
import time
import sys, os
import random
pygame.init()
pause = False
dodged = 0
display_width = 800
display_height = 600
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 200, 0)
brightgreen = (0, 255, 0)
red = (205, 0, 0)
brightred = (255, 0, 0)
white = (255, 255, 255)

car_width = 73
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('race')
clock = pygame.time.Clock()
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
gameIcon = pygame.image.load(resource_path('carIcon.png'))
pygame.display.set_icon(gameIcon)
crashed = False

class obstacle:
    def __init__(self, x = 0, y = 0, width = display_width/10, height = display_height/10, speed = 7, initobject=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.initialwidth = width
        self.initialspeed = speed
    def reset(self):
        self.speed = self.initialspeed
        self.width = self.initialwidth
        self.y=0

obs1 = obstacle(x=100, y = 0, width = 100, height = 100, speed = 4)
obs2 = obstacle(20, 0, 20, 100, 8)
obstacle_list = [obs1, obs2]
carImg = pygame.image.load(resource_path('racecar.png'))
def quitGame():
    pygame.quit()
    quit()
def message_display(text):
    writeText(text, textsize=120)
    pygame.display.update()
    
def restart():
    init_game()
    gameloop()
    
    
def crash():
    writeText('Crash', textsize=120)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        interactive_button("Restart", 150, 450, 130, 50, green, brightgreen, restart)
        interactive_button("Quit", 550, 450, 100, 50, red, brightred, quitGame)
        pygame.display.update()
        clock.tick(10)

def drawRect(startx, starty, width, height, color):
    pygame.draw.rect(gameDisplay, color, [startx, starty, width, height])


def writeText(text='Sample text', textfont='freesansbold.ttf', textsize=50, textcolor=black, x=display_width/2, y=display_height/2):
    textS = pygame.font.Font(textfont, textsize).render(text, True, textcolor)
    textR = textS.get_rect()
    textR.center = (int(x), int(y))
    gameDisplay.blit(textS, textR)

def car(x, y):
    gameDisplay.blit(carImg, (x, y))
def things_dodged(count):
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))
def interactive_button(txt, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    writeText(txt, textsize = int(0.8*h), x=x+w/2, y=y+h/2)

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms", 115, bold=False, italic=False)
        textSurface = largeText.render("A bit racey", True, black)
        textRect = textSurface.get_rect()
        textRect.center = (int(display_width/2), int(display_height/2))
        gameDisplay.blit(textSurface, textRect)
        interactive_button("GO!", 150, 450, 100, 50, green, brightgreen, gameloop)
        interactive_button("Quit", 550, 450, 100, 50, red, brightred, quitGame)
        pygame.display.update()
        clock.tick(10)
def init_game():
    global dodged
    dodged = 0
    for obs in obstacle_list:
        obs.reset()        
def paused():
    writeText('Paused', textsize=100)
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        interactive_button("Continue", 150, 450, 180, 50, green, brightgreen, gameloop)
        interactive_button("Quit", 550, 450, 100, 50, red, brightred, quitGame)
        pygame.display.update()
        clock.tick(15)
    
def gameloop():
    x = (int(display_width * 0.45))
    y = (int(display_height * 0.8))
    gameExit = False
    pause = False
    x_change=0
    global dodged
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        x += x_change
        gameDisplay.fill(white)
        things_dodged(dodged)
        for obs in obstacle_list:
            drawRect(obs.x, obs.y, obs.width, obs.height, blue)
            obs.y += obs.speed
            if (obs.y > display_height):
                obs.y = 0 - obs.height
                obs.x = random.randrange(0, display_width)
                dodged += 1
                obs.width += (dodged*1.2)
                obs.speed += 1
            if y < obs.y + obs.height:
                if obs.x < x + car_width and obs.x > x - obs.width:
                    print('crossover')
                    crash()
        car(x, y)
        if x > display_width - car_width or x < 0:
            crash()
        pygame.display.update()
        clock.tick(30)


init_game()
game_intro()
pygame.quit()
quit()
