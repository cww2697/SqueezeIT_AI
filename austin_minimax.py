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
    return [0, 0, 1, 1]