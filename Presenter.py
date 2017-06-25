class Presenter(object):
    '''
    class Presenter - base class for those that presents a Connect4 board.
    The board is as described in the Connect4 class
    '''
    def Present(self, game):
        '''
        Present the board to the user.
        game: a Connect4 game ongoing
        '''
        raise NotImplemented('Concrete class must implement the method')