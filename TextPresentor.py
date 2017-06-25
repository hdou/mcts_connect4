from Presenter import Presenter

class TextPresenter(Presenter):
    '''
    class TextPresenter: present the Connect4 board with text
    '''
    def Present(self, game):
        colSize = game.ColumnSize()
        rowSize = game.RowSize()
        
        # first line
        print '   ',
        for i in xrange(colSize):
            print i,
            if i < (colSize-1):
                print ' ',
        print '\n'
        
        for i in reversed(xrange(rowSize)):
            print i, ' ',
            row = game.GetRow(i)
            for j in xrange(len(row)):
                s = self._GetSymbol(row[j])
                print s,
                if j<(len(row)-1):
                    print ' ',
            print '\n'
    
    def _GetSymbol(self, playerId):
        if playerId == 1:
            return 'x'
        elif playerId == 2:
            return 'o'
        elif playerId == ' ':
            return playerId
        else:
            raise Exception('Unknown player {}'.format(playerId))
        
        