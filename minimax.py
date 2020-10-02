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

def get_next_move(board, player, heuristic_method):
    # Set how deep we want to go
    depth = 3

    # Initialize Debug File
    debug_file = open('austin_minimax_debug.txt', 'w')
    debug_file.write(datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).isoformat())
    debug_file.write('\n\n')

    result = minimax(board, player, depth, 1, -99, debug_file, heuristic_method)

    debug_file.close()

    #print(result)

    return result

def minimax(board, player, depth, current_level, ab_best, debug_file, heuristic_method):
    debugModifer = ''

    debugModifer = ''

    for i in range(0, current_level-1, 1):
        debugModifer += '\t'
    
    debugModifer += str(current_level) + ' - '

    if depth < current_level:
        # We are at the bottom of the tree, time to propigate back up
        #debug_file.write(debugModifer + 'At bottom. Get value of board\n')
        if heuristic_method == 'simple':
            return heurisitcs.simple_heuristic(board, player)
        elif heuristic_method == 'aggressive':
            return heurisitcs.aggressive_heuristic(board, player)
        elif heuristic_method == 'defensive':
            return heurisitcs.defensive_heuristic(board, player)
    else:
        # Initialize containers for best moves
        # If we are minimizing, use 99. If maximizing, use -99 (i.e., no matter what, the heuristic will be
        # replaced on the first move we look at)
        bestMove = ()
        bestHeuristic = -99 if current_level % 2 != 0 else 99
        opponent = 'W' if player == 'B' else 'B'
        current_player = player if current_level % 2 != 0 else opponent

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

                        ##print(debugModifer, 'Considering', currentMove)
                        debug_file.write(debugModifer + ' Considering ' + str(currentMove) + '\n')

                        # If it is a valid move, 
                        if func.is_valid_move(board, current_player, currentMove):
                            currentHeuristic = minimax(func.make_move(board, current_player, currentMove), player, depth, current_level + 1, bestHeuristic, debug_file, heuristic_method)

                            if current_level % 2 != 0:
                                # Odd level, so maximize

                                # See if we can prune
                                if current_level == 1 or currentHeuristic < ab_best:
                                    if currentHeuristic > bestHeuristic:
                                        ##print(debugModifer, currentMove, 'is better than', bestMove, f'({str(currentHeuristic)} > {str(bestHeuristic)})')
                                        debug_file.write(debugModifer + str(currentMove) + ' is better than ' + str(bestMove) + f'({str(currentHeuristic)} > {str(bestHeuristic)})\n')
                                        bestMove = currentMove
                                        bestHeuristic = currentHeuristic
                                else:
                                    # Prune the branch
                                    debug_file.write(debugModifer + f'{currentHeuristic} >= {ab_best} PRUNING BRANCH\n')
                                    return 99
                            else:
                                # Even level, so minimize

                                if current_level == 1 or currentHeuristic > ab_best:
                                    if currentHeuristic < bestHeuristic:
                                        ##print(debugModifer, currentMove, 'is better than', bestMove, f'({str(currentHeuristic)} < {str(bestHeuristic)})')
                                        debug_file.write(debugModifer + str(currentMove) + ' is better than ' + str(bestMove) + f'({str(currentHeuristic)} < {str(bestHeuristic)})\n')
                                        bestMove = currentMove
                                        bestHeuristic = currentHeuristic
                                else:
                                    # Prune the branch
                                    debug_file.write(debugModifer + f'{currentHeuristic} <= {ab_best} PRUNING BRANCH\n')
                                    return -99
                        else:
                            ##print(debugModifer, currentMove, 'is not a valid move')
                            debug_file.write(debugModifer + str(currentMove) + ' is not a valid move\n')
                        
                        

                    # Check horizontal moves
                    for newX in range(0, 8, 1):
                        # Make a new move
                        currentMove = (x, y, newX, y)

                        ##print(debugModifer, 'Considering', currentMove)
                        debug_file.write(debugModifer + ' Considering ' + str(currentMove) + '\n')

                        # If it is a valid move
                        if func.is_valid_move(board, current_player, currentMove):
                            currentHeuristic = minimax(func.make_move(board, current_player, currentMove), player, depth, current_level + 1, bestHeuristic, debug_file, heuristic_method)

                            if current_level % 2 != 0:
                                # Odd level, so maximize

                                # See if we can prune
                                if current_level == 1 or currentHeuristic < ab_best:
                                    if currentHeuristic > bestHeuristic:
                                        ##print(debugModifer, currentMove, 'is better than', bestMove, f'({str(currentHeuristic)} < {str(bestHeuristic)})')
                                        debug_file.write(debugModifer + str(currentMove) + 'is better than' + f'({str(currentHeuristic)} < {str(bestHeuristic)})\n')
                                        bestMove = currentMove
                                        bestHeuristic = currentHeuristic
                                else:
                                    # Prune the branch
                                    debug_file.write(debugModifer + f'{currentHeuristic} <= {ab_best} PRUNING BRANCH\n')
                                    return 99
                            else:
                                # Even level, so minimize

                                if current_level == 1 or currentHeuristic > ab_best:
                                    if currentHeuristic < bestHeuristic:
                                        ##print(debugModifer, currentMove, 'is better than', bestMove, f'({str(currentHeuristic)} < {str(bestHeuristic)})')
                                        debug_file.write(debugModifer + str(currentMove) + 'is better than' + f'({str(currentHeuristic)} < {str(bestHeuristic)})\n')
                                        bestMove = currentMove
                                        bestHeuristic = currentHeuristic
                                else:
                                    # Prune the branch
                                    debug_file.write(debugModifer + f'{currentHeuristic} >= {ab_best} PRUNING BRANCH\n')
                                    return -99
                        else:
                            ##print(debugModifer, currentMove, 'is not a valid move')
                            debug_file.write(debugModifer + str(currentMove) + 'is not a valid move\n')
                    
        # If we are propigating, return the best heuristic
        # If we are done propigating, return the best move we found
        if current_level == 1:
            ##print(debugModifer, 'Best move:', bestMove, 'with Heuristic:', bestHeuristic)
            debug_file.write(debugModifer + 'Best move: ' + str(bestMove) + ' with Heuristic ' + str(bestHeuristic) + '\n')
            return bestMove
        else:
            ##print(debugModifer, 'Best Heuristic at level', str(current_level) + ':', bestHeuristic)
            debug_file.write(debugModifer + 'Best Heuristic at level ' + str(current_level) + ': ' + str(bestHeuristic) + '\n')
            return bestHeuristic
