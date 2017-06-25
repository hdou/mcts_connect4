class Player(object):
    '''
    player: defines the interface of a player.
    
    Each player is identified by an id. Valid IDs are 1 and 2 for this game.
    Each player can also optionally have a name
    '''
    def __init__(self, id):
        self.id = id
    
    def GetID(self):
        return self.id
    
    def GetMove(self, game, validMove):
        raise NotImplemented('Concrete class must implement this method')
    