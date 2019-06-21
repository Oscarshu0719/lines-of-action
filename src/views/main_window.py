# -*- coding: utf-8 -*-

from math import floor
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow, QMessageBox
from src.models.chessboard import Chessboard, State

class MainWindow(QMainWindow):
    """ Class
    Main window class.
    """
    _CHESSBOARD_SIZE = [633, 633]
    _STATUS_BAR_LEN = 25
    _BORDER_LEN = 11
    _FRAME_LEN = 3
    _GRID_SIZE= [(_CHESSBOARD_SIZE[0] - _FRAME_LEN * 9 - _BORDER_LEN * 2) / 8, 
                 (_CHESSBOARD_SIZE[1] - _FRAME_LEN * 9 - _BORDER_LEN * 2) / 8]
    _CHESS_SIZE = 34
    _DIRECTION = [[1, 0], [0, 1], [1, 1], [1, -1]]
    
    PATH_WINDOW_ICON = r'conf/chess_black.png'
    PATH_CHESSBOARD = r'conf/chessboard.jpg'
    PATH_BLACK_CHESS = r'conf/chess_black.png'
    PATH_WHITE_CHESS = r'conf/chess_white.png'
    PATH_HIGHLIGHT_BEIGE = r'conf/highlight_grid_beige.jpg'
    PATH_HIGHLIGHT_BROWN = r'conf/highlight_grid_brown.jpg'
    
    # Singal. Call `setAvailableMovement` function.
    signal_set_available_movement = pyqtSignal([int, int])
    # Sigbal. Call `aiTurnMonteCarloTreeSearch` function.
    signal_ai_turn = pyqtSignal()
    
    def setupUi(self, main_window):
        """
        Setup GUI.
        """
        self.setWindowTitle("Lines of action")
        self.setWindowIcon(QIcon(MainWindow.PATH_WINDOW_ICON))
        
        # Fixed-size window.
        self.setFixedSize(MainWindow._CHESSBOARD_SIZE[0], \
                          MainWindow._CHESSBOARD_SIZE[1] + MainWindow._STATUS_BAR_LEN)
        
        self.pos_x = 1000
        self.pos_y = 1000

        # Check if it's user's turn now.
        self.is_user_turn = True
        self.current_step = 0
        self.lasting_time = 0
        
        self.statusbar_msg = ''
        
        self.check_exchange_turn = False
        
        self._available_movement = []
        
        # Clicked grid.
        self.from_grid = []
        self.ai_move = []
        
        # Chess images.
        self.black_chess = QPixmap(MainWindow.PATH_BLACK_CHESS)
        self.white_chess = QPixmap(MainWindow.PATH_WHITE_CHESS)
        self.highlight_beige = QPixmap(MainWindow.PATH_HIGHLIGHT_BEIGE)
        self.highlight_brown = QPixmap(MainWindow.PATH_HIGHLIGHT_BROWN)
        
        # Change the cursor to hand-like icon.
        self.setCursor(Qt.PointingHandCursor)

        # Cursor.
        self.cursor = LabelChess(self)
        # Always on the top.
        self.cursor.raise_()
        
        # The labels of the grids on the chessboard to store chess images.
        self.chess_labels = [[LabelChess(self) for i in range(8)] for j in range(8)]
        for y in self.chess_labels:
            for x in y:
                x.setVisible(True)
                x.setScaledContents(True)
        
        # Chessboard.
        self.chessboard = Chessboard()
        
        # Set the starting chess.
        self.resetChess()
        
        # Timer.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerRun)
        
        # Setup signals.
        self.signal_set_available_movement[int, int].connect(main_window.setAvailableMovement)
        self.signal_ai_turn.connect(main_window.aiTurnMonteCarloTreeSearch)
        
        self.setMouseTracking(True)
        
        self.show()
        
        rules =  '1. Players alternate moves, with Black having the first move.\n'
        rules += '2. Checkers move horizontally, vertically, or diagonally.\n'
        rules += '3. A checker moves exactly as many spaces as there are checkers (both friendly and enemy) on the line in which it is moving.\n'
        rules += '4. A checker may jump over friendly checkers, but not over an enemy checker.\n'
        rules += '5. If a checker moves to an enemy checker, then remove the enemy checker, and move the checker to the space.\n'
        rules += '6. If a player has some checker to move, then the player cannot abstain.\n'
        rules += '7. If a player does not move a checker for one minute, then the player loses the game.'
        QMessageBox.information(self, 'Rules', rules, \
                                QMessageBox.Yes, QMessageBox.Yes)
        
        goals =  '1. Bring all of one\'s checkers together into a contiguous body'
        goals += 'so that they are connected vertically, horizontally or diagonally'
        goals += ' (8-connectivity). \n'
        goals += '2. If one\'s enemy only has one checker, then the player wins the game.'
        reply = QMessageBox.information(self, 'Goals', goals, \
                                QMessageBox.Yes, QMessageBox.Yes)
        
        # The timer starts after the user close the info windows.
        if reply == QMessageBox.Yes:
            # 1 second.
            self.timer.start(1000)
            self.past_time = 0
            
    def setStatusbur(self, message):
        """
        Setup Statusbar.
        """
        self.statusBar().showMessage(message)
    
    def checkChessMove(self, from_grid, from_chess, to_grid):
        """
        Check if the chess movement is legal.
        """
        if from_chess != State.BLACK or not self.is_user_turn:
            return False
        elif to_grid not in self._available_movement:
            return False
        else:
            return True
        
    def setAvailableMovement(self, available_movement):
        """
        Setup `self._available_movement`.
        """
        self._available_movement = available_movement
        
    def paintEvent(self, event):
        """ Slot function.
        While painting again, this function is called.
        """
        self.painter = QPainter()
        self.painter.begin(self)
        
        self.painter.setPen(QPen(Qt.NoPen))
        self.painter.drawPixmap(0, 0, MainWindow._CHESSBOARD_SIZE[0], \
                                MainWindow._CHESSBOARD_SIZE[1], \
                                QPixmap(MainWindow.PATH_CHESSBOARD))

        self.painter.end()

    def mousePressEvent(self, event):
        """ Slot function
        While mouse is pressed, this function is called, and while the chess is 
        right-clicked, it's cleared first and the legal movements are 
        highlighted. If the mouse is right-clicked, the user can decide to 
        restart the game.
        """
        if self.check_exchange_turn:
            self.check_exchange_turn = False
            self.is_user_turn = True
        
        # User moves black chess.
        if event.buttons() == Qt.LeftButton and self.is_user_turn:
            grid_x, grid_y = self.coordinate2ChessboardGrid(event.x(), event.y())
            if grid_x != -1 and grid_y != -1:
                if self.is_user_turn:
                    cleared_chess = self.clearChess(grid_x, grid_y)
                    self.from_grid = [grid_x, grid_y, cleared_chess]
                    if self.chessboard.getCoordinateState(grid_x, grid_y) == State.BLACK:
                        self.signal_set_available_movement.emit(grid_x, grid_y)
                        self.highlight_grid()
            else:
                pass
        # Restart the game.
        elif event.buttons() == Qt.RightButton:
            self.timer.stop()
            
            reply = QMessageBox.question(self, 'Restart', 'Are you sure?', \
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.chessboard.resetChessboard()
                self.resetChess()
                self.update()
                self.current_step = 0
                self.past_time = 0
                self.is_user_turn = True
            else:
                self.timer.start(1000)
                
    def mouseReleaseEvent(self, event):
        """ Slot function
        While mouse is pressed, this function is called, and while the mouse is 
        released, check if it's legal first and clear the highlighted movements.
        """
        if self.check_exchange_turn:
            self.check_exchange_turn = False
            self.is_user_turn = True
        
        # User moves black chess, and check the legality.
        if event.button() == Qt.LeftButton and self.is_user_turn:
            grid_x, grid_y = self.coordinate2ChessboardGrid(event.x(), event.y())
            if grid_x != -1 and grid_y != -1:
                if self.checkChessMove(self.from_grid[0: 2], self.from_grid[2], [grid_x, grid_y]):
                    self.chessboard.setCoordinateState(self.from_grid[0], self.from_grid[1], State.EMPTY)
                    self.chessboard.setCoordinateState(grid_x, grid_y, State.BLACK)
                    self.drawChess(grid_x, grid_y, State.BLACK)      
                    self.is_user_turn = False
                    self.current_step += 1
                    self.signal_ai_turn.emit()
                    
                    self.statusbar_msg = 'Steps: {}. Black: ({}, {}) -> ({}, {}); White: ({}, {}) -> ({}, {}). Computed time: {}s.'.format( \
                                      self.current_step, self.from_grid[0] + 1, self.from_grid[1] + 1, grid_x + 1, grid_y + 1, self.ai_move[0][0] + 1, self.ai_move[0][1] + 1, self.ai_move[1][0] + 1, self.ai_move[1][1] + 1, self.lasting_time)
                    self.past_time = 0
                else:
                    if self.from_grid[2] != State.EMPTY:
                        self.drawChess(self.from_grid[0], self.from_grid[1], self.from_grid[2])
                    self.chessboard.setCoordinateState(self.from_grid[0], self.from_grid[1], self.from_grid[2])
                    self.from_grid.clear()
            
            # Clear highlighted grids.
            if [grid_x, grid_y] in self._available_movement:
                self._available_movement.remove([grid_x, grid_y])
            for i in self._available_movement:
                self.clearChess(i[0], i[1])
                chess = self.chessboard.getCoordinateState(i[0], i[1]) 
                if chess != State.EMPTY:
                    self.drawChess(i[0], i[1], chess)

    def highlight_grid(self):
        """
        Hightligth legal movements grids.
        """
        for grid in self._available_movement:
            if (grid[0] + grid[1]) % 2 == 0:
                self.chess_labels[grid[0]][grid[1]].setPixmap(self.highlight_beige)
            else:
                self.chess_labels[grid[0]][grid[1]].setPixmap(self.highlight_brown)
            pos_x, pos_y = self.coordinate2ChessboardCoordinate(grid[0], grid[1])
            # TODO: pos_x, pos_y.
            self.chess_labels[grid[0]][grid[1]].setGeometry(pos_x - 19.5, pos_y - 19.5, MainWindow._GRID_SIZE[1], MainWindow._GRID_SIZE[0])
            
    def drawChess(self, grid_x, grid_y, chess):
        """
        Draw the chess image.
        """
        pos_x, pos_y = self.coordinate2ChessboardCoordinate(grid_x, grid_y)
        
        self.chess_labels[grid_x][grid_y].clear()
        if chess == State.BLACK:
            self.chess_labels[grid_x][grid_y].setPixmap(self.black_chess)
        elif chess == State.WHITE:
            self.chess_labels[grid_x][grid_y].setPixmap(self.white_chess)
            
        self.chessboard.setCoordinateState(grid_x, grid_y, chess)
        self.chess_labels[grid_x][grid_y].setGeometry(pos_x, pos_y, MainWindow._CHESS_SIZE, MainWindow._CHESS_SIZE)
        
    def clearChess(self, grid_x, grid_y):
        """
        Clear the chess image.
        """
        cleared_chess = self.chessboard.getCoordinateState(grid_x, grid_y)
        self.chess_labels[grid_x][grid_y].clear()
        
        return cleared_chess
        
    def coordinate2ChessboardGrid(self, pos_x, pos_y):
        """
        Compute the grid position on the chessboard from the chessboard 
        coordinates.
        """
        if pos_x <= MainWindow._BORDER_LEN or pos_y <= MainWindow._BORDER_LEN or pos_x >= MainWindow._CHESSBOARD_SIZE[1] - MainWindow._BORDER_LEN or pos_y >= MainWindow._CHESSBOARD_SIZE[0] - MainWindow._BORDER_LEN: 
            return -1, -1
        else:
            grid_x = floor((pos_x - MainWindow._BORDER_LEN - MainWindow._FRAME_LEN) / (MainWindow._GRID_SIZE[1] + MainWindow._FRAME_LEN))
            grid_y = floor((pos_y - MainWindow._BORDER_LEN - MainWindow._FRAME_LEN) / (MainWindow._GRID_SIZE[0] + MainWindow._FRAME_LEN))
            return grid_x, grid_y
        
    def coordinate2ChessboardCoordinate(self, grid_x, grid_y):
        """
        Compute the chessboard coordinates from original coordinates.
        """
        coordinate_x = MainWindow._BORDER_LEN + MainWindow._FRAME_LEN * (grid_x + 1) + grid_x * MainWindow._GRID_SIZE[1] + (MainWindow._GRID_SIZE[1] - MainWindow._CHESS_SIZE) / 2
        coordinate_y = MainWindow._BORDER_LEN + MainWindow._FRAME_LEN * (grid_y + 1) + grid_y * MainWindow._GRID_SIZE[0] + (MainWindow._GRID_SIZE[0] - MainWindow._CHESS_SIZE) / 2
        return coordinate_x, coordinate_y
    
    def gameEnd(self, winner):
        """
        After the game ends, show pop-up window to check if the user wants to 
        play again.
        """
        self.timer.stop()
        
        if winner == State.BLACK:
            reply = QMessageBox.question(self, 'Restart', 'Congrats! You win this game.\nPlay again?', \
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        elif winner == State.WHITE:
            reply = QMessageBox.question(self, 'Restart', 'Sorry. You lose this game.\nPlay again?',  \
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.chessboard.resetChessboard()
            self.resetChess()
            self.update()
            self.current_step = 0
            self.past_time = 0
            self.is_user_turn = True
            self.timer.start(1000)
        else:
            self.close()
    
    def resetChess(self):
        """
        Reset the chessboard to the beginning.
        """
        for i in range(8):
            for j in range(8):
                self.clearChess(i, j)
        
        for i in range(1, 7):
            self.drawChess(0, i, State.WHITE)
            self.drawChess(7, i, State.WHITE)
            self.drawChess(i, 0, State.BLACK)
            self.drawChess(i, 7, State.BLACK)
            
    def closeEvent(self, event):
        """ Slot function.
        While the closed button is clicked, this function is called to 
        double-check the operation.
        """
        # Stop the timer.
        self.timer.stop()
        
        reply = QMessageBox.question(self, 'Quit', 'Are you sure?', \
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            self.timer.start(1000)
            event.ignore()
            
    def timerRun(self):
        if self.past_time == 60:
            self.gameEnd(State.WHITE)
        else:
            statusbar_msg = 'Past time: %s. ' % self.past_time + self.statusbar_msg
            self.setStatusbur(statusbar_msg)
            self.past_time += 1
      
class LabelChess(QLabel):
    """ Class
    Chessboard labels class.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        event.ignore()        
