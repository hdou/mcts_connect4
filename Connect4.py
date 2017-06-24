#!/usr/bin/python

# Connect4.py - defines the game logic

import argparse
from HumanPlayer import HumanPlayer
from MctsPlayer import MctsPlayer
import logging.config

logging.config.fileConfig('Logging.conf')
logger = logging.getLogger('connect4.game')


class Connect4(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        logger.info('New game - player 1: %s, player 2: %s', p1, p2)



def MakePlayer(player):
    '''
    Instantiate a Player based on the input string:
    h or human: HumanPlayer
    m or mcts:  MctsPlayer
    Raise exception otherwise
    '''
    if player == 'h' or player == 'human':
        return HumanPlayer()
    elif player == 'm' or player == 'mcts':
        return MctsPlayer()
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
    
    player1 = MakePlayer(args.p1)
    player2 = MakePlayer(args.p2)
    
    game = Connect4(player1, player2)
    
