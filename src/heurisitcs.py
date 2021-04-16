import random


# Just counts up the pieces and rates the board based on
# who has more (i.e., encourages capturing of opponent and
# avoiding being captured by opponent)
def simple_heuristic(board, player):
    counter = 0
    opponent = 'W' if player == 'B' else 'B'

    for x in range(0, 8, 1):
        for y in range(0, 8, 1):
            if board[y][x] == player:
                counter += 5

    for x in range(0, 8, 1):
        for y in range(0, 8, 1):
            if board[y][x] == opponent:
                counter -= 5

    return counter


# Defensive heuristic
# Encourages diagonals
# Discourages single spaces in between pieces and multiple pieces next to each other
# Encourages staying on the edge
def defensive_heuristic(board, player):
    counter = simple_heuristic(board, player)
    opponent = 'W' if player == 'B' else 'B'

    for x in range(0, 6, 1):
        for y in range(0, 8, 1):
            # Encourage player not to leave space between two pieces
            if board[y][x] == player and board[y][x] == board[y][x + 2]:
                counter -= 1

    for x in range(0, 7, 1):
        for y in range(0, 8, 1):
            # Encourage upper and lower edges
            if board[y][0] == player:
                counter += 1
            if board[y][7] == player:
                counter += 1

            # Encourage player not to put pieces right next to each other
            if board[y][x] == player and board[y][x] == board[y][x + 1]:
                counter -= 1
    for x in range(0, 8, 1):
        # Encourage left and right edges
        if board[0][x] == player:
            counter += 1
        if board[7][x] == player:
            counter += 1

        for y in range(0, 7, 1):
            # Encourage player not to put pieces right next to each other
            if board[y][x] == player and board[y][x] == board[y + 1][x]:
                counter -= 1
    for x in range(0, 8, 1):
        for y in range(0, 6, 1):
            # Encourage player not to leave a space between two pieces
            if board[y][x] == player and board[y][x] == board[y + 2][x]:
                counter -= 1
    for x in range(0, 7, 1):
        for y in range(0, 7, 1):
            # Encourage diagonals as they defend very well
            if board[y][x] == player and board[y][x] == board[y + 1][x + 1]:
                counter += 1

    return counter


# Aggressive Heuristic
# Encourages trades
# Encourages being close to opponent
def aggressive_heuristic(board, player):
    base_counter = defensive_heuristic(board, player)
    simple_counter = simple_heuristic(board, player)
    counter = 0
    opponent = 'W' if player == 'B' else 'B'

    for x in range(0, 8, 1):
        for y in range(0, 8, 1):
            if board[y][x] == player:
                # Higher counter for taking pieces encourages trades
                counter += 8

    for x in range(0, 8, 1):
        for y in range(0, 8, 1):
            if board[y][x] == opponent:
                counter -= 5

    for x in range(0, 7, 1):
        for y in range(0, 8, 1):
            # Encourage being next to the opponent
            if board[y][x] == player and board[y][x + 1] == opponent:
                counter += 1
    for x in range(1, 8, 1):
        for y in range(0, 8, 1):
            # Encourage being next to the opponent
            if board[y][x] == player and board[y][x - 1] == opponent:
                counter += 1
    for x in range(0, 8, 1):
        for y in range(0, 7, 1):
            # Encourage being next to the opponent
            if board[y][x] == player and board[y + 1][x] == opponent:
                counter += 1
    for x in range(0, 8, 1):
        for y in range(1, 8, 1):
            # Encourage being next to the opponent
            if board[y][x] == player and board[y - 1][x] == opponent:
                counter += 1
    if base_counter > counter:
        return base_counter
    elif base_counter < counter:
        return counter
    else:
        return simple_counter


# Randomly picks an above heuristic. This heuristic is very
# bad for quite a few reasons, but is fun to play against
def random_heuristic(board, player):
    choice = random.randrange(0, 3, 1)

    if choice == 0:
        return simple_heuristic(board, player)
    elif choice == 1:
        return aggressive_heuristic(board, player)
    elif choice == 2:
        return defensive_heuristic(board, player)
    else:
        print(choice)


def stay_in_the_center_heuristic(board, player):
    counter = simple_heuristic(board, player)

    for x in range(2, 6, 1):
        for y in range(2, 6, 1):
            if board[y][x] == player:
                counter += 1
    return counter
