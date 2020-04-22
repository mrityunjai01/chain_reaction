import sys
import os
import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE
xlen = 10
ylen = 10

class board:
    def __init__(self, xlen=10, ylen=10):
        self.xlen = xlen
        self.ylen = ylen
        self.board = []

    def init_board(self):
        self.arr = [[cell(x, y, board=self) for y in range(1, self.ylen+1)]
                    for x in range(1, self.xlen+1)]

    def init_board_cells(self):
        try:
            for i in self.arr:
                for j in i:
                    j.init_neighbours()

        except AttributeError:
            self.init_board()

    def restart_game(self):
        print("inside restart")
        try:
            for i in self.arr:
                for j in i:
                    j.number = 0
                    j.side = None
        except AttributeError:
            self.init_board()
            self.init_board_cells()
        if hasattr(self.arr[0][0], 'btn'):
            for i in self.arr:
                for j in i:
                    if hasattr(j.btn, 'img'):
                        del(j.btn.img)
                        j.btn.draw()


    def __str__(self):
        s = ""
        for i in self.arr:
            for j in i:
                s += (str(j.side)[0] + " |" + str(j.number)[0]+"| ")
            s += '\n\n'
        return s


board1 = board()


class cell():
    def __init__(self, x, y, capacity=3, number=0, board=board1):

        self.number = number
        self.side = None
        self.x = x
        self.y = y
        self.b = board

    def init_neighbours(self):
        x = self.x
        y = self.y
        l = [(x-1, y), (x+1, y), (x, y+1), (x, y-1)]
        self.n = []
        for i in l:
            if self.b.xlen >= i[0] > 0 and self.b.ylen >= i[1] > 0:
                self.n.append(i)
        self.capacity = len(self.n)-1

    def move(self, unknown_side=None):
        print('started moving {0} {1}'.format(self.x, self.y))
        if self.side == None:
            self.side = unknown_side
            if unknown_side == None:
                print(f"can't move over empty cell {self.x} {self.y}")
                return
        if self.number < self.capacity:
            self.number += 1
        else:
            self.number = 0
            myside = self.side
            self.side = None
            try:
                for x, y in self.n:
                    a = self.b.arr[x-1][y-1]
                    a.side = myside
                    a.move()
            except RecursionError:
                print("Too much recursion in call, aborting...")
        if hasattr(self, 'btn'):
            if self.number > 0:
                self.btn.img = img_side[self.side][self.number-1]
            else:
                self.btn.img = None
            self.btn.draw()

def input_move(myside, board1):
    while True:
        b = input('your move: q to quit ')
        if b == 'q':
            return 1
        b = b.strip().split(' ')
        if len(b) < 2:
            print('that was one value try again')
            continue
        x = int(b[1])
        y = int(b[0])
        if x <= board1.xlen and x > 0:
            if y <= board1.ylen and y > 0:
                c = board1.arr[x-1][y-1]
                if c.side == myside:
                    c.move()
                    return None
                elif c.side == None:
                    c.side = myside
                    c.move()
                    return None
                else:
                    print("that's not your cell")
            else:
                print('your x was not right')
        else:
            print('your x was not right')


def count(side, b):
    cnt = 0
    for i in b.arr:
        for j in i:
            if j.side == side:
                cnt += 1
    return cnt


def play():
    board1 = board()
    board1.init_board()
    board1.init_board_cells()
    gameExit = False
    print(board1)
    if input_move('a', board1):
        gameExit = True
    print(board1)
    if input_move('c', board1):
        gameExit = True
    while not gameExit:
        print(board1)
        if count('a', board1) == 0:
            print('a lost')
            break
        if input_move('a', board1):
            break

        print(board1)
        if count('c', board1) == 0:
            print('c lost')
            break
        if input_move('c', board1):
            break


pygame.init()
display_height = 800
display_width = 600
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
gray = (220, 220, 220)
gameDisplay = pygame.display.set_mode(
    (display_width, display_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption('chain reaction')
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

inactive_color = white
active_color = gray
clicked_color = blue
gameIcon = pygame.image.load('imgs/gameIcon.png')
pygame.display.set_icon(gameIcon)
try:
    redlist = [pygame.image.load(resource_path('imgs/one_red.png')), pygame.image.load(
        'imgs/two_red.png'), pygame.image.load('imgs/three_red.png')]
    greenlist = [pygame.image.load('imgs/one_green.png'), pygame.image.load(
        'imgs/two_green.png'), pygame.image.load('imgs/three_green.png')]
except pygame.error:
    print("couldn't open images")

img_side = {'a' : greenlist, 'c': redlist}
class Button():
    def __init__(self, x, y, w, h, c):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = inactive_color
        self.c=c
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.ic = inactive_color
    def draw(self, img = None):
        pygame.draw.rect(gameDisplay, self.color, self.rect)
        pygame.draw.rect(gameDisplay, (0, 0, 0), self.rect, 1)
        if img != None:
            self.img = img
        if hasattr(self, 'img') and self.img!=None:
            gameDisplay.blit(pygame.transform.scale(self.img, (self.w, self.h)), (self.x, self.y))
    def __str__(self):
        return str(self.rect)
class NormalButton():
    def __init__(self, x, y, text, ic, ac, callback):
        self.x = x
        self.y = y
        self.text = text
        self.action = callback
        self.ac = ac
        self.ic = ic
        self.color = ic

    def create_button(self):
        self.surf = pygame.font.Font(None, 50).render(self.text, True, black)
        self.rect = self.surf.get_rect(topleft=(self.x, self.y))

    def draw(self, screen=gameDisplay):
        try:
            pygame.draw.rect(screen, self.colpr, self.rect)
            screen.blit(self.surf, self.rect)
        except AttributeError:
            self.create_button()
            pygame.draw.rect(screen, self.color, self.rect)
            screen.blit(self.surf, self.rect)


def writeText(text='Sample text', textfont='freesansbold.ttf', textsize=50, textcolor=black, x=display_width/2, y=display_height/2):
    textS = pygame.font.Font(textfont, textsize).render(text, True, textcolor)
    textR = textS.get_rect()
    textR.center = (int(x), int(y))
    gameDisplay.blit(textS, textR)


def img_button(img, x, y, w, h, ic, ac, border, cell, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h), border)
        if click[0] == 1 and action != None:
            print('clicked an img button')
            action()
            print(cell.b)

    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    img = pygame.transform.scale(img, (w, h))
    gameDisplay.blit(img, (x, y))


def interactive_button(txt, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    writeText(txt, textsize=int(0.8*h), x=x+w/2, y=y+h/2)


def empty_button(x, y, w, h, ic, ac, border, c, side):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1:
            print('clicked an empty button')
            c.side = side
            c.move()
            print(c.b)
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

def quitGame():
    pygame.quit()
    quit()
def oops():
    print("that's not your cell")


sideref = 0
sides = ['a', 'c']


def movefromside(cell, side):
    cell.side=side
    cell.move()
    global sideref
    sideref = 1-sideref

sideref = 0
count = 0
def play_display(b=board1):
    b.init_board()
    b.init_board_cells()
    gameExit = False
    sideref = 0
    sides = ['a', 'c']
    x_init, y_init = 0, 0
    xlen, ylen = b.ylen, b.xlen
    x_dstep = int(display_width/b.ylen)
    y_dstep = int(display_height/b.xlen)
    x_dstep = y_dstep = min(x_dstep, y_dstep)
    buttonlist = []
    normalButtonList = []
    normalButtonList.append(NormalButton(x_dstep, display_height-100, "Quit", (0, 0, 215), (0, 0, 255), quitGame))
    normalButtonList.append(NormalButton(x_dstep+100, display_height-100, "Restart", (0, 160, 0), (0, 255, 0), b.restart_game))
    for i in range(ylen):
        for j in range(xlen):
            x = x_init + j * x_dstep
            y = y_init + i * y_dstep
            b.arr[i][j].btn = Button(x, y, x_dstep, y_dstep, b.arr[i][j])
            buttonlist.append(b.arr[i][j].btn)
            
    gameDisplay.fill(white)
    for button in buttonlist:
        button.draw()
    for button in normalButtonList:

        button.draw()
        # print(button)
    hovered_list = []
    while not gameExit:
        turn = sides[sideref]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type ==pygame.MOUSEBUTTONDOWN:
                for button in buttonlist:
                    if button.rect.collidepoint(event.pos):
                        if button.c.side != None and button.c.side != turn:
                            print ("don't be smart, do your turn")
                            break
                        button.c.move(turn)
                        sideref = 1 - sideref
                        button.draw()
                # print(b)
                        break
                for button in normalButtonList:
                    if button.rect.collidepoint(event.pos):
                        button.action()
            if event.type == pygame.MOUSEMOTION:
                for btton in buttonlist:
                    # print(f"{btton}")
                    if btton.rect.collidepoint(event.pos):
                        # print(f"hovered over {btton.c.x} {btton.c.y}")
                        btton.color = active_color
                        btton.draw()
                        if btton not in hovered_list:
                            while hovered_list:
                                hvbtn = hovered_list.pop()
                                hvbtn.color = hvbtn.ic
                                hvbtn.draw()
                            hovered_list.append(btton)
                        break
                for btton in normalButtonList:
                    if btton.rect.collidepoint(event.pos):
                        btton.color = btton.ac
                        btton.draw()
                        if btton not in hovered_list:
                            while hovered_list:
                                hvbtn = hovered_list.pop()
                                hvbtn.color = hvbtn.ic
                                hvbtn.draw()
                            hovered_list.append(btton)


        pygame.display.update()
        clock.tick(30)
play_display(board(xlen=5, ylen = 8))
