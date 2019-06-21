# -*- coding: utf-8 -*-

from numpy import zeros
from src.models.chessboard import State

def eightConnectivityTwoPass(chessboard):
    """
    Two-pass algorithm to check if the input image is eight-connective.
    """
    chessboard_labels = zeros([8, 8], dtype=int)
    
    index = 1
    check_connective = True
    check_first_chess = True
    for iter_time in range(2):
        for i in range(8):
            for j in range(8):
                if chessboard[i][j] != State.EMPTY:
                    if index == 1 and check_first_chess:
                        chessboard_labels[i][j] = 1
                        check_connective = True
                        check_first_chess = False
                    else:
                        neighbors = findNeighborsWithoutZeros(i, j, chessboard_labels)
                        if len(neighbors) == 0:
                            if check_connective == False:
                                index += 1
                            chessboard_labels[i][j] = index
                        else:
                            chessboard_labels[i][j] = min(neighbors)
                        check_connective = True
                else:
                    check_connective = False
    
    chess_label = 0
    for i in range(8):
        for j in range(8):
            if chess_label == 0:
                chess_label = chessboard_labels[i][j]
            else:
                if chess_label != chessboard_labels[i][j]:
                    return 0
    
    return 1
                
def findNeighborsWithoutZeros(self, row, column, chessboard_labels):
    """
    Find the surronding pixels values of a specified position.
    """
    mask_range = []
    if row == 0:
        mask_range.append(row)
        mask_range.append(row + 1)
    elif row == 7:
        mask_range.append(row - 1)
        mask_range.append(row)
    else:
        mask_range.append(row - 1)
        mask_range.append(row + 1)
    
    if column == 0:
        mask_range.append(column)
        mask_range.append(column + 1)
    elif row == 7:
        mask_range.append(column - 1)
        mask_range.append(column)
    else:
        mask_range.append(column - 1)
        mask_range.append(column + 1)
    
    tmp = [i[mask_range[2]: mask_range[3] + 1] \
           for i in chessboard_labels[mask_range[0]: mask_range[1] + 1]]            
    
    return [j for i in tmp for j in i if j != 0]