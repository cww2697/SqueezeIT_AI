import random

def simple_heuristic(board, player):
    counter = 0
    opponent = 'W' if player == 'B' else 'B'

    for x in range(0, 8, 1):
        for y in range(0, 8, 1):
            if board[y][x] == player:
                counter += 1
    
    for x in range(0, 8, 1):
        for y in range(0, 8, 1):
            if board[y][x] == opponent:
                counter -= 1

    return counter

# Defensive heuristic
# Encourages diagonals
# Discourages single spaces in between pieces and multiple pieces next to each other


def defensive_heuristic(board, player):
    counter = simple_heuristic(board, player)
    opponent = 'W' if player == 'B' else 'B'

    for x in range(0, 6, 1):
        for y in range(0, 8 , 1):
            if board[y][x] == player and board[y][x] == board[y][x+2]:
                counter -= 1
    for x in range(0, 7, 1):
        for y in range(0, 8 , 1):
            if board[y][x] == player and board[y][x] == board[y][x+1]:
                counter -= 1
    for x in range(0,8, 1):
        for y in range(0, 7 , 1):
            if board[y][x] == player and board[y][x] == board[y+1][x]:
                counter -= 1
    for x in range(0,8, 1):
        for y in range(0, 6 , 1):
            if board[y][x] == player and board[y][x] == board[y+2][x]:
                counter -= 1
    for x in range(0,7, 1):
        for y in range(0, 7, 1):
            if board[y][x] == player and board[y][x] == board[y+1][x+1]:
                counter += 1
    
    return counter

# Aggressive Heuristic
# Encourages trades
# Encourages being close to opponent
def aggressive_heuristic(board, player):
    #counter = check_repeat_state(board)
    counter = 0
    opponent = 'W' if player == 'B' else 'B'

    for x in range(0, 8, 1):
        for y in range(0, 8, 1):
            if board[y][x] == player:
                counter += 2
    
    for x in range(0, 8, 1):
        for y in range(0, 8, 1):
            if board[y][x] == opponent:
                counter -= 1

    for x in range(0, 7, 1):
        for y in range(0, 8 , 1):
            if board[y][x] == player and board[y][x+1] == opponent:
                counter += 1
    for x in range(1, 8, 1):
        for y in range(0, 8 , 1):
            if board[y][x] == player and board[y][x-1] == opponent:
                counter += 1
    for x in range(0,8, 1):
        for y in range(0, 7, 1):
            if board[y][x] == player and board[y+1][x] == opponent:
                counter += 1
    for x in range(0,8, 1):
        for y in range(1, 8, 1):
            if board[y][x] == player and board[y-1][x] == opponent:
                counter += 1

    return counter

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