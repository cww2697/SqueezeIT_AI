from enum import Enum
import re

# Constants
GRID_HEIGHT = 8
GRID_WIDTH = 8
WC = 'W'
BC = 'B'
# Should we change to 0?
EC = ' '
PLAYERS = Enum("Players", "White Black")


# Printing the Game Grid
def print_grid(grid):
    """This function is drawing the grid"""
    print("       A   B   C   D   E   F   G   H\n")
    for i in range(GRID_HEIGHT):
        print(i, "   |", end=" ")
        for j in range(GRID_WIDTH):
            current_cell = grid[i][j]
            print(current_cell + " |", end=" ")
        print("")
    print("")


# Forming the Game Grid
def form_grid():
    global grid
    grid = [[BC, BC, BC, BC, BC, BC, BC, BC],
            [EC, EC, EC, EC, EC, EC, EC, EC],
            [EC, EC, EC, EC, EC, EC, EC, EC],
            [EC, EC, EC, EC, EC, EC, EC, EC],
            [EC, EC, EC, EC, EC, EC, EC, EC],
            [EC, EC, EC, EC, EC, EC, EC, EC],
            [EC, EC, EC, EC, EC, EC, EC, EC],
            [WC, WC, WC, WC, WC, WC, WC, WC]]

    return grid


# Move function
def move(value_package):
    print("Turn : ", value_package["turn_count"])
    if value_package["cur_turn"] == PLAYERS.White:
        print("White's turn :\n")
        print_grid(value_package["board"])

        # Ask for command until the syntax is correct
        while True:
            print("Enter movement :", end="")
            if interpret_response(value_package["board"], input()) == True:
                value_package["cur_turn"] = PLAYERS.Black
                value_package["turn_count"] += 1
                break
    else:
        print("Black's turn :\n")
        print_grid(value_package["board"])

        # WHERE AI FUNCTION FOR BLACK'S TURN

        value_package["cur_turn"] = PLAYERS.White


# Turns the move into a tuple and sees if syntax is valid and if move is legal
def interpret_response(board, response):
    if check_input_syntax(response):
        tuples = response_to_tuples(response)
        if check_move_legality(board, tuples):
            return True
    else:
        print("Syntax Error")
    return False


# RegEx to determine if move syntax is valid
def check_input_syntax(response):
    return re.match("^([0-9][A-J]){2}$", response)


# Turns input to tuples
def response_to_tuples(response):
    match = re.findall("([0-9][A-J]){1}", response)
    # -65 because ASCII A-Z to integers (remember A == 0 ...)
    # -48 because ASCII 1-9 to integers (remember 0 == 0 ...)
    l_val1 = ord(match[0][0]) - 48
    r_val1 = ord(match[0][1]) - 65
    l_val2 = ord(match[1][0]) - 48
    r_val2 = ord(match[1][1]) - 65
    return ((l_val1, r_val1), (l_val2, r_val2))


# Checks move legality and updates grid
def check_move_legality(board, tuples):
    fr = tuples[0]
    to = tuples[1]

    if grid[fr[0]][fr[1]] == 'W':
        if fr[0] == to[0] or fr[1] == to[1]:
            if grid[to[0]][to[1]] == ' ':
                grid[to[0]][to[1]] = 'W'
                grid[fr[0]][fr[1]] = ' '
                return True
            else:
                print('Space is not empty')
        else:
            print('Illegal Move')

    else:
        print('Illegal Move')
        return False


# Game interface
def main():
    print('SQUEEZE IT')
    value_package = dict([("board", form_grid()), ("turn_count", 1), ("cur_turn", PLAYERS.White)])
    while True:
        move(value_package)


main()
