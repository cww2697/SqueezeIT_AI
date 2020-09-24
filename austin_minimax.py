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
    # Set how deep we want to go
    depth = 3

    return minimax(board, player, depth, 1)

def minimax(board, player, depth, current_level):
    debugModifer = ""

    for i in range(0, current_level, 1):
        debugModifer += "\t"

    if depth < current_level:
        # We are at the bottom of the tree, time to propigate back up
        return heuristic(board, player)
    else:
        bestMove = ()
        bestHeuristic = -99 if current_level % 2 != 0 else 99

        # For each player piece, for each possible move, recursively call minimax() with current_level + 1
        for x in range(0, 7, 1):
            for y in range(0, 7, 1):
                if board[y][x] == player:
                    # Generate every possible move this player can do (limit search to just row and column)
                    
                    # Check vertical moves
                    for newY in range(0, 7, 1):
                        # Make a new move
                        currentMove = (x, y, x, newY)

                        print(debugModifer, "Considering", currentMove)

                        # If it is a valid move, 
                        if is_valid_move(board, player, currentMove):
                            currentHeuristic = minimax(make_move(board, player, currentMove), player, depth, current_level + 1)

                            if current_level % 2 != 0:
                                # Odd level, so maximize
                                if currentHeuristic > bestHeuristic:
                                    print(debugModifer, currentMove, "is better than", bestMove)
                                    bestMove = currentMove
                                    bestHeuristic = currentHeuristic
                            else:
                                # Even level, so minimize
                                if currentHeuristic < bestHeuristic:
                                    print(debugModifer, currentMove, "is better than", bestMove)
                                    bestMove = currentMove
                                    bestHeuristic = currentHeuristic
                        else:
                            print(debugModifer, currentMove, "is not a valid move")
                        
                        

                    # Check horizontal moves
                    for newX in range(0, 7, 1):
                        # Make a new move
                        currentMove = (x, y, newX, y)

                        # If it is a valid move, 
                        if is_valid_move(board, player, currentMove):
                            currentHeuristic = minimax(make_move(board, player, currentMove), player, depth, current_level + 1)

                            if current_level % 2 != 0:
                                # Odd level, so maximize
                                if currentHeuristic > bestHeuristic:
                                    print(debugModifer, currentMove, "is better than", bestMove)
                                    bestMove = currentMove
                                    bestHeuristic = currentHeuristic
                            else:
                                # Even level, so minimize
                                if currentHeuristic < bestHeuristic:
                                    print(debugModifer, currentMove, "is better than", bestMove)
                                    bestMove = currentMove
                                    bestHeuristic = currentHeuristic
                        else:
                            print(debugModifer, currentMove, "is not a valid move")
                    
                    # If we are propigating, return the best heuristic
                    # If we are done propigating, return the best move we found
                    if current_level == 1:
                        print(debugModifer, "Best move:", bestMove)
                        return bestMove
                    else:
                        print(debugModifer, "Best Heuristic at level", str(current_level) + ":", bestHeuristic)
                        return bestHeuristic

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

def make_move(board, player, move):
    newBoard = board

    newBoard[move[1]][move[0]] = ' '
    newBoard[move[3]][move[2]] = player

    return newBoard

# Given a board, player, and move, return whether the move is valid
def is_valid_move(board, player, move):
    pieceX = move[0]
    pieceY = move[1]
    new_locX = move[2]
    new_locY = move[3]

    if board[pieceY][pieceX] != player:
        # Chosen piece does not belong to the player or is not there, so invalid
        #print("Not Player Piece")
        return False
    elif pieceX == new_locX and pieceY == new_locY:
        # Not moving the piece, so invalid
        #print("Not Moving")
        return False
    elif pieceX == new_locX:
        # Moving Up or down

        # Look up or down to make sure no pieces between the piece and its new location
        if pieceY > new_locY:
            # Moving Up
            #print("Moving Up")
            for loc in board[new_locY:pieceY]:
                #print(loc[pieceX])
                if loc[pieceX] != ' ':
                    #print("Piece In Way")
                    return False
            return True
        else:
            # Moving down
            #print("Moving Down")
            for loc in board[pieceY+1:new_locY+1]:
                #print(loc[pieceX])
                if loc[pieceX] != ' ':
                    #print("Piece In Way")
                    return False
            return True
    elif pieceY == new_locY:
        # Moving left or right

        # Look left or right to make sure no pieces between the piece and its new location
        if pieceX > new_locX:
            # Moving left
            #print("Moving Left")
            for loc in board[pieceY][new_locX:pieceX]:
                #print(loc)
                if loc != ' ':
                    #print("Piece In Way")
                    return False
            return True
        else:
            # Moving right
            #print("Moving Right")
            for loc in board[pieceY][pieceX+1:new_locX+1]:
                #print(loc)
                if loc != ' ':
                    #print("Piece In Way")
                    return False
            return True
    else:
        # Piece is not moving in a straight line, so invalid
        #print("Not moving in a straight line")
        return False
