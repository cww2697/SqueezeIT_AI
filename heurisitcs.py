

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

    for x in range(0,8, 1):
        for y in range(0, 8 , 1):
            if board[y][x] == board[y][x+2]:
                counter -= 1
    for x in range(0,8, 1):
        for y in range(0, 8 , 1):
            if board[y][x] == board[y][x+1]:
                counter -= 1
    for x in range(0,8, 1):
        for y in range(0, 8 , 1):
            if board[y][x] == board[y+1][x]:
                counter -= 1
    for x in range(0,8, 1):
        for y in range(0, 8 , 1):
            if board[y][x] == board[y+2][x]:
                counter -= 1
    for x in range(0,8, 1):
        for y in range(0, 8 , 1):
            if board[y][x] == board[y+1][x+1]:
                counter += 1

def aggressive_heuristic(board, player):
    counter = simple_heuristic(board, player)
    opponent = 'W' if player == 'B' else 'B'