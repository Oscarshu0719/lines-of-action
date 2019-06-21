# -*- coding: utf-8 -*-

from copy import deepcopy
from numpy import zeros
from random import choice
from src.models.chessboard import State
from src.models.eight_connectivity_two_pass import eightConnectivityTwoPass
from src.models.get_available_movement import getAvailableMovement as getMovement

class NodeState(object):
    """ Class
    Describe the state of a node.
    """
    MAX_ROUND = 200
    
    def __init__(self, chessboard):
        self._chessboard = deepcopy(chessboard)
        self._current_round = 0
        self._current_turn = 0
        self._best_movement = []
        self._available_movement = []
        self._is_end = 0
        
    def getChessboard(self):
        """
        Return the chessboard of this state.
        """
        return self._chessboard
    
    def getCurrentRound(self):
        """
        Return the current round of this state.
        """
        return self._current_round

    def getCurrentTurn(self):
        """
        Return the current turn of this state.
        """
        return self._current_turn
    
    def getBestMovement(self):
        """
        Return the best movement of this state.
        """
        return self._best_movement
   
    def getAvailableMovement(self):
        """
        Setup the legal movements of this state.
        """
        return self._available_movement
    
    def setChessboard(self, chessboard):
        """
        Setup the chessboard of this state.
        """
        self._chessboard = deepcopy(chessboard)
        
    def setCurrentRound(self, current_round):
        """
        Setup the current round of this state.
        """
        self._current_round = current_round

    def setCurrentTurn(self, turn):
        """
        Setup the current turn of this state.
        """
        self._current_turn = turn
        
    def setBestMovement(self, from_movement, to_movement):
        """
        Setup the best movement of this state.
        """
        self._best_movement.append(from_movement)
        self._best_movement.append(to_movement)
        
    def setAvailableMovement(self, available_movement):
        """
        Setup the legal movements of this state.
        """
        self._available_movement = available_movement
        
    def getChessPosition(self, chess):
        """
        Return positions of a kind of chess.
        """
        return [[i, j] for i in range(8) for j in range(8) if self._chessboard[i][j] == chess]
    
    def setChess(self, pos_x, pos_y, chess):
        """
        Setup the value of a specified position.
        """
        self._chessboard[pos_x][pos_y] = chess
        
    def checkTerminal(self):
        """
        Check if this node is a leaf node.
        """
        if self._is_end != 0 or self._current_round == NodeState.MAX_ROUND:
            return True
        else:
            return False
        
    def computeReward(self):
        """
        Compute ths reward of this state.
        """
        # White chess won.
        if self._is_end == 1: 
            return 1
        # Black chess won.
        elif self._is_end == 2: 
            return -1
        else:
            return 0
    
    def getNextState(self):
        """
        Return the next state of this state.
        """
        next_state = NodeState(self.getChessboard())
        
        # Change to the other player.
        if self.getCurrentTurn() == State.BLACK:
            next_state.setCurrentTurn(State.WHITE)
        else:
            next_state.setCurrentTurn(State.BLACK)

        available_choices = next_state.getChessPosition(next_state.getCurrentTurn())
        if len(available_choices) == 0:
            self._is_end = next_state.getCurrentTurn()
            return None
        from_movement = choice([choice for choice in available_choices])

        while True:
            available_movement = getMovement(from_movement[1], from_movement[0], \
                                             next_state.getCurrentTurn(), next_state.getChessboard())
            if len(available_movement) != 0:
                next_state.setAvailableMovement([[x[1], x[0]] for x in available_movement])
                break
            else:
                from_movement = choice([choice for choice in available_choices])
                
        to_movement = choice([choice for choice in next_state.getAvailableMovement()])
        next_state.setBestMovement(from_movement, to_movement)
        next_state.setChess(from_movement[0], from_movement[1], State.EMPTY)
        next_state.setChess(to_movement[0], to_movement[1], next_state.getCurrentTurn())
        next_state.setCurrentRound(self.getCurrentRound() + 1)
        
        next_state.checkGameEnd()
        
        return next_state
    
    def checkGameEnd(self):
        """
        Check if this game ends in this state.
        """
        # White chess won.
        if len(self.getChessPosition(State.BLACK)) <= 1:
            self._is_end = 1
        # Black chess won.
        elif len(self.getChessPosition(State.WHITE)) <= 1:
            self._is_end = 2
        else:
            chessboard = self.getChessboard()
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
                self._is_end = 2
            # White chess won.
            elif check_white_win == 1 and check_black_win == 0:
                self._is_end = 1
            # Keep going.
            else:
                self._is_end = 0        
