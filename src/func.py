"""
    func.py

    Description:
    A series of helper functions used by both the minimax and game master
"""

from copy import deepcopy


def make_move(board, player, move):

    new_board = deepcopy(board)
    opponent = 'W' if player == 'B' else 'B'

    if is_valid_move(board, player, move):
        new_board[move[1]][move[0]] = ' '
        new_board[move[3]][move[2]] = player

        # Resolve any intervention captures
        for x in range(0, 8, 1):
            for y in range(0, 8, 1):
                if new_board[y][x] == opponent:
                    # Check down
                    for down_space in range(y + 1, 8, 1):
                        if abs(y - down_space) > 1 and new_board[down_space][x] == opponent:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(y + 1, down_space, 1):
                                if new_board[inter][x] != player:
                                    capture_flag = False

                            if capture_flag:
                                # All pieces between these two pieces are opposite, so intervention by player

                                new_board[y][x] = ' '
                                new_board[down_space][x] = ' '

                    # Check right
                    for right_space in range(x + 1, 8, 1):
                        if abs(x - right_space) > 1 and new_board[y][right_space] == opponent:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True

                            for inter in range(x + 1, right_space, 1):
                                if new_board[y][inter] != player:
                                    capture_flag = False

                            if capture_flag:
                                # All pieces between these two pieces are opposite, so intervention by player

                                new_board[y][x] = ' '
                                new_board[y][right_space] = ' '

        for x in range(0, 8, 1):
            for y in range(0, 8, 1):
                if new_board[y][x] == player:
                    # Check down
                    for down_space in range(y + 1, 8, 1):
                        if new_board[down_space][x] == player:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(y + 1, down_space, 1):
                                if new_board[inter][x] != opponent:
                                    capture_flag = False

                            if capture_flag:
                                # All pieces between these two pieces are opposite, so capture them
                                for inter in range(y + 1, down_space, 1):

                                    new_board[inter][x] = ' '

                    # Check right
                    for right_space in range(x + 1, 8, 1):
                        if new_board[y][right_space] == player:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(x + 1, right_space, 1):
                                if new_board[y][inter] != opponent:
                                    capture_flag = False

                            if capture_flag:
                                # All pieces between these two pieces are opposite, so capture them
                                for inter in range(x + 1, right_space, 1):

                                    new_board[y][inter] = ' '

    return new_board


# Checks move legality and updates grid
def is_valid_move(board, player, move):

    piece_x = move[0]
    piece_y = move[1]
    new_loc_x = move[2]
    new_loc_y = move[3]

    if board[piece_y][piece_x] != player:
        # Chosen piece does not belong to the player or is not there, so invalid

        return False
    elif piece_x == new_loc_x and piece_y == new_loc_y:
        # Not moving the piece, so invalid

        return False
    elif piece_x == new_loc_x:
        # Moving Up or down

        # Look up or down to make sure no pieces between the piece and its new location
        if piece_y > new_loc_y:
            # Moving Up

            for loc in board[new_loc_y:piece_y]:
                if loc[piece_x] != ' ':

                    return False
            return True
        else:
            # Moving down

            for loc in board[piece_y + 1:new_loc_y + 1]:
                if loc[piece_x] != ' ':

                    return False
            return True
    elif piece_y == new_loc_y:
        # Moving left or right

        # Look left or right to make sure no pieces between the piece and its new location
        if piece_x > new_loc_x:
            # Moving left

            for loc in board[piece_y][new_loc_x:piece_x]:
                if loc != ' ':

                    return False
            return True
        else:
            # Moving right

            for loc in board[piece_y][piece_x + 1:new_loc_x + 1]:
                if loc != ' ':

                    return False
            return True
    else:
        # Piece is not moving in a straight line, so invalid
        return False
