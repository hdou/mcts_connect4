# MctsPlayer.py - Represents an AI player using Monte Carlo Tree Search
from __future__ import division     # otherwise 5/2 = 2

from Player import Player

import logging.config
import time
from math import log
from math import sqrt
from math import ceil
from random import choice
import copy
import sys

logging.config.fileConfig('Logging.conf')
logger = logging.getLogger('connect4.player.MctsPlayer')

class MctsPlayer(Player):
    '''
    MctsPlayer: defines a player using Monte Carlo Tree Search
    '''
    def __init__(self, playerId, **kwargs):
        super(MctsPlayer,self).__init__(playerId)
        logger.debug('Player {}: Mcts player instantiated'.format(playerId))
        
        # parameters
        self.simTime = kwargs.get('time', 30)       # simulation time, in seconds
        self.simDepth = kwargs.get('depth', 100)    # maximum depth to simulate
        
        # Dictionaries from (player, board_state) to winning count and visited count respectively, where
        # player: the id of the player whose move results in the board state
        # board_state: the state of the board
        # wins: the number of times the player wins when enter into this state
        # totals: the number of times the (player, board_state) has been simulated 
        self.wins = {}
        self.totals = {}
        self.loses = {}
        self.draws = {}
        
        self.depth = 0
    
    def __str__(self):
        return '{} - Mcts({})'.format(self.GetID(), self.simTime)
    
    def GetMove(self, game, validMoves):
        '''
        Returns the move computed with MCTS algorithm
        '''
        if validMoves is None or len(validMoves) == 0:
            return
        
        if len(validMoves) == 1:
            return validMoves[0]
        
        simulationCount = 0
        beginTime = time.time()
        currTime = time.time()
        logTime = currTime
        sys.stdout.write('{} move - time left ({})'.format(self, self.simTime))
        sys.stdout.flush()
        nextFivesMark = int(ceil((self.simTime - 5)/5)*5)
        while currTime - beginTime < self.simTime:
            # Make a copy of the game
            #copiedGame = copy.deepcopy(game)
            copiedGame = game.Copy()
            self.Simulate(copiedGame)
            simulationCount += 1
            if currTime - logTime >= 1:
                timeLeft = self.simTime - (currTime - beginTime)
                if timeLeft <= nextFivesMark:
                    sys.stdout.write('({})'.format(str(nextFivesMark)))
                    nextFivesMark -= 5
                else:
                    sys.stdout.write('.')
                sys.stdout.flush()
                logTime = currTime
            currTime = time.time()
        print
                
        
        logging.info('{} simulated {} times in {} seconds'.format(self, simulationCount, self.simTime))
        
        myId = self.GetID()
        movesStates = [(move, game.GetNextState(myId, move)) for move in validMoves]

                
        # Pick the move with the highest winning percentage
        winPercentage, move = max((self.wins.get((myId, state), 0)/self.totals.get((myId,state), 1), mv) for mv, state in movesStates)
        if winPercentage < 0.2:
            winDrawPercentage, move2 = max(((self.wins.get((myId, state), 0)+self.draws.get((myId, state), 0))/self.totals.get((myId,state), 1), mv) for mv, state in movesStates)
            if move2 != move:
                move = move2
                print 'Winning percentage too low. Use win+draw% - move {} - {:.1f}%'.format(move, winDrawPercentage*100)
        
        # Print out the winning percentages
        for x in sorted(((
            100 * self.wins.get((myId, state), 0)/self.totals.get((myId, state), 1),
            self.wins.get((myId, state), 0),
            self.totals.get((myId, state), 0),
            mv,
            100 * self.draws.get((myId, state), 0)/self.totals.get((myId, state), 1),
            self.draws.get((myId, state), 0),
            100 * self.loses.get((myId, state), 0)/self.totals.get((myId, state), 1),
            self.loses.get((myId, state), 0)            
            ) for mv, state in movesStates), reverse=True):
            print '{3} : w: {0:.1f}% ({1}/{2}), d: {4:.1f}% ({5}/{2}), l: {6:.1f}% ({7}/{2})'.format(*x)            
    
        print 'Max depth = ', self.depth
        
        # clear stored states
        self.totals = {}
        self.wins = {}
        
        return move
    
    
    def Simulate(self, game, randomFunc=choice):
        '''
        Simulate the game
        If randomFunc is provided, it will be called with randomFunc(validMoves) when random moves are desired
        '''
        totals = self.totals
        wins = self.wins
        loses = self.loses
        draws = self.draws
        
        depth = 0
        winner = game.GetWinner()
        playerId = game.GetCurrentPlayer()
        validMoves = game.GetValidMoves()
        
        visitedPlayersStates = set()
        expandTree = True
        
        while winner is None and len(validMoves)>0 and depth < self.simDepth:
            movesStates = [(move, game.GetNextState(playerId, move)) for move in validMoves]
            
            if all(totals.get((playerId, state)) for _, state in movesStates):
                # all child nodes have statistics, use UCT
                N = sum(totals.get((playerId, state)) for _, state in movesStates)
                moveScore = max((wins.get((playerId, state))/totals.get((playerId, state)) + sqrt(2*log(N)/totals.get((playerId, state))), move)
                               for move, state in movesStates)
                move = moveScore[1]
            else:
                move = randomFunc(validMoves)
            
            game.Move(playerId, move)
            
            # Add the (player, state) into visited nodes
            moveState = [item for item in movesStates if item[0]==move]    # find the state corresponding to the move 
            if len(moveState) != 1:
                raise Exception('Duplicated move {} {} times: {}'.format(move, len(moveState), validMoves))
            # first index [0]: first (the only) element
            # second index [1]: the state
            state = moveState[0][1] 
            visitedPlayersStates.add((playerId, state))
            
            # Add the (player, state) into the statistics if expandTree is false.
            # Only add the first new node
            if expandTree:
                if (playerId, state) not in totals:
                    expandTree = False
                    totals[(playerId, state)] = 0
                    wins[(playerId, state)] = 0
                    draws[(playerId, state)] = 0
                    loses[(playerId, state)] = 0

            playerId = game.GetCurrentPlayer()
            winner = game.GetWinner()
            validMoves = game.GetValidMoves()
            depth += 1
        
        for (p, s) in visitedPlayersStates:
            if (p, s) in totals:
                totals[(p, s)] += 1
                if winner is None:
                    draws[(p,s)] += 1
                elif p == winner:
                    wins[(p,s)] += 1
                else:
                    loses[(p,s)] += 1
                        
                        
        if depth >= self.depth:
            self.depth = depth
                    
