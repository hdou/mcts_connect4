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
        self.assertTrue(self.game.IsValidPlayer(player))
        next_player = player % 2 + 1
        self.assertFalse(self.game.IsValidPlayer(next_player))
            
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
    def test_GetWinner(self):
        v = [1]
        self.assertEqual(None, self.game.GetWinner(v))
        v = [2,1,1,1,2]
        self.assertEqual(None, self.game.GetWinner(v))
        v = [' ',' ',' ',' ',1]
        self.assertEqual(None, self.game.GetWinner(v))
        v = [' ',' ',2,2,2,2]
        self.assertEqual(2, self.game.GetWinner(v))
        v = [' ',1,1,1,1,2,' ']
        self.assertEqual(1, self.game.GetWinner(v))

if __name__ == '__main__':
    unittest.main()
    