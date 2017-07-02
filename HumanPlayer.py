# HumanPlayer.py - Represents a human player

from Player import Player

import logging.config
from pyparsing import col

logging.config.fileConfig('Logging.conf')
logger = logging.getLogger('connect4.player.HumanPlayer')

class HumanPlayer(Player):
    '''
    HumanPlayer: defines a human player
    '''
    def __init__(self, playerId):
        super(HumanPlayer,self).__init__(playerId)
        logger.debug('Player {}: Human player instantiated'.format(playerId))
    
    def __str__(self):
        return '{} - Human'.format(self.GetID())

    def GetMove(self, game, validMoves):
        while True:
            try:
                col = eval(raw_input('{} Make a move (by entering the column number):'.format(self)))
                return col
            except Exception:
                pass

        