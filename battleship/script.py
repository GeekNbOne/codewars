from math import sqrt
ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


class Coord(object):


    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Coord(self.x - other.x,self.y - other.y)

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)


    def __len__(self):
        return int(sqrt(self.x*self.x + self.y * self.y))

    def __str__(self):
        return f'({self.x},{self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ship(object):

    class shipIter(object):

        def __init__(self,sp,ep):
            self._sp = sp
            self._current = None
            self._ep = ep
            self.l = len(self._ep - self._sp)

            self._add = Coord(0,1) if (self._sp.x - self._ep.x ==0) else Coord(1,0)


        def __iter__(self):
            return self

        def __next__(self):

            if self._current is None:
                self._current = self._sp
            else:
                if self._current == self._ep:
                    raise StopIteration

                self._current += self._add

            return self._current



    def __init__(self,start_point,end_point):
        self._start_point = start_point
        self._end_point = end_point

    def __len__(self):
        return len(self._end_point - self._start_point) +1

    def __iter__(self):
        return self.shipIter(self._start_point,self._end_point)

    def __repr__(self):
        return f'Ship@{self._start_point}->{self._end_point}'

class Board(object):

    def __init__(self,board):
        self._board = board


    def add_ship(self,ship):
        for c in ship:
            self._board[c.x][c.y] = 0

    def remove_ship(self,ship):
        for c in ship:
            self._board[c.x][c.y] = 1

    def sum(self):
        return sum([j for i in self._board for j in i])

    @property
    def sum_valid(self):
        return self.sum() == 4 + 3*2 + 2*3 + 4


    def __str__(self):
        return '\n'.join(['|'.join([str(j) for j in i]) for i in (self._board)])


def search(board, ships, last_ship=None, x=0, y=0, xp=0, yp=0):
    if len(ships) ==0:
        return True

    ship = ships.pop(0)


    if last_ship != ship:
        x = 0
        y = 0
        xp = 0
        yp = 0


    x,y,xp,yp = scan(board,ship,True,x,y)
    if x < 10 or y < 10:
        val = search(board,ships,ship,x,y,xp,yp)

        if val:
            return val

    x,y,xp,yp = scan(board, ship, False, xp, yp)
    if xp < 10 or yp <10:
        val = search(board, ships, ship, x, y, xp, yp)

        if val:
            return val

    return False


def scan(board,ship,horiz,x,y):
    for i in range(x, len(board)):
        acc = 0
        for j in range(y, len(board[i])):
            try:
                if horiz:
                    r = i
                    c = j
                else:
                    r = j
                    c = i

                if board[r][c] == 1:
                    acc += 1
                else:
                    acc = 0


                if acc == ship:
                    if horiz:
                        return r,c,0,0
                    else:
                        return 10,10,c,r

            except:
                print(i, j)
                raise
    if horiz:
        return 10,10,0,0
    else:
        return 10,10,10,10

board = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
         [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
         [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]



s = Ship(Coord(0,0),Coord(4,0))

b = Board(board)
print(b)
b.add_ship(s)
print('----')
print(b)

print(b.sum_valid)