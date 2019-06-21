# -*- coding: utf-8 -*-

from src.models.chessboard import State

def getAvailableMovement(pos_x, pos_y, chess, chessboard):
    """
    Return the legal movements.
    """
    available_movement = []
    if chess == State.BLACK:
        enemy_chess = State.WHITE
    else:
        enemy_chess = State.BLACK
        
    count_ver = sum([1 for i in chessboard if i[pos_x] != State.EMPTY])
    count_hor = sum([1 for i in chessboard[pos_y] if i != State.EMPTY])
    start = min(pos_x, pos_y)
    diff = abs(pos_x - pos_y)
    count_diagonal = sum([1 for i in range(7 - diff + 1) \
                          if chessboard[pos_y - start + i][pos_x - start + i] != State.EMPTY])
    start = pos_x + pos_y
    diff = max(start - 7, 0)
    start -= diff
    count_paradiagonal = sum([1 for i in range(start - diff + 1) \
                              if chessboard[start - i][diff + i] != State.EMPTY])

    # Vertical (x-direction).
    if pos_y - count_ver >= 0 and chessboard[pos_y - count_ver][pos_x] != chess:
        count_invalid = sum([1 for i in range(pos_y - count_ver + 1, pos_y) \
                             if chessboard[i][pos_x] == enemy_chess])
        if count_invalid == 0:
            available_movement.append([pos_x, pos_y - count_ver])
    if pos_y + count_ver <= 7 and chessboard[pos_y + count_ver][pos_x] != chess:
        count_invalid = sum([1 for i in range(pos_y + 1, pos_y + count_ver + 1 - 1) \
                             if chessboard[i][pos_x] == enemy_chess])
        if count_invalid == 0:
            available_movement.append([pos_x, pos_y + count_ver])
    
    # Horizontal (y-direction).
    if pos_x - count_hor >= 0 and chessboard[pos_y][pos_x - count_hor] != chess:
        count_invalid = sum([1 for i in range(pos_x - count_hor + 1, pos_x) \
                             if chessboard[pos_y][i] == enemy_chess])
        if count_invalid == 0:
            available_movement.append([pos_x - count_hor, pos_y]) 
    if pos_x + count_hor <= 7 and chessboard[pos_y][pos_x + count_hor] != chess:
        count_invalid = sum([1 for i in range(pos_x + 1, pos_x + count_hor + 1 - 1) \
                             if chessboard[pos_y][i] == enemy_chess])
        if count_invalid == 0:
            available_movement.append([pos_x + count_hor, pos_y]) 
            
    # Diagonal.
    if min(pos_x, pos_y) - count_diagonal >= 0 and chessboard[pos_y - count_diagonal][pos_x - count_diagonal] != chess:
        count_invalid = sum([1 for i in range(1, count_diagonal + 1 - 1) \
                             if chessboard[pos_y - i][pos_x - i] == enemy_chess])
        if count_invalid == 0:
            available_movement.append([pos_x - count_diagonal, pos_y - count_diagonal])
    if max(pos_x, pos_y) + count_diagonal <= 7 and chessboard[pos_y + count_diagonal][pos_x + count_diagonal] != chess:
        count_invalid = sum([1 for i in range(1, count_diagonal + 1 - 1) \
                             if chessboard[pos_y + i][pos_x + i] == enemy_chess])
        if count_invalid == 0:
            available_movement.append([pos_x + count_diagonal, pos_y + count_diagonal])
            
    # Paradiagonal.
    if pos_y - count_paradiagonal >= 0 and pos_x + count_paradiagonal <= 7 \
    and chessboard[pos_y - count_paradiagonal][pos_x + count_paradiagonal] != chess:
        count_invalid = sum([1 for i in range(1, count_paradiagonal + 1 - 1) \
                             if chessboard[pos_y - i][pos_x + i] == enemy_chess])
        if count_invalid == 0:
            available_movement.append([pos_x + count_paradiagonal, pos_y - count_paradiagonal])
    if pos_x - count_paradiagonal >= 0 and pos_y + count_paradiagonal <= 7 \
    and chessboard[pos_y + count_paradiagonal][pos_x - count_paradiagonal] != chess:
        count_invalid = sum([1 for i in range(1, count_paradiagonal + 1 - 1) \
                             if chessboard[pos_y + i][pos_x - i] == enemy_chess])
        if count_invalid == 0:
            available_movement.append([pos_x - count_paradiagonal, pos_y + count_paradiagonal])

    return available_movement
