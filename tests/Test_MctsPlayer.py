#!/usr/bin/python

import unittest
import copy
from MctsPlayer import MctsPlayer

class Test_Mcts_Player_kwArgs(unittest.TestCase):
    def test_kwArgs_default(self):
        p = MctsPlayer(1)
        self.assertFalse(p.simTime is None)
        p = MctsPlayer(1, time=60, depth=2000)
        self.assertEqual(60, p.simTime)
        self.assertEqual(2000, p.simDepth)

class TestGame1(object):
    '''
    A dummy game for test purpose
    (player=2, state='s1') is the initial state - player 1 moves to 's1' state
    player 2 has options to choose moves 'm1', 'm2', or 'm3' to reach state 's2', 's3', and 's4'
    respectively. The winner for the states are 's2':player1, 's3':2, 's4':1
    '''
    def __init__(self):
        self.current_player = 2
        self.state = 's1'
        self.winning_table = {'s1':None, 's2':1, 's3':2, 's4':1}
        self.state_transitions = {('s1', 'm1'):'s2', ('s1', 'm2'):'s3', ('s1', 'm3'):'s4'}
    
    def Copy(self):
        return copy.deepcopy(self)
    
    def GetCurrentPlayer(self):
        return self.current_player
    
    def GetWinner(self):
        return self.winning_table[self.state]
    
    def GetValidMoves(self):
        if self.state == 's1':
            return ['m1', 'm2', 'm3']
        return []
    
    def Move(self, playerId, move):
        if self.current_player != playerId:
            raise Exception('TestGame1 - invalid move')
        self.state = self.state_transitions[(self.state, move)]
        self.current_player = self.GetNextPlayer()
        
    def GetNextPlayer(self):
        if self.current_player == 1:
            return 2
        else:
            return 1
    
    def GetNextState(self, playerId, move):
        if playerId == self.current_player:
            return self.state_transitions[(self.state, move)]
        raise Exception ('TestGame1 - GetNextState invalid player')
           
    # static variable to keep moving state
    moveCount = 0
    @staticmethod
    def ControlledMove(validMoves):
        move = validMoves[TestGame1.moveCount % len(validMoves)] # returns the moves in turn
        TestGame1.moveCount += 1
        return move
        
            
        
class Test_Mcts_Player_Simulation_1(unittest.TestCase):
    def test_sim1(self):  
        game = TestGame1()
        player = MctsPlayer(2)
        
        copiedGame = copy.deepcopy(game)
        player.Simulate(copiedGame, TestGame1.ControlledMove)
        self.assertEqual(player.wins, {(2,'s2'):0})
        self.assertEqual(player.totals, {(2,'s2'):1})
        
        copiedGame = copy.deepcopy(game)
        player.Simulate(copiedGame, TestGame1.ControlledMove)
        self.assertEqual(2, TestGame1.moveCount)
        self.assertEqual(player.wins, {(2,'s2'):0,(2, 's3'):1})
        self.assertEqual(player.totals, {(2,'s2'):1,(2, 's3'):1})
        
        copiedGame = copy.deepcopy(game)
        player.Simulate(copiedGame, TestGame1.ControlledMove)
        self.assertEqual(3, TestGame1.moveCount)
        self.assertEqual(player.wins, {(2,'s2'):0,(2, 's3'):1,(2, 's4'):0})
        self.assertEqual(player.totals, {(2,'s2'):1,(2, 's3'):1,(2, 's4'):1})
        
        # Now all the child nodes have statistics
        copiedGame = copy.deepcopy(game)
        player.Simulate(copiedGame, TestGame1.ControlledMove)
        self.assertEqual(player.wins, {(2,'s2'):0,(2, 's3'):2,(2, 's4'):0})
        self.assertEqual(player.totals, {(2,'s2'):1,(2, 's3'):2,(2, 's4'):1})
    def test_GetMove(self):
        game = TestGame1()
        player = MctsPlayer(2, time=0.5)    # 0.5 second
        move = player.GetMove(game, game.GetValidMoves())
        self.assertEqual('m2', move)
        
        
        
if __name__ == '__main__':
    unittest.main()

