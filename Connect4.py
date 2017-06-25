#!/usr/bin/python

# Connect4.py - defines the game logic

import argparse
from HumanPlayer import HumanPlayer
from MctsPlayer import MctsPlayer
import logging.config
import copy
from TextPresentor import TextPresenter

logging.config.fileConfig('Logging.conf')
logger = logging.getLogger('connect4.game')


class Connect4(object):
    '''
    Connect 4 - represent a Connect 4 game.
    
    Two players are identified as 1 and 2
    
    Board layout is defined as:
            Column 0, Column 1, ... Column N
    Row M
    ...
    Row 1
    Row 0
    
    Diagonals and antidiagonals are defined as follows (see https://en.wikipedia.org/wiki/Main_diagonal):
    Diag[-M] = [(rM, c0)]
    ...
    Diag[-1] = [(r1, c0), (r2, c1), ..., (rx, cx)] where x = min(M-1, N)
    Diag[0]  = [(r0, c0), (r1, c1), ..., (rx, cx)] where x = min(M, N)
    Diag[1]  = [(r0, c1), (r1, c2), ..., (rx, cx)] where x = min(M, N-1)
    ...
    Diag[N]  = [(r0, cN)]
    
    AntiDiag[-M] = [(r0, c0)]
    ...
    AntiDiag[-1] = [(rM-1, c0), (rM-2, c1), ..., (rx, cx)] where x = min(M-1, N)
    AntiDiag[0]  = [(rM, c0), (rM-1, c1), ..., (rx, cx)]   where x = min(M, N)
    AntiDiag[1]  = [(rM, c1), r(M-1, c2), ..., (rx, cx)]   where x = min(M, N-1)
    AntiDiag[N]  = [(r0, cN)]
    
    GetColumn(column) returns a list of player IDs who has taken the location, up to the last row occupied.
    For example [1,2,2,1]
    GetRow(row) returns the list represeting the entire row. If a location is taken by player ID=x, the 
    corresponding element will have value x. If a location is not occupied, the corresponding element will
    have character space, or ' '.
    GetDiag(index) and GetAntiDiag(index) are similar to GetRow.
    '''
    def __init__(self, p1, p2, board=None, current_player=1, presenter=None):
        self.p1 = p1
        self.p2 = p2
        
        # size of the board
        self.size = [6,7]   # 6 rows, 7 columns
        print('New game - players: {}, {}'.format(p1, p2))
        
        if board is None:
            # initialize the board [[],[],...[]], each element list represents a column
            self.board = [[] for _ in xrange(self.ColumnSize())]
        else:
            # make a copy of the board given
            self.ValidateBoard(board)
            self.board = copy.deepcopy(board)
        
        # player 1 expects to make a move
        self.current_player = current_player
        
        # Default to a text presenter
        if presenter is None:
            self.presenter = TextPresenter()
        else:
            self.presenter = presenter
        
        # remember the last move
        self.lastMove = None
            
    def RowSize(self):
        return self.size[0]
    def ColumnSize(self):
        return self.size[1]
    def DiagRange(self):
        return xrange(-self.RowSize()+1, self.ColumnSize())
    
    def Play(self):
        while True:
            if self.presenter is not None:
                self.presenter.Present(self)
                
            winner = self.GetWinner()
            if winner is not None:
                player = self.GetPlayerFromId(winner)
                print "Game over. {} wins".format(player)
                return
            if not self.HasSpaceToMove():
                print "Game over. It's a tie"
                return
            player = self.GetPlayerFromId(self.current_player)
        
            while True:
                move = player.GetMove(self, self.GetValidMoves())
                try:
                    self.Move(self.current_player, move)
                    break
                except Exception:
                    print 'Invalid move {}'.format(move)
                            
    def GetPlayerFromId(self, playerId):
        if not self.IsValidPlayer(playerId):
            raise Exception('Invalid player ID: {}'.format(playerId))
        if playerId == 1:
            return self.p1
        return self.p2
    
    def GetValidMoves(self):
        validMoves = []
        for i in xrange(self.ColumnSize()):
            col = self.GetColumn(i)
            if len(col) < self.RowSize():
                validMoves.append(i)
        return validMoves

    def Move(self, player, column):
        '''
        Move: player makes a move
        player (1 or 2) puts a piece in column (0 to 6 inclusive)
        '''
        logger.info('Move: Player %s, Column %s', player, column)
        logger.debug('Board: %s', self.board)
        if not self.IsCurrentPlayer(player):
            raise Exception ('Not player', player, '\'s turn')
        if not self.IsValidMove(column):
            raise Exception ('Invalid move', column, self.board)
        col = self.GetColumn(column)
        col.append(player)
        logger.debug("Board: {}".format(self.board))
        
        self.lastMove = column
        self.current_player = self.GetNextPlayer()        
    
    def IsValidMove(self, column):
        '''
        IsValidMove: check whether the move is valid (column is 0-based)
        Returns True if so, or False otherwise
        '''
        if column >= self.ColumnSize() or column < 0:
            return False
        col = self.GetColumn(column)
        return len(col) < self.RowSize()
    
    def GetLastMove(self):
        '''
        If there are moves, return the last move in (row,column)
        '''
        if self.lastMove is not None:
            col = self.GetColumn(self.lastMove)
            for i in reversed(xrange(len(col))):
                if self.IsValidPlayer(col[i]):
                    return (i, self.lastMove)
        return None
                
            
    def GetValue(self, row, col):
        '''
        Return value at location (row, col). If a player has taken it, returns the ID of the player;
        Otherwise returns ' '
        '''
        column = self.GetColumn(col)
        if row < len(column):
            return column[row]
        return ' '
            
    def GetColumn(self, index):
        if index >= self.ColumnSize() or index < 0:
            raise Exception('Invalid column', index)
        return self.board[index]
    
    def GetRow(self, index):
        if index >= self.RowSize() or index < 0:
            raise Exception('Invalid row', index)
        row = []
        for i in xrange(self.ColumnSize()):
            row.append(self.GetValue(index, i))
        return row
    
    def GetDiag(self, index):
#     Diag[-M] = [(rM, c0)]
#     ...
#     Diag[-1] = [(r1, c0), (r2, c1), ..., (rx, cx-1)] where x = min(M-1, N)
#     Diag[0]  = [(r0, c0), (r1, c1), ..., (rx, cx)] where x = min(M, N)
#     Diag[1]  = [(r0, c1), (r1, c2), ..., (rx, cx+1)] where x = min(M, N-1)
#     ...
#     Diag[N]  = [(r0, cN)]
        if index not in self.DiagRange():
            raise Exception('Invalid diagonal', index)
        M = self.RowSize() - 1
        N = self.ColumnSize() - 1
        if index < 0:
            r = -index
            c = 0
            nElem = min(M+index, N) + 1
        else:
            r = 0
            c = index
            nElem = min(M, N-index) + 1
        diag = []
        for _ in xrange(nElem):
            diag.append(self.GetValue(r,c))
            r = r+1
            c = c+1
        return diag
    
    def GetAntiDiag(self,index):
        if index not in self.DiagRange():
            raise Exception('Invalid antidiagonal {}. Expect {}'.format(index, self.DiagRange()))
#     AntiDiag[-M] = [(r0, c0)]
#     ...
#     AntiDiag[-1] = [(rM-1, c0), (rM-2, c1), ..., (rx, cx)] where x = min(M-1, N)
#     AntiDiag[0]  = [(rM, c0), (rM-1, c1), ..., (rx, cx)]   where x = min(M, N)
#     AntiDiag[1]  = [(rM, c1), r(M-1, c2), ..., (rx, cx)]   where x = min(M, N-1)
#     AntiDiag[N]  = [(rM, cN)]
        M = self.RowSize()-1
        N = self.ColumnSize()-1
        if index < 0:
            r = M+index
            c = 0
            nElem = min(M+index, N) + 1
        else:
            r = M
            c = index
            nElem = min(M, N-index) + 1
        adiag = []
        for _ in xrange(nElem):
            adiag.append(self.GetValue(r,c))
            r = r - 1
            c = c + 1
        return adiag
        
    def IsCurrentPlayer(self, player):
        return player == self.current_player
    
    def IsValidPlayer(self, player):
        return player == 1 or player == 2
    
    def GetCurrentPlayer(self):
        return self.current_player;
    
    def GetNextPlayer(self):
        return self.current_player % 2 + 1 # alternate 1 and 2
    
    def ValidateBoard(self, board):
        if len(board) != self.ColumnSize():
            raise Exception('Invalid board size: expect {} columns, got {}'.format(self.ColumnSize(), len(board)))
        for i in xrange(len(board)):
            col = board[i]
            if len(col) > self.RowSize():
                raise Exception('Invalid board size. Column {} has more than {} elements'.format(i, self.RowSize()))
            for j in xrange(len(col)):
                if col[j] != 1 and col[j] != 2:
                    raise Exception('Invalid value at ({},{}): {}. Expect 1 or 2'.format(i,j,col[j]))
                
    def GetNConscecutivesToWin(self):
        return 4
        
    def GetWinnerInLine(self, valueList):
        '''
        Check whether the list of values indicate a winner (4 conscecutive values).
        If so, returns it (if both players have 4 conscecutives, the first one detected is considered 
        the winner). Otherwise returns None 
        '''
        winner = None
        if len(valueList) >= self.GetNConscecutivesToWin():
            potential_winner = None
            conscecutives = 0
            for i in xrange(len(valueList)):
                v = valueList[i]
                if potential_winner is None:
                    if v != 1 and v != 2:
                        continue
                    else:
                        potential_winner = v
                        conscecutives = 1
                elif potential_winner == v:
                    conscecutives = conscecutives + 1
                elif v != 1 and v != 2:
                    potential_winner = None
                    conscecutives = 0
                else:
                    potential_winner = v
                    conscecutives = 1
                    
                if conscecutives == 4:
                    break
                
            if potential_winner is not None and conscecutives >= 4:
                winner = potential_winner

        return winner
        
    def GetWinner(self):
        '''
        Get the winner of the game, if there is one, otherwise None.
        '''
        for i in xrange(self.ColumnSize()):
            line = self.GetColumn(i)
            winner = self.GetWinnerInLine(line)
            if winner is not None:
                return winner
        for i in xrange(self.RowSize()):
            line = self.GetRow(i)
            winner = self.GetWinnerInLine(line)
            if winner is not None:
                return winner
        for i in self.DiagRange():
            line = self.GetDiag(i)
            winner = self.GetWinnerInLine(line)
            if winner is not None:
                return winner
        for i in self.DiagRange():  # same range as diagonal lines
            line = self.GetAntiDiag(i)
            winner = self.GetWinnerInLine(line)
            if winner is not None:
                return winner
    
    def HasSpaceToMove(self):
        for i in xrange(self.ColumnSize()):
            col = self.GetColumn(i)
            if len(col) < self.RowSize():
                return True
        return False    
                
def MakePlayer(player, playerId):
    '''
    Instantiate a Player based on the input string:
    h or human: HumanPlayer
    m or mcts:  MctsPlayer
    Raise exception otherwise
    '''
    if player == 'h' or player == 'human':
        return HumanPlayer(playerId)
    elif player == 'm' or player == 'mcts':
        return MctsPlayer(playerId)
    raise Exception("Unknown Player type", player)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Experiment Monte Carlo tree search with a connect-4 game.')
    
#     parser.add_argument('--ps', '--players', choices=['hm', 'mh'], default='hm',
#                         help = 'Specify the players. ' \
#                         + 'hm: player1=human, player2=mcts. ' \
#                         + 'mh: player1=mcts, player2=human' \
#                         + '(default=%(default)s)')

    parser.add_argument('--p1', '--player1', choices=['h', 'human', 'm', 'mcts'], default='human',
                        help = 'Specify Player 1. h=human or m=mcts (default=%(default)s)')
    parser.add_argument('--p2', '--player2', choices=['m', 'mcts', 'h', 'human'], default='mcts',
                        help = 'Specify Player 2. m=mcts or h=human (default=%(default)s)')
    
    
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    
    player1 = MakePlayer(args.p1, 1)
    player2 = MakePlayer(args.p2, 2)
    
    game = Connect4(player1, player2)
    
    game.Play()
    
