# HumanPlayer.py - Represents a human player

from Player import Player

import logging.config

logging.config.fileConfig('Logging.conf')
logger = logging.getLogger('connect4.player.HumanPlayer')

class HumanPlayer(Player):
    '''
    HumanPlayer: defines a human player
    '''
    def __init__(self, id):
        super(HumanPlayer,self).__init__(id)
        logger.debug('Player {}: Human player instantiated'.format(id))
    
    def __str__(self):
        return '{} - Human'.format(self.GetID())
