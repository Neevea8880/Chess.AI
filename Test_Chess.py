from Chess import Chess
from copy import deepcopy

class Test():
    def __init__(self):
        try: from Chess import Chess
        except: print('Unable to import Chess from Chess')
        try: self.game = Chess()
        except: print('Unable to initialize Game')

        tests = [method for method in dir(Test) if not method.startswith('__')]
        for i, test in enumerate(tests):
            print('TEST', i, test)
            exec('self.'+test+'()')


def printgrid(g):
    for row in g:
        print('<', end='')
        for cell in row:
            if cell==True: print('#', end='')
            elif cell==False: print(' ', end='')
        print('>')

def Knightmoves(grid, x, y):
    g=deepcopy(grid)
    for dy in range(y-2, y+3):
        for dx in range(x-2, x+3):
            print('cell', dx, dy,':', end='')
            if 0<=dx<8 and 0<=dy<8 and dx!=x and dy!=y and abs(dx-x)!=abs(dy-y):
                g[dy][dx]=True
    return g

def BishopMoves(grid, x, y):
    g = deepcopy(grid)
    print('Bishop at', x, y)
    for k in range(0, 8):
        if 0<=y-(x-k)<8:
            print('cell', k, '%d-(%d-%d) ='%(y, x, k),y-(x-k))
            g[k][y-(x-k)] = True
        if 0<=y+(x-k)<8:
            print('cell', k, '%d+(%d-%d) ='%(y, x, k), y+(x-k))
            g[k][y+(x-k)] = True
    return g

def testRook():
    global game
    game = game.makeMove('a2', 'a4'); print(game)
    game = game.makeMove('h7', 'h5'); print(game)
    game = game.makeMove('a1', 'a3'); print(game)
    game = game.makeMove('h8', 'h6'); print(game)
    print('checkableMoves(a3)')
    print(game.checkableMoves('a3'))
def testBishop():
    global game
    game = game.makeMove('d2', 'd3'); print(game)
    game = game.makeMove('e7', 'e6'); print(game)
    print('checkableMoves(c1)')
    print(game.checkableMoves('c1'))
    game = game.makeMove('c1', 'f4'); print(game)
    print('checkableMoves(f4)')
    print(game.checkableMoves('f4'))
def testEnPassant():
    global game
    game = game.makeMove('d2', 'd4'); print(game)
    game = game.makeMove('e7', 'e5'); print(game)
    game = game.makeMove('d4', 'e5'); print(game)
    game = game.makeMove('f7', 'f5'); print(game)
    print('movesOf(e5) :', game.movesOf('e5'))
    game = game.makeMove('e5', 'f6'); print(game)
def testCastling():
    global game
    game = game.makeMove('e2', 'e4')
    game = game.makeMove('e7', 'e5')
    game = game.makeMove('f2', 'f4')
    game = game.makeMove('f7', 'f5')
    game = game.makeMove('g2', 'g4')
    game = game.makeMove('g7', 'g5')
    game = game.makeMove('h2', 'h4')
    game = game.makeMove('h7', 'h5')
    game = game.makeMove('d2', 'd4')
    game = game.makeMove('d7', 'd5')
    game = game.makeMove('c2', 'c4')
    game = game.makeMove('c7', 'c5')
    game = game.makeMove('b2', 'b4')
    game = game.makeMove('b7', 'b5')
    game = game.makeMove('a2', 'a4')
    game = game.makeMove('a7', 'a5')
    game = game.makeMove('b1', 'c3')
    game = game.makeMove('b8', 'c6')
    game = game.makeMove('c1', 'a3')
    game = game.makeMove('c8', 'a6')
    game = game.makeMove('d1', 'd3')
    game = game.makeMove('d8', 'd6')
    game = game.makeMove('f1', 'h3')
    game = game.makeMove('f8', 'h6')
    game = game.makeMove('g1', 'f3')
    game = game.makeMove('g8', 'f6'); print(game)
def testCastleCheck():
    global game
    game = game.makeMove('d2','d4')
    game = game.makeMove('d7','d5')
    game = game.makeMove('c1','g5')
    game = game.makeMove('e7','e6')
    game = game.makeMove('b1','c3')
    game = game.makeMove('d8','g5')
    game = game.makeMove('d1','d3')
    game = game.makeMove('g5','g6')
    game = game.makeMove('d3','c4')
    game = game.makeMove('g6','d3'); print(game)

import code
game = Chess(); print(game)
# testRook()
# testBishop()
# testEnPassant()
# testCastling()
testCastleCheck()
code.interact(banner='', local=dict(globals(), **locals()), exitmsg='')
