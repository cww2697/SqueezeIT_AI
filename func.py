"""
    func.py

    Description:
    A series of helper functions used by both the minimax and game master
"""

from copy import deepcopy

def make_move(board, player, move):
    ###print(player, f'({move[0]}, {move[1]}) to ({move[2]}, {move[3]})')
    newBoard = deepcopy(board)
    opponent = 'W' if player == 'B' else 'B'

    if is_valid_move(board, player, move):
        newBoard[move[1]][move[0]] = ' '
        newBoard[move[3]][move[2]] = player

        # Resolve any intervention captures
        for x in range(0, 8, 1):
            for y in range(0, 8, 1):
                if newBoard[y][x] == opponent:
                    # Check down
                    for down_space in range(y+1, 8, 1):
                        if abs(y - down_space) > 1 and newBoard[down_space][x] == opponent:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(y+1, down_space, 1):
                                if newBoard[inter][x] != player:
                                    capture_flag = False
                            
                            if capture_flag:
                                # All pieces between these two pieces are opposite, so intervention by player
                                #print(f"remove ({x}, {y}) and ({x}, {down_space})")
                                newBoard[y][x] = ' '
                                newBoard[down_space][x] = ' '

                    # Check right
                    for right_space in range(x+1, 8, 1):
                        if abs(x - right_space) > 1 and newBoard[y][right_space] == opponent:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True

                            for inter in range(x+1, right_space, 1):
                                if newBoard[y][inter] != player:
                                    capture_flag = False
                            
                            if capture_flag:
                                # All pieces between these two pieces are opposite, so intervention by player
                                #print(f"remove ({x}, {y}) and ({right_space}, {y})")
                                newBoard[y][x] = ' '
                                newBoard[y][right_space] = ' '
        
        for x in range(0, 8, 1):
            for y in range(0, 8, 1):
                if newBoard[y][x] == player:
                    # Check down
                    for down_space in range(y+1, 8, 1):
                        if newBoard[down_space][x] == player:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(y+1, down_space, 1):
                                if newBoard[inter][x] != opponent:
                                    capture_flag = False
                            
                            if capture_flag:
                                # All pieces between these two pieces are opposite, so capture them
                                for inter in range(y+1, down_space, 1):
                                    ##print(f'{opponent} lost piece at ({x}, {inter})')
                                    newBoard[inter][x] = ' '
                                    
                    # Check right
                    for right_space in range(x+1, 8, 1):
                        if newBoard[y][right_space] == player:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(x+1, right_space, 1):
                                if newBoard[y][inter] != opponent:
                                    capture_flag = False
                            
                            if capture_flag:
                                # All pieces between these two pieces are opposite, so capture them
                                for inter in range(x+1, right_space, 1):
                                    ##print(f'{opponent} lost piece at ({inter}, {y})')
                                    newBoard[y][inter] = ' '

    return newBoard

# Checks move legality and updates grid
def is_valid_move(board, player, move):
    ###print(board),
    ###print(player)
    ###print(move)

    pieceX = move[0]
    pieceY = move[1]
    new_locX = move[2]
    new_locY = move[3]

    if board[pieceY][pieceX] != player:
        # Chosen piece does not belong to the player or is not there, so invalid
        ###print('Not Player Piece')
        return False
    elif pieceX == new_locX and pieceY == new_locY:
        # Not moving the piece, so invalid
        ###print('Not Moving')
        return False
    elif pieceX == new_locX:
        # Moving Up or down

        # Look up or down to make sure no pieces between the piece and its new location
        if pieceY > new_locY:
            # Moving Up
            ###print('Moving Up')
            for loc in board[new_locY:pieceY]:
                if loc[pieceX] != ' ':
                    ###print('Piece In Way')
                    return False
            return True
        else:
            # Moving down
            ###print('Moving Down')
            for loc in board[pieceY+1:new_locY+1]:
                if loc[pieceX] != ' ':
                    ###print('Piece In Way')
                    return False
            return True
    elif pieceY == new_locY:
        # Moving left or right

        # Look left or right to make sure no pieces between the piece and its new location
        if pieceX > new_locX:
            # Moving left
            ###print('Moving Left')
            for loc in board[pieceY][new_locX:pieceX]:
                if loc != ' ':
                    ###print('Piece In Way')
                    return False
            return True
        else:
            # Moving right
            ###print('Moving Right')
            for loc in board[pieceY][pieceX+1:new_locX+1]:
                if loc != ' ':
                    ###print('Piece In Way')
                    return False
            return True
    else:
        # Piece is not moving in a straight line, so invalid
        ###print('Not moving in a straight line')
        return False