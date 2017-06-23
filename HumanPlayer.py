# HumanPlayer.py - Represents a human player

from Player import Player

import logging
import logging.config

logging.config.fileConfig('Logging.conf')
logger = logging.getLogger('connect4.player.HumanPlayer')

class HumanPlayer(Player):
    '''
    HumanPlayer: defines a human player
    '''
    def __init__(self):
        logger.debug('Human player instantiated')
    
    def __str__(self):
        return "Human"