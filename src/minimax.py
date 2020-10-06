# Written by Austin Maddox

# Description:
# This module defines a single function, get_next_move, which receives
# an 8x8 array representing a Squeeze-It board, where the position of
# white pieces is represented with W's, and the position of black pieces
# is represented with B's, along with the team the agent is making
# decisions for. The function returns a tuple of the format
#  
#           (x, y, a, b)
# 
# where (x, y) is the location of the piece to be moved, and (a, b) 
# is the new location

from copy import deepcopy
import datetime
import heurisitcs
import func

class PruneBranch(Exception):
    pass

def get_next_move(board, player, heuristic_method):
    # Set how deep we want to go
    depth = 3

    debug_flag = False
    debug_file = ""

    # Initialize debug File
    if debug_flag:
        debug_file = open('austin_minimax_debug.txt', 'w')
        debug_file.write(datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).isoformat())
        debug_file.write('\n\n')

    result = minimax(board, player, depth, 1, -99, 99, heuristic_method, debug_flag, debug_file)

    if debug_flag:
        debug_file.close()

    #print(result)

    return result

def minimax(board, player, depth, current_level, a, b, heuristic_method, debug_flag, debug_file):
    alpha = a
    beta = b
    
    debugModifer = ''

    for i in range(0, current_level-1, 1):
        debugModifer += '\t'
    
    debugModifer += str(current_level) + ' - '

    if depth < current_level:
        # We are at the bottom of the tree, time to propigate back up
        heuristic_value = 0

        if heuristic_method == 'simple':
            heuristic_value = heurisitcs.simple_heuristic(board, player)
        elif heuristic_method == 'aggressive':
            heuristic_value = heurisitcs.aggressive_heuristic(board, player)
        elif heuristic_method == 'defensive':
            heuristic_value = heurisitcs.defensive_heuristic(board, player)
        elif heuristic_method == 'stay_in_center':
            heuristic_value = heurisitcs.stay_in_the_center_heuristic(board, player)
        
        if debug_flag: debug_file.write(debugModifer + f'{heuristic_method} heuristic gives value of {heuristic_value}\n')

        return heuristic_value
    else:
        # Initialize containers for best moves
        # If we are minimizing, use 99. If maximizing, use -99 (i.e., no matter what, the heuristic will be
        # replaced on the first move we look at)
        bestMove = ()
        bestHeuristic = -99 if current_level % 2 != 0 else 99
        opponent = 'W' if player == 'B' else 'B'
        current_player = player if current_level % 2 != 0 else opponent

        try:
            # For each player piece, for each possible move, recursively call minimax() with current_level + 1
            for x in range(0, 8, 1):
                for y in range(0, 8, 1):
                    # When odd, consider your moves. When even, consider opponent moves
                    if board[y][x] == current_player:
                        # Generate every possible move this piece can do (limit search to just row and column)
                        
                        # Check vertical moves
                        for newY in range(0, 8, 1):
                            # Make a new move
                            currentMove = (x, y, x, newY)

                            if debug_flag: debug_file.write(debugModifer + ' Considering ' + str(currentMove) + '\n')

                            # If it is a valid move, 
                            if func.is_valid_move(board, current_player, currentMove):
                                currentHeuristic = minimax(func.make_move(board, current_player, currentMove), player, depth, current_level + 1, alpha, beta, heuristic_method, debug_flag, debug_file)

                                if current_level % 2 != 0:
                                    # Odd level, so maximize

                                    # Get max we have seen at this node and what we just saw
                                    if currentHeuristic > bestHeuristic:
                                        if debug_flag: debug_file.write(debugModifer + str(currentMove) + ' is better than ' + str(bestMove) + f'({str(currentHeuristic)} > {str(bestHeuristic)})\n')
                                        bestMove = currentMove
                                        bestHeuristic = currentHeuristic

                                    # See if best we have seen at this node is better than alpha
                                    if bestHeuristic > alpha:
                                        alpha = bestHeuristic
                                    
                                    # If alpha >= beta, we can prune
                                    if alpha >= beta:
                                        if debug_flag: debug_file.write(debugModifer + f'{alpha} >= {beta} PRUNING BRANCH\n')
                                        raise PruneBranch
                                else:
                                    # Even level, so minimize
                                    if currentHeuristic < bestHeuristic:
                                        if debug_flag: debug_file.write(debugModifer + str(currentMove) + ' is better than ' + str(bestMove) + f'({str(currentHeuristic)} < {str(bestHeuristic)})\n')
                                        bestMove = currentMove
                                        bestHeuristic = currentHeuristic
                                    
                                    if bestHeuristic < beta:
                                        beta = bestHeuristic
                                    
                                    if alpha >= beta:
                                        if debug_flag: debug_file.write(debugModifer + f'{alpha} >= {beta} PRUNING BRANCH\n')
                                        raise PruneBranch
                            else:
                                if debug_flag: debug_file.write(debugModifer + str(currentMove) + ' is not a valid move\n') 

                        # Check horizontal moves
                        for newX in range(0, 8, 1):
                            # Make a new move
                            currentMove = (x, y, newX, y)

                            ##print(debugModifer, 'Considering', currentMove)
                            if debug_flag: debug_file.write(debugModifer + ' Considering ' + str(currentMove) + '\n')

                            # If it is a valid move
                            if func.is_valid_move(board, current_player, currentMove):
                                currentHeuristic = minimax(func.make_move(board, current_player, currentMove), player, depth, current_level + 1, alpha, beta, heuristic_method, debug_flag, debug_file)

                                if current_level % 2 != 0:
                                    # Odd level, so maximize

                                    # Get max we have seen at this node and what we just saw
                                    if currentHeuristic > bestHeuristic:
                                        if debug_flag: debug_file.write(debugModifer + str(currentMove) + ' is better than ' + str(bestMove) + f'({str(currentHeuristic)} > {str(bestHeuristic)})\n')
                                        bestMove = currentMove
                                        bestHeuristic = currentHeuristic

                                    # See if best we have seen at this node is better than alpha
                                    if bestHeuristic > alpha:
                                        alpha = bestHeuristic
                                    
                                    # If alpha >= beta, we can prune
                                    if alpha >= beta:
                                        if debug_flag: debug_file.write(debugModifer + f'{alpha} >= {beta} PRUNING BRANCH\n')
                                        raise PruneBranch
                                else:
                                    # Even level, so minimize
                                    if currentHeuristic < bestHeuristic:
                                        if debug_flag: debug_file.write(debugModifer + str(currentMove) + ' is better than ' + str(bestMove) + f'({str(currentHeuristic)} < {str(bestHeuristic)})\n')
                                        bestMove = currentMove
                                        bestHeuristic = currentHeuristic
                                    
                                    if bestHeuristic < beta:
                                        beta = bestHeuristic
                                    
                                    if alpha >= beta:
                                        if debug_flag: debug_file.write(debugModifer + f'{alpha} >= {beta} PRUNING BRANCH\n')
                                        raise PruneBranch
                            else:
                                if debug_flag: debug_file.write(debugModifer + str(currentMove) + 'is not a valid move\n')
        except PruneBranch:
            pass    

        # If we are propigating, return the best heuristic
        # If we are done propigating, return the best move we found
        if current_level == 1:
            ##print(debugModifer, 'Best move:', bestMove, 'with Heuristic:', bestHeuristic)
            if debug_flag: debug_file.write(debugModifer + 'Best move: ' + str(bestMove) + ' with Heuristic ' + str(bestHeuristic) + '\n')
            return bestMove
        else:
            ##print(debugModifer, 'Best Heuristic at level', str(current_level) + ':', bestHeuristic)
            if debug_flag: debug_file.write(debugModifer + 'Best Heuristic at level ' + str(current_level) + ': ' + str(bestHeuristic) + '\n')
            return bestHeuristic
