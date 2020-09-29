

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