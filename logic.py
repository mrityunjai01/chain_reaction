import sys
import os
import pygame
xlen = 10
ylen = 10


class board:
    def __init__(self, xlen=10, ylen=10):
        self.xlen = xlen
        self.ylen = ylen
        self.board = []

    def init_board(self):
        self.arr = [[cell(x, y, board=self) for y in range(1, ylen+1)]
                    for x in range(1, xlen+1)]

    def init_board_cells(self):
        try:
            for i in self.arr:
                for j in i:
                    j.init_neighbours()

        except AttributeError:
            self.init_board()

    def restart_game(self):
        try:
            for i in self.arr:
                for j in i:
                    j.number = 0
                    j.side = None
        except AttributeError:
            self.init_board()
            self.init_board_cells()

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

    def move(self):
        if self.number < self.capacity:
            self.number += 1
        else:
            self.number = 0
            myside = self.side
            self.side = None
            for x, y in self.n:
                a = self.b.arr[x-1][y-1]
                a.side = myside
                a.move()


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
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('chain reaction')
clock = pygame.time.Clock()
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))


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


def play_display():
    gameExit = False
    while not gameExit:
        pass
