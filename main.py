# -*- coding: utf-8 -*-

from copy import deepcopy
from numpy import zeros
from PyQt5 import QtCore, QtWidgets
from src.models.chessboard import State
from src.models.get_available_movement import getAvailableMovement
from src.models.eight_connectivity_two_pass import eightConnectivityTwoPass
from src.models.monte_carlo_tree_search import monteCarloTreeSearch
from src.views.main_window import MainWindow
from sys import argv
from time import time

class Controller(QtWidgets.QMainWindow):
    """ Class
    Controller class.
    """
    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)
        self.main_window = MainWindow()
        self.main_window.setupUi(self)

    def setAvailableMovement(self, pos_x, pos_y):
        """ Slot function
        Setup `self._available_movement`.
        """
        available_movement = getAvailableMovement(pos_x, pos_y, State.BLACK, \
                                                  self.main_window.chessboard.getChessboard())
        self.main_window.setAvailableMovement(available_movement)
    
    def aiTurnMonteCarloTreeSearch(self):
        """ Slot function
        Monte Carlo Tree Search (MCTS) function.
        """
        chessboard = deepcopy(self.main_window.chessboard.getChessboard())
        time_start = time()
        from_chess, to_chess = monteCarloTreeSearch(chessboard)
        time_end = time()
        
        self.main_window.chessboard.setCoordinateState(from_chess[1], from_chess[0], State.EMPTY)
        self.main_window.clearChess(from_chess[1], from_chess[0])
        self.main_window.chessboard.setCoordinateState(to_chess[1], to_chess[0], State.WHITE)
        self.main_window.drawChess(to_chess[1], to_chess[0], State.WHITE)

        self.main_window.lasting_time = round(time_end - time_start, 3)
        self.main_window.ai_move = [from_chess, to_chess]
        
        result = self.checkGameEnd()
        if result != State.EMPTY:
            self.main_window.gameEnd(result)
        
        self.main_window.check_exchange_turn = True
        
    def checkGameEnd(self):
        """
        Check if this game ends.
        """
        # White chess won.
        if len(self.main_window.chessboard.getChessPosition(State.BLACK)) == 1:
            return State.WHITE
        # Black chess won.
        elif len(self.main_window.chessboard.getChessPosition(State.WHITE)) == 1:
            return State.BLACK
        else:
            chessboard = self.main_window.chessboard.getChessboard()
            chessboard_black = zeros([8, 8], dtype=int)
            chessboard_white = zeros([8, 8], dtype=int)
            
            for i in range(8):
                for j in range(8):
                    if chessboard[i][j] == State.BLACK:
                        chessboard_black[i][j] == 1
            for i in range(8):
                for j in range(8):
                    if chessboard[i][j] == State.WHITE:
                        chessboard_white[i][j] == 1
            
            check_black_win = eightConnectivityTwoPass(chessboard_black)
            check_white_win = eightConnectivityTwoPass(chessboard_white)
            
            # Black chess won.
            if check_black_win == 1 and check_white_win == 0:
                return State.BLACK
            # White chess won.
            elif check_white_win == 1 and check_black_win == 0:
                return State.WHITE
            # Keep going.
            else:
                return State.EMPTY
    
if __name__ == '__main__':
    """
    Program entry.
    """
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(argv)
        
    controller = Controller()
    
    app.exec_()
