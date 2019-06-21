# -*- coding: utf-8 -*-

from numpy import zeros

class Chessboard(object):
    """ Class
    Describe Chessboard.
    """
    def __init__(self):
        self._chessboard_state = zeros([8, 8], dtype=int)
        for i in range(1, 7):
            self._chessboard_state[0][i] = State.BLACK
            self._chessboard_state[7][i] = State.BLACK
            self._chessboard_state[i][0] = State.WHITE
            self._chessboard_state[i][7] = State.WHITE
            
    def getCoordinateState(self, grid_x, grid_y):
        """
        Return the value of a specified position of the chessboard.
        """
        return self._chessboard_state[grid_y][grid_x]
    
    def getChessboard(self):
        """
        Return the chessboard.
        """
        return self._chessboard_state
    
    def getChessPosition(self, chess):
        """
        Return positions of a kind of chess.
        """
        chessboard = self.getChessboard()
        return [[i, j] for i in range(8) for j in range(8) if chessboard[i][j] == chess]
    
    def setCoordinateState(self, grid_x, grid_y, state):
        """
        Setup the value of a specified position of the chessboard. 
        """
        self._chessboard_state[grid_y][grid_x] = state
    
    def resetChessboard(self):
        """
        Reset the chessboard state.
        """
        for i in range(8):
            for j in range(8):
                self._chessboard_state[i][j] = State.EMPTY
        
        for i in range(1, 7):
            self._chessboard_state[0][i] = State.BLACK
            self._chessboard_state[7][i] = State.BLACK
            self._chessboard_state[i][0] = State.WHITE
            self._chessboard_state[i][7] = State.WHITE
        
class State(object):
    """ Class
    Describe chess states.
    """
    EMPTY = 0
    BLACK = 1
    WHITE = 2