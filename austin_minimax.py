# Written by Austin Maddox

# Description:
# This module defines a single function, get_next_move, which receives
# an 8x8 array representing a Squeeze-It board, where the position of
# white pieces is represented with W's, and the position of black pieces
# is represented with B's, along with the team the agent is making
# decisions for. The function returns a tuple of the format
#  
#           [x, y, a, b]
# 
# where (x, y) is the location of the piece to be moved, and (a, b) 
# is the new location

def get_next_move(board, player):
    # Do some minimax things
    return [0, 0, 1, 1]

# Heuristic function that judges the value of a particular game state 
# given a board and the player to be judged
def heuristic(board, player):
    # Notes for possible heuristic calculation
    # 
    #  - Obviously, if you are squeezing the opponent, that is good
    #  - If you are put into a position where you will be squeezed on 
    #    the next turn, that is bad (also squeezing yourself is probably
    #    bad)
    #  - Best to probably weight pieces captured vs pieces lost and take
    #    any move where we come out on top, even if sacrificing
    #  - Positions that threaten to squeeze two different pieces separatly
    #    is good, as it forces the opponent to choose and guarantees a 
    #    capture. For example (we are white)
    # 
    #       _ B W
    #       _ W B
    #       W _ _
    #  - Probably best to encourage reasonable aggression in the agent
    #  - If winning is the only objective, time wasting is a perfectly 
    #    viable strategy if we get a lead
    #      
    return 0

# Given a board, player, and move, return whether the move is valid
def is_valid_move(board, player, move):
    pieceX = move[0]
    pieceY = move[1]
    new_locX = move[2]
    new_locY = move[3]

    if board[pieceX, pieceY] != player:
        # Chosen piece does not belong to the player or is not there, so invalid
        return False
    elif pieceX == new_locX and pieceY == new_locY:
        # Not moving the piece, so invalid
        return False
    elif pieceX == new_locX:
        # Moving up or down

        # Look up or down to make sure no pieces between the piece and its new location
        if pieceY > new_locY:
            # Moving up

            for loc in board[pieceX][new_locY:pieceY-1]:
                if loc != '':
                    return False
            return True
        else:
            # Moving down

            for loc in board[pieceX][pieceY+1:new_locY]:
                if loc != '':
                    return False
            return True
    elif pieceY == new_locY:
        # Moving left or right

        # Look left or right to make sure no pieces between the piece and its new location
        if pieceX > new_locX:
            # Moving left

            for loc in board[new_locX:pieceX-1]:
                if loc[pieceY] != '':
                    return False
            return True
        else:
            # Moving right

            for loc in board[pieceX+1:new_locX]:
                if loc[pieceY] != '':
                    return False
            return True
    else:
        # Piece is not moving in a straight line, so invalid
        return False
