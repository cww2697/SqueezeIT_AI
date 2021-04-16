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


# Custom exception to escape out of nested loops when we prune a branch
class PruneBranch(Exception):
    pass


def get_next_move(board, player, heuristic_method):
    # Set how deep we want to go
    depth = 3

    # Flag for if we want a debug output file. Including the file increases runtime a bit,
    # but it allows us to see how the AI is making decisions
    debug_flag = True

    # Initialize debug File
    if debug_flag:
        date = datetime.datetime.now()
        debug_file_name = '{0}debug.txt'.format(date.strftime("%d%m%Y"))
        debug_file = open(debug_file_name, 'w+')
        debug_file.write(datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).isoformat())
        debug_file.write('\n\n')

    # Get the move
    result = minimax(board, player, depth, 1, -99, 99, heuristic_method, debug_flag, debug_file)

    if debug_flag:
        debug_file.close()

    return result


def minimax(board, player, depth, current_level, a, b, heuristic_method, debug_flag, debug_file):
    # Copy alpha and beta
    alpha = a
    beta = b

    # Modifier for debug file to indent farther as the depth gets greater
    debug_modifer = ''
    for i in range(0, current_level - 1, 1):
        debug_modifer += '\t'
    debug_modifer += str(current_level) + ' - '

    if depth < current_level:
        # We are at the bottom of the tree, time to get the value of the state and propagate back up
        heuristic_value = 0

        if heuristic_method == 'simple':
            heuristic_value = heurisitcs.simple_heuristic(board, player)
        elif heuristic_method == 'aggressive':
            heuristic_value = heurisitcs.aggressive_heuristic(board, player)
        elif heuristic_method == 'defensive':
            heuristic_value = heurisitcs.defensive_heuristic(board, player)
        elif heuristic_method == 'stay_in_center':
            heuristic_value = heurisitcs.stay_in_the_center_heuristic(board, player)

        # Record the value of the state if we are outputting
        if debug_flag: debug_file.write(
            debug_modifer + f'{heuristic_method} heuristic gives value of {heuristic_value}\n')

        return heuristic_value
    else:
        # Initialize containers for best moves
        # If we are minimizing, use 99. If maximizing, use -99 (i.e., no matter what, the heuristic will be
        # replaced on the first move we look at)
        best_move = ()
        best_heuristic = -99 if current_level % 2 != 0 else 99
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
                            current_move = (x, y, x, newY)

                            if debug_flag:
                                debug_file.write(
                                    '{0} Considering {1}\n'.format(debug_modifer, str(current_move)))

                            # If it is a valid move, 
                            if func.is_valid_move(board, current_player, current_move):
                                current_heuristic = minimax(func.make_move(board, current_player, current_move), player,
                                                            depth, current_level + 1, alpha, beta, heuristic_method,
                                                            debug_flag, debug_file)

                                if current_level % 2 != 0:
                                    # Odd level, so maximize

                                    # Get max we have seen at this node and what we just saw
                                    if current_heuristic > best_heuristic:
                                        if debug_flag: debug_file.write(
                                            debug_modifer + str(current_move) + ' is better than ' + str(
                                                best_move) + f'({str(current_heuristic)} > {str(best_heuristic)})\n')
                                        best_move = current_move
                                        best_heuristic = current_heuristic

                                    # See if best we have seen at this node is better than alpha
                                    if best_heuristic > alpha:
                                        alpha = best_heuristic

                                    # If alpha >= beta, we can prune
                                    if alpha >= beta:
                                        if debug_flag: debug_file.write(
                                            debug_modifer + f'{alpha} >= {beta} PRUNING BRANCH\n')
                                        raise PruneBranch
                                else:
                                    # Even level, so minimize
                                    if current_heuristic < best_heuristic:
                                        if debug_flag: debug_file.write(
                                            debug_modifer + str(current_move) + ' is better than ' + str(
                                                best_move) + f'({str(current_heuristic)} < {str(best_heuristic)})\n')
                                        best_move = current_move
                                        best_heuristic = current_heuristic

                                    # See if worse we have seen at this node is worse than beta
                                    if best_heuristic < beta:
                                        beta = best_heuristic

                                    # If alpha >= beta, we can prune
                                    if alpha >= beta:
                                        if debug_flag: debug_file.write(
                                            f'{0}{alpha} >= {beta} PRUNING BRANCH\n'.format(debug_modifer))
                                        raise PruneBranch
                            else:
                                if debug_flag: debug_file.write(
                                    '{0}{1} is not a valid move\n'.format(debug_modifer, str(current_move)))

                                # Check horizontal moves
                        for newX in range(0, 8, 1):
                            # Make a new move
                            current_move = (x, y, newX, y)

                            if debug_flag: debug_file.write(debug_modifer + ' Considering ' + str(current_move) + '\n')

                            # If it is a valid move
                            if func.is_valid_move(board, current_player, current_move):
                                current_heuristic = minimax(func.make_move(board, current_player, current_move), player,
                                                            depth, current_level + 1, alpha, beta, heuristic_method,
                                                            debug_flag, debug_file)

                                if current_level % 2 != 0:
                                    # Odd level, so maximize

                                    # Get max we have seen at this node and what we just saw
                                    if current_heuristic > best_heuristic:
                                        if debug_flag: debug_file.write(
                                            debug_modifer + str(current_move) + ' is better than ' + str(
                                                best_move) + f'({str(current_heuristic)} > {str(best_heuristic)})\n')
                                        best_move = current_move
                                        best_heuristic = current_heuristic

                                    # See if best we have seen at this node is better than alpha
                                    if best_heuristic > alpha:
                                        alpha = best_heuristic

                                    # If alpha >= beta, we can prune
                                    if alpha >= beta:
                                        if debug_flag: debug_file.write(
                                            debug_modifer + f'{alpha} >= {beta} PRUNING BRANCH\n')
                                        raise PruneBranch
                                else:
                                    # Even level, so minimize
                                    if current_heuristic < best_heuristic:
                                        if debug_flag: debug_file.write(
                                            debug_modifer + str(current_move) + ' is better than ' + str(
                                                best_move) + f'({str(current_heuristic)} < {str(best_heuristic)})\n')
                                        best_move = current_move
                                        best_heuristic = current_heuristic

                                    # See if worst we have seen at this node is worse than beta
                                    if best_heuristic < beta:
                                        beta = best_heuristic

                                    # If alpha >= beta, we can prune
                                    if alpha >= beta:
                                        if debug_flag: debug_file.write(
                                            debug_modifer + f'{alpha} >= {beta} PRUNING BRANCH\n')
                                        raise PruneBranch
                            else:
                                if debug_flag: debug_file.write(
                                    debug_modifer + str(current_move) + 'is not a valid move\n')
        except PruneBranch:
            # Used to jump out of all of the loops if we are pruning a branch
            pass

            # If we are propagating, return the best heuristic
        # If we are done propagating, return the best move we found
        if current_level == 1:
            if debug_flag: debug_file.write(
                debug_modifer + 'Best move: ' + str(best_move) + ' with Heuristic ' + str(best_heuristic) + '\n')
            return best_move

        else:
            if debug_flag: debug_file.write(
                debug_modifer + 'Best Heuristic at level ' + str(current_level) + ': ' + str(best_heuristic) + '\n')
            return best_heuristic
