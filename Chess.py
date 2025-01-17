from copy import deepcopy
from datetime import datetime


class Player:
    '''Contains implementations of a players functionality.'''
    def __init__(self, White=True):
        pass

class Chess:
    '''Contains all logic for a chess game'''
    def __init__(self, promotion=None, gameString=None):
        """intializes the board and sets the state of the board.

        The choosePiece argument expects a function that returns a character in (Q, R, B, N).
        This function will be used when a pawn is to be promoted. If choosePiece defaults to None,
        the pawn will be promoted to Queen."""
        if not gameString:
            self.board = [
                ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'], #a8 - h8
                ['bP']*8, [None]*8, [None]*8, [None]*8, [None]*8, ['wP']*8,
                ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'], #a1 - h1
            ]
            self.isWhitesMove = True
            self.result = None
            self.wPoints = 0
            self.bPoints = 0
            self.choosePiece = promotion if promotion else lambda:'Q'
            self.log = []
            self.gameString = ''
            self.history = []
            self.fiftyCounter = 0
        else:
            game = Chess(promotion=promotion)
            for i, move in enumerate(gameString.split()):
                if move == 'O-O-O': a, b = (4, 7 if i%2==0 else 0), (2, 7 if i%2==0 else 0)
                elif move == 'O-O': a, b = (4, 7 if i%2==0 else 0), (6, 7 if i%2==0 else 0)
                else:
                    a, b = move.split('x' if 'x' in move else '-')
                    promoteToPiece = b.split('=')[1] if '=' in b else None
                    a = a[1:3] if a[0].isupper() else a[:2]
                    b = b[1:3] if b[0].isupper() else b[:2]
                    game = game.makeMove(a, b, promoteTo=promoteToPiece)
            self.board = game.board
            self.isWhitesMove = game.isWhitesMove
            self.result = game.result
            self.wPoints = game.wPoints
            self.bPoints = game.bPoints
            self.choosePiece = game.choosePiece
            self.log = game.log
            self.gameString = game.gameString
            self.history = game.history
            self.fiftyCounter = game.fiftyCounter
    
    def __str__(game):
        '''prints the board on console'''
        string = '\n'
        for y, row in enumerate(game.board):
            string += '%d| '%(8-y)
            for cell in row:
                if not cell: string += '  '
                elif cell[0]=='b': string += cell[1].lower()+' '
                elif cell[0]=='w': string += cell[1].upper()+' '
            string += '|\n'
        string += '   a b c d e f g h\n'
        return string
    
    def _coords_(game, string):
        '''Accepts a string Chess-cell location and returns x-y tuple indices on the board'''
        return (ord(string[0].lower())-97, 8-int(string[1]))
    
    def _notation_(game, cell):
        '''Accepts a duplet cell, array location and returns a string notation of the cell'''
        return 'abcdefgh'[cell[0]]+str(8-cell[1])
    
    def _FEN_(game):
        '''Returns a Forsyth–Edwards Notation (FEN) of the board without game information.
        Saving boards as strings is expected to speed up history checks when compared to arrays.'''
        fen = ''
        for row in game.board:
            emptyCells = 0
            for cell in row:
                if not cell: emptyCells += 1
                else: 
                    if emptyCells:
                        fen += str(emptyCells)
                        emptyCells = 0
                    fen += cell[1].upper() if cell[0]=='w' else cell[1].lower()
            if emptyCells: fen += str(emptyCells)
            fen += '/'
        return fen[:-1]
    
    def checkResult(game):
        """
        checks for a result from the board.
        1  white won
        -1 black won
        2  quit
        3  stalemate
        4  draw by insufficient material
        5  three-fold repetition
        6  fifty-move rule
        """

        if game.fiftyCounter >= 100:
            game.result = 6
        elif not game.getMoves():
            if game.isCheck():
                if game.isWhitesMove: game.result = -1
                else: game.result = 1
                game.gameString += '#'
            else: game.result = 3
        elif game.history.count(game._FEN_())>=2:
            game.result = 5
        else:
            bp, wp = [], []
            for y in range(8):
                for x in range(8):
                    piece = game.board[y][x]
                    if not piece or piece[1]=='K': continue
                    if piece[0]=='b':
                        bp.append(piece[1])
                        if piece[1]=='B': bbcol = (x+y)%2
                    elif piece[0]=='w':
                        wp.append(piece[1])
                        if piece[1]=='B': wbcol = (x+y)%2
            if bp==wp==[] or \
                (bp==[] and wp==['B']) or (bp==['B'] and wp==[]) or \
                (bp==[] and wp==['N']) or (bp==['N'] and wp==[]) or \
                (bp==wp==['B'] and bbcol==wbcol):
                game.result = 4
            else:
                game.result = None

        return game.result

    def isCheck(game, check_side=None):
        '''Returns a boolean specifying if the current player is in check or not.
        If check_side is set to w or b, checking is made for white or black respectively.'''
        if not check_side: check_side = 'w' if game.isWhitesMove else 'b'
        for y, row in enumerate(game.board):
            for x, cell in enumerate(row):
                if game.board[y][x]==check_side+'K':
                    king=(x, y)
                    break
            else: continue
            break
        for checkPiece in ['P', 'RQ', 'BQ', 'N', 'K']:
            for coord in game.checkableMoves(king, check_side+checkPiece[0]):
                #essentially places a piece in kings cell and finds same enemy pieces in sight
                piece = game.board[coord[1]][coord[0]]
                if piece and piece[0]!=check_side and piece[1] in checkPiece:
                    return True
        return False

    def getMoves(game, current_side=None):
        '''Returns a list of possible moves (pairs of xy coordinate pairs)'''
        if not current_side: current_side = 'w' if game.isWhitesMove else 'b'
        pieces = [
            (x, y) for y, row in enumerate(game.board)
            for x, cell in enumerate(row) if cell!=None and cell[0]==current_side]
        return [
            (piece, move) for piece in pieces
            for move in game.movesOf(piece)]
    
    def legalMoves(self, cell, piece=None):
        '''Returns a list of legal moves for a piece in the cell.
        if piece (PRNBQK) is explicitly specified the rules of that piece would apply.
        This method does not consider the state of the game, only the position of the piece.
        Intended to be used when making PreMoves.'''
        if type(cell)==str: x, y = self._coords_(cell)
        else: x, y = cell[0], cell[1]
        if not piece:
            if not self.board[y][x]: return []
            else: piece = self.board[y][x]
        current_side = piece[0]
        ops = []

        if piece[1] == 'P':
            if current_side=='w' and y>0: d=-1
            elif current_side=='b' and y<7: d=1
            else: return []
            
            ops += [(x, y+d)]
            if (d==1 and y==1) or (d==-1 and y==6): ops += [(x, y+d*2)]
            if x>0: ops += [(x-1, y+d)]
            if x<7: ops += [(x+1, y+d)]

        elif piece[1] == 'R':
            for k in range(0, 8):
                if k!=x: ops.append((k, y))
                if k!=y: ops.append((x, k))

        elif piece[1] == 'N':
            ops = [
                (dx, dy) for dy in range(y-2, y+3) for dx in range(x-2, x+3)
                if 0<=dx<8 and 0<=dy<8 and dx!=x and dy!=y and abs(dx-x)!=abs(dy-y)
            ]

        elif piece[1] == 'B':
            for k in range(0, 8):
                if 0 <= y-(x-k) < 8 and k!=x:
                    ops.append((k, y-(x-k)))
                if 0 <= y+(x-k) < 8 and k!=x:
                    ops.append((k, y+(x-k)))

        elif piece[1] == 'Q':
            ops = self.legalMoves((x, y), current_side+'B') + self.legalMoves((x, y), current_side+'R')

        elif piece[1] == 'K':
            ops = [
                (dx, dy) for dy in range(y-1, y+2)
                for dx in range(x-1, x+2)
                if 0<=dy<8 and 0<=dx<8
            ]
            ops.remove((x, y))
        
        return ops
    
    def checkableMoves(self, cell, piece=None):
        '''Returns a list of squares eyed/targetted by a piece in the cell, 
        This method simply refines the moves from legalMoves according to the game.
        This method Does not however check if the move is completely possible.'''
        
        if type(cell)==str: x, y = self._coords_(cell)
        else: x, y = cell[0], cell[1]
        if not piece:
            if not self.board[y][x]: return []
            else: piece = self.board[y][x]
        current_side = piece[0]
        ops, moves = [], self.legalMoves((x, y), piece)

        if piece[1] == 'P':
            for op in moves:
                if op[0]-x in (1, -1): #sideways move
                    ops.append(op)

        elif piece[1] == 'R':
            for d in range(x+1, 8):
                ops.append((d, y))
                if self.board[y][d]: break
            for d in range(x-1, -1, -1):
                ops.append((d, y))
                if self.board[y][d]: break
            for d in range(y+1, 8):
                ops.append((x, d))
                if self.board[d][x]: break
            for d in range(y-1, -1, -1):
                ops.append((x, d))
                if self.board[d][x]: break

        elif piece[1] == 'N':
            ops = moves

        elif piece[1] == 'B':
            for d in range(1, min(8-x, 8-y)):
                ops.append((x+d, y+d))
                if self.board[y+d][x+d]: break
            for d in range(1, min(8-x, y+1)):
                ops.append((x+d, y-d))
                if self.board[y-d][x+d]: break
            for d in range(1, min(x+1, y+1)):
                ops.append((x-d, y-d))
                if self.board[y-d][x-d]: break
            for d in range(1, min(x+1, 8-y)):
                ops.append((x-d, y+d))
                if self.board[y+d][x-d]: break

        elif piece[1] == 'Q':
            ops = self.checkableMoves((x, y), current_side+'B') + self.checkableMoves((x, y), current_side+'R')

        elif piece[1] == 'K':
            ops = [
                op for op in moves
                if op[0]-x in (-1, 0, 1)
            ]
        return ops
    
    def movesOf(game, cell, piece=None):
        '''implements a check to make sure a piece can move from its current location.
        Also adds special checks for the pawn and the king's moves'''
        if type(cell)==str: x, y = game._coords_(cell)
        else: x, y = cell[0], cell[1]
        if not piece:
            if not game.board[y][x]: return []
            else: piece = game.board[y][x]
        
        current_side = piece[0]
        moves = []
        
        if piece[1]=='P':
            for op in game.legalMoves((x, y), piece):
                if op[0]-x == 0: # straight move
                    if not game.board[op[1]][op[0]]: # empty square
                        if op[1]-y in (1, -1):
                            moves.append(op) # one step
                        elif op[1]-y in (2, -2) and not game.board[(op[1]+y)//2][op[0]]:
                            moves.append(op) # two steps and empty path
                else: # sidemove
                    if game.board[op[1]][op[0]] and game.board[op[1]][op[0]][0]!=current_side: #takes
                        ('takes', game.board[y][x], game.board[op[1]][op[0]])
                        moves.append(op)
                    elif len(game.log)>0 and y==(3 if current_side=='w' else 4) and\
                        op[1]==(game.log[-1][0][1]+game.log[-1][1][1])/2 and\
                        game.log[-1][0][0]==game.log[-1][1][0]==op[0]: # en passant
                            moves.append(op)
        else: moves = game.checkableMoves((x, y), piece)

        # add castling moves
        if piece[1]=='K':
            kingMoved = game.hasMoved((4, 0)) if current_side=='b' else game.hasMoved((4, 7))
            if not kingMoved and not game.isCheck():
                if not game.hasMoved((7, y)) and \
                game.board[y][5]==game.board[y][6]==None and \
                not game.makeMove((4, y), (5, y), True).isCheck(current_side) :
                    moves.append((6, y))
                if not game.hasMoved((0, y)) and \
                game.board[y][1]==game.board[y][2]==game.board[y][3]==None and \
                not game.makeMove((4, y), (3, y), True).isCheck(current_side) :
                    moves.append((2, y))

        # ensure proposed move doesn't have a friendly piece on it and don't result in check
        finalMoves = [ 
            move for move in moves 
            if (not game.board[move[1]][move[0]] or game.board[move[1]][move[0]][0]!=current_side)
            and not game.makeMove((x,y), move, True).isCheck(current_side)
        ]
        return finalMoves
    
    def hasMoved(game, cell):
        '''Returns a boolean that tells wether or not a move has been made from the cell during the game'''
        if type(cell)==str: x, y = game._coords_(cell)
        else: x, y = cell[0], cell[1]
        for move in game.log:
            if list(move[0]) == list((x, y)):
                return True
        return False
    
    def makeMove(game, oldCell, newCell, testMove=False, promoteTo=None):
        '''Returns an instance of the board after having made the move
        testMove is intended for blocking user action in case of possible pawn promotions'''
        if type(oldCell) == str: oldCell = game._coords_(oldCell)
        if type(newCell) == str: newCell = game._coords_(newCell)
        
        if not game.board[oldCell[1]][oldCell[0]] \
        or (game.board[oldCell[1]][oldCell[0]][0]=='w' and not game.isWhitesMove) \
        or (game.board[oldCell[1]][oldCell[0]][0]=='b' and game.isWhitesMove):
            return game

        current_side = game.board[oldCell[1]][oldCell[0]][0]
        g = deepcopy(game)

        # the move
        g.board[newCell[1]][newCell[0]] = g.board[oldCell[1]][oldCell[0]]
        g.board[oldCell[1]][oldCell[0]] = None
        g.isWhitesMove = not g.isWhitesMove
        g.history.append(game._FEN_())

        if game.board[oldCell[1]][oldCell[0]][1]=='P': g.fiftyCounter = 0
        else: g.fiftyCounter += 1

        if game.board[newCell[1]][newCell[0]]:
            if game.board[newCell[1]][newCell[0]][0]!=current_side:
                # piece acquired
                g.fiftyCounter = 0
                g.gameString += ' '+game.board[oldCell[1]][oldCell[0]][1]+game._notation_(oldCell)+'x'+game.board[newCell[1]][newCell[0]][1]+game._notation_(newCell)
                # TODO: add points for piece acquired
            else: # cannot move to own piece's square
                return game

        #en passant
        elif len(game.log)>0 and oldCell[1]==(3 if current_side=='w' else 4) and\
            newCell[1]==(game.log[-1][0][1]+game.log[-1][1][1])/2 and newCell[0]-oldCell[0]!=0 and\
            game.log[-1][0][0]==game.log[-1][1][0]==newCell[0]:
            g.fiftyCounter = 0
            g.gameString += ' '+game.board[oldCell[1]][oldCell[0]][1]+game._notation_(oldCell)+'x'+game._notation_(newCell)
            g.board[oldCell[1]][newCell[0]] = None
            # TODO: add game points for en passant
        
        #castling
        elif game.board[oldCell[1]][oldCell[0]][1]=='K' and not game.hasMoved(oldCell):
            if oldCell[0]-newCell[0] == 2: #queenside
                if not game.hasMoved((0, oldCell[1])):
                    g.board[oldCell[1]][3]=current_side+'R'
                    g.board[oldCell[1]][0]=None
                    g.gameString += ' '+'O-O-O'
            elif oldCell[0]-newCell[0] == -2: #kingside
                if not game.hasMoved((7, oldCell[1])):
                    g.board[oldCell[1]][5]=current_side+'R'
                    g.board[oldCell[1]][7]=None
                    g.gameString += ' '+'O-O'

        else: g.gameString += \
            (' ' if g.gameString else '')+game.board[oldCell[1]][oldCell[0]][1]+game._notation_(oldCell)+'-'+game._notation_(newCell)
        
        #pawn promotion
        if g.board[newCell[1]][newCell[0]][1]=='P' and newCell[1] in (0, 7):
            newPiece = 'Q' if testMove else (promoteTo if promoteTo else g.choosePiece())
            if newPiece in 'RNBQ':
                g.fiftyCounter = 0
                g.board[newCell[1]][newCell[0]] = current_side + newPiece
                g.gameString += '='+newPiece
            else: return game

        #game states
        g.log.append((oldCell, newCell))
        if not testMove: g.checkResult()
        
        return g

    def save(game):
        '''Saves the log of the game into a text file'''
        now = datetime.now()
        filename = 'chess_%d%02d%02d%02d%02d%02d.save.txt'%(now.year, now.month, now.day, now.hour, now.minute, now.second)
        # with open(filename, 'w') as file:
        #     for i, log in enumerate(game.log):
        #         file.write('%d. %s-%s\n'%(i+1, game._notation_(log[0]), game._notation_(log[1])))
        open(filename, 'w').write(game.gameString)
        return filename
    
    @staticmethod
    def loadFrom(filename, promotion=None):
        '''Loads a game state from an old .save version file.'''
        game = Chess(promotion=promotion)
        lines = open(filename, 'r').readlines()
        if len(lines) == 1:
            game = Chess(gameString=lines[0], promotion=promotion)
            print('game initialized', game)
            return game
        else:
            for line in lines:
                move = line.split()[1].split('-')
                game = game.makeMove(move[0], move[1])
        return game
