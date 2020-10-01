import tkinter as tk
from enum import Enum
import re
import IO
import austin_minimax
import time
from copy import deepcopy
from functools import partial

#Constants
GRID_HEIGHT = 8
GRID_WIDTH = 8
WC = 'W'
BC = 'B'
EC = ' '


HEURISTIC_OPTIONS_LIST = [
    ("Player Controlled", "player"),
    ("Simple Minimax", "simple"),
    ("Aggressive Minimax", "aggressive"),
    ("Defensive Minimax", "defensive")
]

#GUI Globals
window = tk.Tk()

white_variable = tk.StringVar()
black_variable = tk.StringVar()

#Global
grid = [
    [BC, BC, BC, BC, BC, BC, BC, BC ], 
    [EC, EC, EC, EC, EC, EC, EC, EC ], 
    [EC, EC, EC, EC, EC, EC, EC, EC ], 
    [EC, EC, EC, EC, EC, EC, EC, EC ], 
    [EC, EC, EC, EC, EC, EC, EC, EC ], 
    [EC, EC, EC, EC, EC, EC, EC, EC ], 
    [EC, EC, EC, EC, EC, EC, EC, EC ], 
    [WC, WC, WC, WC, WC, WC, WC, WC ]]
cur_move = dict([("W", (-1, -1, -1, -1)), ("B", (-1, -1, -1, -1))])
current_player = 'W'
turn_count = 0
player_heuristics = dict([("W", "player"), ("B", "player")])
board_buttons = []
turn_label = ""
board_button_funcs = []
start_game = False

"""*****************MAIN FUNCTIONS*********************"""

#Printing the Game Grid
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
    
def make_move(board, player, move):
    ##print(player, f'({move[0]}, {move[1]}) to ({move[2]}, {move[3]})')
    newBoard = deepcopy(board)
    opponent = 'W' if player == 'B' else 'B'

    if is_valid_move(board, player, move):
        newBoard[move[1]][move[0]] = ' '
        newBoard[move[3]][move[2]] = player

        # Resolve any squeezes, prioritizing player GETTING SQUEEZED first
        for x in range(0, 8, 1):
            for y in range(0, 8, 1):
                if newBoard[y][x] == opponent:
                    # Check up
                    for up_space in range(0, y, 1):
                        if newBoard[up_space][x] == opponent:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(up_space+1, y, 1):
                                if newBoard[inter][x] != player:
                                    capture_flag = False
                            
                            if capture_flag:
                                # All pieces between these two pieces are opposite, so capture them
                                for inter in range(up_space+1, y, 1):
                                    #print(f'{player} lost piece at ({x}, {inter})')
                                    newBoard[inter][x] = ' '

                    # Check down
                    for down_space in range(y+1, 8, 1):
                        if newBoard[down_space][x] == opponent:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(y+1, down_space, 1):
                                if newBoard[inter][x] != player:
                                    capture_flag = False
                            
                            if capture_flag:
                                # All pieces between these two pieces are opposite, so capture them
                                for inter in range(y+1, down_space, 1):
                                    #print(f'{player} lost piece at ({x}, {inter})')
                                    newBoard[inter][x] = ' '
                    
                    # Check left
                    for left_space in range(0, x, 1):
                        if newBoard[y][left_space] == opponent:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(left_space+1, x, 1):
                                if newBoard[y][inter] != player:
                                    capture_flag = False
                            
                            if capture_flag:
                                # All pieces between these two pieces are opposite, so capture them
                                for inter in range(left_space+1, x, 1):
                                    #print(f'{player} lost piece at ({inter}, {y})')
                                    newBoard[y][inter] = ' '
                    # Check right
                    for right_space in range(x+1, 8, 1):
                        if newBoard[y][right_space] == opponent:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(x+1, right_space, 1):
                                if newBoard[y][inter] != player:
                                    capture_flag = False
                            
                            if capture_flag:
                                # All pieces between these two pieces are opposite, so capture them
                                for inter in range(x+1, right_space, 1):
                                    #print(f'{player} lost piece at ({inter}, {y})')
                                    newBoard[y][inter] = ' '
        
        for x in range(0, 8, 1):
            for y in range(0, 8, 1):
                if newBoard[y][x] == player:
                     # Check up
                    for up_space in range(0, y, 1):
                        if newBoard[up_space][x] == player:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(up_space+1, y, 1):
                                if newBoard[inter][x] != opponent:
                                    capture_flag = False
                            
                            if capture_flag:
                                # All pieces between these two pieces are opposite, so capture them
                                for inter in range(up_space+1, y, 1):
                                    #print(f'{opponent} lost piece at ({x}, {inter})')
                                    newBoard[inter][x] = ' '

                    # Check down
                    for down_space in range(y+1, 8, 1):
                        if newBoard[down_space][x] == player:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(y+1, down_space, 1):
                                if newBoard[inter][x] != opponent:
                                    capture_flag = False
                            
                            if capture_flag:
                                # All pieces between these two pieces are opposite, so capture them
                                for inter in range(y+1, down_space, 1):
                                    #print(f'{opponent} lost piece at ({x}, {inter})')
                                    newBoard[inter][x] = ' '
                    
                    # Check left
                    for left_space in range(0, x, 1):
                        if newBoard[y][left_space] == player:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(left_space+1, x, 1):
                                if newBoard[y][inter] != opponent:
                                    capture_flag = False
                            
                            if capture_flag:
                                # All pieces between these two pieces are opposite, so capture them
                                for inter in range(left_space+1, x, 1):
                                    #print(f'{opponent} lost piece at ({inter}, {y})')
                                    newBoard[y][inter] = ' '
                    # Check right
                    for right_space in range(x+1, 8, 1):
                        if newBoard[y][right_space] == player:
                            # See if we have a series of opposite pieces between these two pieces
                            capture_flag = True
                            for inter in range(x+1, right_space, 1):
                                if newBoard[y][inter] != opponent:
                                    capture_flag = False
                            
                            if capture_flag:
                                # All pieces between these two pieces are opposite, so capture them
                                for inter in range(x+1, right_space, 1):
                                    #print(f'{opponent} lost piece at ({inter}, {y})')
                                    newBoard[y][inter] = ' '

    return newBoard

# Checks move legality and updates grid
def is_valid_move(board, player, move):
    ##print(board),
    ##print(player)
    ##print(move)

    pieceX = move[0]
    pieceY = move[1]
    new_locX = move[2]
    new_locY = move[3]

    if board[pieceY][pieceX] != player:
        # Chosen piece does not belong to the player or is not there, so invalid
        ##print('Not Player Piece')
        return False
    elif pieceX == new_locX and pieceY == new_locY:
        # Not moving the piece, so invalid
        ##print('Not Moving')
        return False
    elif pieceX == new_locX:
        # Moving Up or down

        # Look up or down to make sure no pieces between the piece and its new location
        if pieceY > new_locY:
            # Moving Up
            ##print('Moving Up')
            for loc in board[new_locY:pieceY]:
                if loc[pieceX] != ' ':
                    ##print('Piece In Way')
                    return False
            return True
        else:
            # Moving down
            ##print('Moving Down')
            for loc in board[pieceY+1:new_locY+1]:
                if loc[pieceX] != ' ':
                    ##print('Piece In Way')
                    return False
            return True
    elif pieceY == new_locY:
        # Moving left or right

        # Look left or right to make sure no pieces between the piece and its new location
        if pieceX > new_locX:
            # Moving left
            ##print('Moving Left')
            for loc in board[pieceY][new_locX:pieceX]:
                if loc != ' ':
                    ##print('Piece In Way')
                    return False
            return True
        else:
            # Moving right
            ##print('Moving Right')
            for loc in board[pieceY][pieceX+1:new_locX+1]:
                if loc != ' ':
                    ##print('Piece In Way')
                    return False
            return True
    else:
        # Piece is not moving in a straight line, so invalid
        ##print('Not moving in a straight line')
        return False

def game_over():
    global turn_count

    return turn_count >= 50

def update_GUI():
    global grid
    global board_buttons
    global current_player
    global cur_move
    global turn_count
    global turn_label

    for i in range(8):
        for j in range(8):
            board_buttons[i][j]["text"] = grid[i][j]
            #board_buttons[i][j]["bg"] = 'blue'
            print(cur_move[current_player])
    #if cur_move[current_player][0] != -1 and cur_move[current_player][1] != -1:
        #board_buttons[cur_move[current_player][1]][cur_move[current_player][0]]["bg"] = 'yellow'
    
    turn_label["text"] = "Turn: " + str(turn_count) if not game_over() else "Game Over!"

def update_white_heuristic():
    global player_heuristics

    player_heuristics["W"] = white_variable.get()
    #print(f"White Heuristic: {player_heuristics["W"]}")

def update_black_heuristic():
    global player_heuristics

    player_heuristics["B"] = black_variable.get()
    #print(f"Black Heuristic: {player_heuristics["B"]}")

#Move function
def move():
    global grid
    global cur_move
    global current_player
    global turn_count
    global player_heuristics

    if start_game and not game_over():
        #print("Turn : ", turn_count)
        #print("Current Player: ", player_heuristics[current_player], current_player)
        
        if player_heuristics[current_player] != "player":
            grid = make_move(grid, current_player, austin_minimax.get_next_move(grid, current_player, player_heuristics[current_player]))
            
            if current_player == "W":
                current_player = "B"
            else:
                current_player = "W"
            
            turn_count += 1
            print_grid(grid)

            update_GUI()
        else:
            if cur_move[current_player][0] != -1 and cur_move[current_player][1] != -1 and cur_move[current_player][2] != -1 and cur_move[current_player][3] != -1:
                # We have a valid move to do
                grid = make_move(grid, current_player, cur_move[current_player])
                update_GUI()

                cur_move[current_player] = (-1, -1, -1, -1)

                if current_player == "W":
                    current_player = "B"
                else:
                    current_player = "W"

        

    window.after(50, move)

def resolve_button_click(i, j):
    global start_game

    if start_game:
        global grid
        global player_heuristics
        global current_player
        global cur_move

        if player_heuristics[current_player] == "player":
            if cur_move[current_player][0] == -1 and cur_move[current_player][1] == -1 and grid[i][j] == current_player:
                # Player has not clicked anything yet but just clicked one of their own pieces
                cur_move[current_player] = (j, i, -1, -1)
            elif cur_move[current_player][0] != -1 and cur_move[current_player][1] != -1 and cur_move[current_player][2] == -1 and cur_move[current_player][3] == -1:
                temp_move = (cur_move[current_player][0], cur_move[current_player][1], j, i)

                if is_valid_move(grid, current_player, temp_move):
                    cur_move[current_player] = temp_move
                else:
                    cur_move[current_player] = (-1, -1, -1, -1)
        
        print(cur_move[current_player])

def play_game():
    global start_game
    start_game = True

"""***********************GAME GUI*****************************"""
window.title('Squeeze-It!')

white_variable.set("player")
black_variable.set("player")

instructions = tk.Frame(master=window)

instructions_label = tk.Label(master=instructions, text="Choose an option from the following")
instructions_label.pack()

instructions.pack()

options_frame = tk.Frame(master=window)

white_options = tk.Frame(master=options_frame)
white_label = tk.Label(master=white_options, text="White Heuristic")
white_label.pack()
for heuristic in HEURISTIC_OPTIONS_LIST:
    tk.Radiobutton(master=white_options, 
                   text=heuristic[0], 
                   indicatoron=0, 
                   padx=20, 
                   variable=white_variable, 
                   value=heuristic[1],
                   command=update_white_heuristic
    ).pack(anchor=tk.W)
white_options.grid(row=0, column=0)

black_options = tk.Frame(master=options_frame)
black_label = tk.Label(master=black_options, text="Black Heuristic")
black_label.pack()
for heuristic in HEURISTIC_OPTIONS_LIST:
    tk.Radiobutton(master=black_options, 
                   text=heuristic[0], 
                   indicatoron=0, 
                   padx=20, 
                   variable=black_variable, 
                   value=heuristic[1],
                   command=update_black_heuristic
    ).pack(anchor=tk.W)
black_options.grid(row=0, column=1)

options_frame.pack()

play_game_frame = tk.Frame(master=window)

turn_label = tk.Label(master=play_game_frame, text="Click to Start")
turn_label.pack()

play_game_button = tk.Button(master=play_game_frame, text="Play Game", command=play_game)
play_game_button.pack()

play_game_frame.pack()

game_board = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1
)

for i in range(0, 8, 1):
    board_buttons.append([])
    board_button_funcs.append([])

    for j in range(0, 8, 1):
        frame = tk.Frame(
            master=game_board,
            borderwidth=1
        )
        frame.grid(row=i, column=j, padx=5, pady=5)

        board_button_funcs[i].append(partial(resolve_button_click, i, j))

        board_buttons[i].append(tk.Button(master=frame, 
                                        text= 'B' if i == 0 else 'W' if i == 7 else ' ',
                                        borderwidth=1,
                                        command=board_button_funcs[i][j]
        ))
        board_buttons[i][j].pack()

game_board.pack()

window.after(1000, move)

window.mainloop()