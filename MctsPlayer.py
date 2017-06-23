# MctsPlayer.py - Represents an AI player using Monte Carlo Tree Search

from Player import Player

import logging
import logging.config

logging.config.fileConfig('Logging.conf')
logger = logging.getLogger('connect4.player.MctsPlayer')

class MctsPlayer(Player):
    '''
    MctsPlayer: defines a player using Monte Carlo Tree Search
    '''
    def __init__(self):
        logger.debug('Mcts player instantiated')
    
    def __str__(self):
        return "Mcts"