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
            for x, y in self.n:
                a=self.b.arr[x-1][y-1]
                a.side = self.side
                a.move()
def input_move(myside, board1):
    while True:
        b = input('your move: q to quit ')
        if b=='q':
            return 1
        b=b.strip().split(' ')
        if len(b) < 2:
            print('that was one value try again')
            continue
        x = int(b[1])
        y = int(b[0])
        if x<=board1.xlen and x > 0:
            if y <= board1.ylen and y >0:
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
def play():
    board1 = board()
    board1.init_board()
    board1.init_board_cells()
    gameExit = False
    while not gameExit:
        print(board1)
        if input_move('a', board1):
            break
        print(board1)
        if input_move('c', board1):
            break
play()     
