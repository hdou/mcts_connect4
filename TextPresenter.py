from Presenter import Presenter

class TextPresenter(Presenter):
    '''
    class TextPresenter: present the Connect4 board with text
    '''
    def Present(self, game):
        colSize = game.ColumnSize()
        rowSize = game.RowSize()
        
        # first line
        print ' ',
        for i in xrange(colSize):
            print ' ', i,
        print
        
        lastMove = game.GetLastMove()
        
        for i in reversed(xrange(rowSize)):
            print i,
            row = game.GetRow(i)
            for j in xrange(len(row)):
                s = self._GetSymbol(row[j])
                if lastMove is not None and (i, j) == lastMove:
                    print '>',s,
                else:
                    print ' ', s,
            print
    
    def _GetSymbol(self, playerId):
        if playerId == 1:
            return 'x'
        elif playerId == 2:
            return 'o'
        elif playerId == ' ':
            return playerId
        else:
            raise Exception('Unknown player {}'.format(playerId))
        
        