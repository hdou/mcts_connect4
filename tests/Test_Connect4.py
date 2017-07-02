#!/usr/bin/python

import unittest
from HumanPlayer import HumanPlayer
from Connect4 import Connect4

class Test_Connect4_Validations(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        p1 = HumanPlayer(1)
        p2 = HumanPlayer(2)
        self.game = Connect4(p1, p2)
    
    def test_IsValidPlayer(self):
        player = self.game.GetCurrentPlayer()
        self.assertTrue(self.game.IsCurrentPlayer(player))
        next_player = player % 2 + 1
        self.assertFalse(self.game.IsCurrentPlayer(next_player))
            
    def test_IsValidMove(self):
        self.assertEqual(False, self.game.IsValidMove(-1))
        self.assertFalse(self.game.IsValidMove(self.game.ColumnSize()))
        self.assertTrue(self.game.IsValidMove(self.game.ColumnSize()-1))
        # Column 2 is valid until it's filled up
        self.assertTrue(self.game.IsValidMove(2))
        self._FillColumn(2)
        self.assertFalse(self.game.IsValidMove(2))
    
    def _FillColumn(self, column):
        '''
        Fill a column
        '''
        current_player = self.game.GetCurrentPlayer()
        col = self.game.GetColumn(column)
        for _ in xrange(len(col), self.game.RowSize()):
            self.game.Move(current_player, column)
            current_player = current_player % 2 + 1 # alternate 1 and 2
    
    def test_ValidateBoard(self):
        board = [[1]]
        with self.assertRaises(Exception) as context:
            self.game.ValidateBoard(board)
        self.assertTrue('Invalid board size' in str(context.exception))
        
        board = [[],[],[1,2],[1,2,1,2,1,2,1],[],[],[]]
        with self.assertRaises(Exception) as context:
            self.game.ValidateBoard(board)
        self.assertTrue('Invalid board size' in str(context.exception))
        
        board = [[],[],[1,2],[1,2,1,2,1,2],[' '],[],[]]
        with self.assertRaises(Exception) as context:
            self.game.ValidateBoard(board)
        self.assertTrue('Invalid value' in str(context.exception))

class Test_Connect4_Algorithm(unittest.TestCase):
    '''
    Test more complex algorithms, such as GetRow, GetDiag, GetAntiDiag, etc
    '''
    def setUp(self):
        p1 = HumanPlayer(1)
        p2 = HumanPlayer(2)
        board = [[1,2,2,1,2], [2,1,2,1], [1,2,1,2,1,2], [2,1,2,1,2,1], [2,2,1], [1,1,2,1], [2,1,2,1]]
        #     2 1
        # 2   1 2
        # 1 1 2 1   1 1
        # 2 2 1 2 1 2 2
        # 2 1 2 1 2 1 1
        # 1 2 1 2 2 1 2
        self.game = Connect4(p1, p2, board)
    def test_GetValue(self):
        v = self.game.GetValue(5, 0)
        self.assertEqual(' ', v)
        v = self.game.GetValue(1, 2)
        self.assertEqual(2, v)
        v = self.game.GetValue(0, 5)
        self.assertEqual(v, 1)
        v = self.game.GetValue(3, 4)
        self.assertEqual(v, ' ')
    def test_GetRow(self):
        row = self.game.GetRow(0)
        self.assertEqual([1,2,1,2,2,1,2], row)
        row = self.game.GetRow(1)
        self.assertEqual([2,1,2,1,2,1,1], row)
        row = self.game.GetRow(2)
        self.assertEqual([2,2,1,2,1,2,2], row)
        row = self.game.GetRow(3)
        self.assertEqual([1,1,2,1,' ',1,1], row)
        row = self.game.GetRow(4)
        self.assertEqual([2,' ',1,2,' ',' ',' '], row)
        row = self.game.GetRow(5)
        self.assertEqual([' ',' ',2,1,' ',' ',' '], row)
    def test_GetDiagonal(self):
        #     2 1
        # 2   1 2
        # 1 1 2 1   1 1
        # 2 2 1 2 1 2 2
        # 2 1 2 1 2 1 1
        # 1 2 1 2 2 1 2
        self.assertRaises(Exception, self.game.GetDiag, -6)
        self.assertRaises(Exception, self.game.GetDiag, 7)
        diag = self.game.GetDiag(-5)
        self.assertEqual([' '], diag)
        diag = self.game.GetDiag(-4)
        self.assertEqual([2,' '], diag)
        diag = self.game.GetDiag(-3)
        self.assertEqual([1,' ',2], diag)
        diag = self.game.GetDiag(-2)
        self.assertEqual([2,1,1,1], diag)
        diag = self.game.GetDiag(-1)
        self.assertEqual([2,2,2,2,' '], diag)
        diag = self.game.GetDiag(0)
        self.assertEqual([1,1,1,1,' ',' '], diag)
        diag = self.game.GetDiag(1)
        self.assertEqual([2,2,2,' ',' ',' '], diag)
        diag = self.game.GetDiag(2)
        self.assertEqual([1,1,1,1,' '], diag)
        diag = self.game.GetDiag(3)
        self.assertEqual([2,2,2,1], diag)
        diag = self.game.GetDiag(4)
        self.assertEqual([2,1,2], diag)
        diag = self.game.GetDiag(5)
        self.assertEqual([1,1], diag)
        diag = self.game.GetDiag(6)
        self.assertEqual([2], diag)
    def test_GetAntiDiag(self):
        #     2 1
        # 2   1 2
        # 1 1 2 1   1 1
        # 2 2 1 2 1 2 2
        # 2 1 2 1 2 1 1
        # 1 2 1 2 2 1 2
        self.assertRaises(Exception, self.game.GetDiag, -6)
        self.assertRaises(Exception, self.game.GetDiag, 7)
        adiag = self.game.GetAntiDiag(-5)
        self.assertEqual([1], adiag)
        adiag = self.game.GetAntiDiag(-4)
        self.assertEqual([2,2], adiag)
        adiag = self.game.GetAntiDiag(-3)
        self.assertEqual([2,1,1], adiag)
        adiag = self.game.GetAntiDiag(-2)
        self.assertEqual([1,2,2,2], adiag)
        adiag = self.game.GetAntiDiag(-1)
        self.assertEqual([2,1,1,1,2], adiag)
        adiag = self.game.GetAntiDiag(0)
        self.assertEqual([' ',' ',2,2,2,1], adiag)
        adiag = self.game.GetAntiDiag(1)
        self.assertEqual([' ',1,1,1,1,2], adiag)
        adiag = self.game.GetAntiDiag(2)
        self.assertEqual([2,2,' ',2,1], adiag)
        adiag = self.game.GetAntiDiag(3)
        self.assertEqual([1,' ',1,2], adiag)
        adiag = self.game.GetAntiDiag(4)
        self.assertEqual([' ',' ',1], adiag)
        adiag = self.game.GetAntiDiag(5)
        self.assertEqual([' ',' '], adiag)
        adiag = self.game.GetAntiDiag(6)
        self.assertEqual([' '], adiag)
    def test_GetWinnerInLine(self):
        v = [1]
        self.assertEqual(None, self.game.GetWinnerInLine(v))
        v = [2,1,1,1,2]
        self.assertEqual(None, self.game.GetWinnerInLine(v))
        v = [' ',' ',' ',' ',1]
        self.assertEqual(None, self.game.GetWinnerInLine(v))
        v = [' ',' ',2,2,2,2]
        self.assertEqual(2, self.game.GetWinnerInLine(v))
        v = [' ',1,1,1,1,2,' ']
        self.assertEqual(1, self.game.GetWinnerInLine(v))

class Test_Connect4_GetWinner(unittest.TestCase):
    def test_GetWinner_None_1(self):
        p1 = HumanPlayer(1)
        p2 = HumanPlayer(2)
        board = [[], [2,1], [1,2,1], [2,2,1], [], [], []]
        #       
        #      
        #     
        #     1 1       
        #   1 2 2       
        #   2 1 2       
        game = Connect4(p1, p2, board)
        w = game.GetWinner()
        self.assertEqual(None, w)        
    def test_GetWinner_None_2(self):
        p1 = HumanPlayer(1)
        p2 = HumanPlayer(2)
        board = [[], [2,1,2,1], [1,2,2,2,1], [2,1,2,1,2,1], [], [], [1,1,2]]
        #       1
        #     1 2
        #   1 2 1
        #   2 2 2       2
        #   1 2 1       1
        #   2 1 2       1
        game = Connect4(p1, p2, board)
        w = game.GetWinner()
        self.assertEqual(None, w)        
    def test_GetWinner_Column(self):
        p1 = HumanPlayer(1)
        p2 = HumanPlayer(2)
        board = [[], [2,1,2,1], [1,2,2,2,2], [2,1,2,1,2,1], [], [], [1,1,2]]
        #       1
        #     2 2
        #   1 2 1
        #   2 2 2       2
        #   1 2 1       1
        #   2 1 2       1
        game = Connect4(p1, p2, board)
        w = game.GetWinner()
        self.assertEqual(2, w)
    def test_GetWinner_Row(self):
        p1 = HumanPlayer(1)
        p2 = HumanPlayer(2)
        board = [[], [2,1,2,1], [1,2,2,2,1], [2,1,2,1,2,1], [1,1,2], [], [2]]
        #       1
        #     1 2
        #   1 2 1
        #   2 2 2 2    
        #   1 2 1 1
        #   2 1 2 1    2
        game = Connect4(p1, p2, board)
        w = game.GetWinner()
        self.assertEqual(2, w)
    def test_GetWinner_Diag(self):
        p1 = HumanPlayer(1)
        p2 = HumanPlayer(2)
        board = [[], [2,1,2,1], [1,2,2,2,1], [2,1,2,1,2,1], [1,1,1,2], [], [2]]
        #       1
        #     1 2
        #   1 2 1 2
        #   2 2 2 1    
        #   1 2 1 1
        #   2 1 2 1    2
        game = Connect4(p1, p2, board)
        w = game.GetWinner()
        self.assertEqual(2, w)
    def test_GetWinner_AntiDiag(self):
        p1 = HumanPlayer(1)
        p2 = HumanPlayer(2)
        board = [[], [2,1,2,1], [1,2,2,2,1], [2,1,2,1,2,1], [1,1,1], [2,1], [2]]
        #       1
        #     1 2
        #   1 2 1
        #   2 2 2 1    
        #   1 2 1 1 1
        #   2 1 2 1 2 2
        game = Connect4(p1, p2, board)
        w = game.GetWinner()
        self.assertEqual(1, w)

class Test_Connect4_GetValidMoves(unittest.TestCase):
    def test_GetValidMoves_1(self):
        p1 = HumanPlayer(1)
        p2 = HumanPlayer(2)
        board = [[1,2,2,1,2,1], [2,1,2,1], [1,2,2,2,1], [2,1,2,1,2,1], [1,1,1], [2,1], [2]]
        # 1     1
        # 2   1 2
        # 1 1 2 1
        # 2 2 2 2 1    
        # 2 1 2 1 1 1
        # 1 2 1 2 1 2 2
        game = Connect4(p1, p2, board)
        ms = game.GetValidMoves()
        self.assertEqual([1,2,4,5,6], ms)
    def test_GetValidMoves_2(self):
        p1 = HumanPlayer(1)
        p2 = HumanPlayer(2)
        board = [[1,2,2,1,2,1], [1,2,2,1,2,1], [1,2,2,1,2,1], [1,2,2,1,2,1], [1,2,2,1,2,1], [1,2,2,1,2,1], [1,2,2,1,2,1]]
        game = Connect4(p1, p2, board)
        ms = game.GetValidMoves()
        self.assertEqual([], ms)

class Test_Connect4_GetLastMove(unittest.TestCase):
    def test_GetLastMove(self):
        p1 = HumanPlayer(1)
        p2 = HumanPlayer(2)
        game = Connect4(p1, p2)
        self.assertEqual(None, game.GetLastMove())
        game.Move(1, 2)
        self.assertEqual((0,2), game.GetLastMove())
        
class Test_Connect4_GetNextState(unittest.TestCase):
    def test_GetNextState(self):
        p1 = HumanPlayer(1)
        p2 = HumanPlayer(2)
        board = [[1,2,2,1,2,1], [2,1,2,1], [1,2,2,2,1], [2,1,2,1,2,1], [1,1,1], [2,1], [2]]
        game = Connect4(p1, p2, board)
        state = game.GetNextState(player=1, column=2)
        expectedState = ((1,2,2,1,2,1), (2,1,2,1), (1,2,2,2,1,1), (2,1,2,1,2,1), (1,1,1), (2,1), (2,))
        self.assertEqual(expectedState, state)
        # Make sure the original game hasn't been changed
        self.assertEqual(board, game.board)
        self.assertEqual(1, game.GetCurrentPlayer())
            
if __name__ == '__main__':
    unittest.main()
    