"""
    squeeze_it_GUI.py

    Description:
    This file creates a user interface for the game of Squeeze-it (Mak-Yek) and
    allows players to play against one another hotseat-style, play against the 
    minimax AI, or pit different minimax heuristics against one another
"""

import tkinter as tk
import minimax
import time
from copy import deepcopy
from functools import partial
import func
import heurisitcs

#Constants
GRID_HEIGHT = 8
GRID_WIDTH = 8
WC = 'W'
BC = 'B'
EC = ' '
BG_COLOR = "#FFEEE5"

HEURISTIC_OPTIONS_LIST = [
    ("Player Controlled", "player"),
    ("Simple Minimax", "simple"),
    ("Aggressive Minimax", "aggressive"),
    ("Defensive Minimax", "defensive"),
    ("Center Minimax", "stay_in_center"),
    ("Random Minimax", "random")
]

#GUI Globals
window = tk.Tk()
window.iconbitmap("images/squeezeit.ico")

white_variable = tk.StringVar()
black_variable = tk.StringVar()

black_circle = tk.PhotoImage(file = r"images/black_circle.png")
white_circle = tk.PhotoImage(file = r"images/white_circle.png")
empty_square = tk.PhotoImage(file = r"images/empty_square.png")

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
turn_count = 1
turn_time = 0
player_heuristics = dict([("W", "player"), ("B", "player")])
board_buttons = []
turn_label = ""
flavor_text = ""
board_button_funcs = []
start_game = False

"""*****************MAIN FUNCTIONS*********************"""

#printing the Game Grid
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

def countPieces(player):
    global grid
    counter = 0

    for x in range(0, 8, 1):
        for y in range(0, 8, 1):
            if grid[y][x] == player:
                counter += 1
    
    return counter

def game_over():
    global turn_count
    global grid

    if turn_count >= 50:
        return True
    elif countPieces("W") == 0:
        return True
    elif countPieces("B") == 0:
        return True
    return False

def update_GUI():
    global grid
    global board_buttons
    global current_player
    global cur_move
    global turn_count
    global turn_label
    global turn_time_label
    global turn_time

    for i in range(8):
        for j in range(8):
            board_buttons[i][j]["image"] = black_circle if grid[i][j] == "B" else white_circle if grid[i][j] == "W" else empty_square
            board_buttons[i][j]["bg"] = '#E4D2B6'
    if cur_move[current_player][0] != -1 and cur_move[current_player][1] != -1:
        board_buttons[cur_move[current_player][1]][cur_move[current_player][0]]["bg"] = 'yellow'
    
    turn_label["text"] = "Turn: " + str(turn_count) if not game_over() else "Game Over!"
    turn_time_label["text"] = "Time: " + str(turn_time)

    if not start_game:
        if turn_count <= 1:
            flavor_text["text"] = "Click to Start"
        else:
            white_score = heurisitcs.simple_heuristic(grid, "W")
            flavor_text["text"] = "White Wins!" if white_score > 0 else "Black Wins!" if white_score < 0 else "Its a Tie!"
    else:
        if current_player == "W":
            flavor_text["text"] = "White's Turn"
        else:
            flavor_text["text"] = "Black's Turn"

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
    global turn_time
    global turn_count
    global player_heuristics
    global start_game
    heuristic_runtime_file = open("heuristic_runtimes.csv", "a")

    if start_game and not game_over():
        #print("Turn : ", turn_count)
        #print("Current Player: ", player_heuristics[current_player], current_player)

        if player_heuristics[current_player] != "player":
            start_turn_time = int(round(time.time()*1000))
            grid = func.make_move(grid, current_player, minimax.get_next_move(grid, current_player, player_heuristics[current_player]))
            
            if current_player == "W":
                current_player = "B"
            else:
                current_player = "W"
            
            cur_turn_time = int(round(time.time()*1000))
            turn_time = cur_turn_time - start_turn_time
            heuristic_runtime_file.write(f"\"{player_heuristics[current_player]}\",\"{turn_time}\"\n")

            turn_count += 1
            #print_grid(grid)
        else:
            if cur_move[current_player][0] != -1 and cur_move[current_player][1] != -1 and cur_move[current_player][2] != -1 and cur_move[current_player][3] != -1:
                # We have a valid move to do
                start_turn_time = int(round(time.time()*1000))
                grid = func.make_move(grid, current_player, cur_move[current_player])

                cur_move[current_player] = (-1, -1, -1, -1)

                if current_player == "W":
                    current_player = "B"
                else:
                    current_player = "W"
                turn_count += 1
    elif turn_count > 1:
        start_game = False
    
    update_GUI()
    heuristic_runtime_file.close()
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

                if func.is_valid_move(grid, current_player, temp_move):
                    cur_move[current_player] = temp_move
                else:
                    cur_move[current_player] = (-1, -1, -1, -1)
        
        print(cur_move[current_player])


def play_game():
    global start_game
    start_game = True

def reset_game():
    global start_game
    global turn_count
    global current_player
    global cur_move
    global grid

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
    turn_count = 1
    start_game = False


"""***********************GAME GUI*****************************"""
window.title('Squeeze-It!')
window["bg"] = '#FFEEE5'

white_variable.set("player")
black_variable.set("player")

instructions = tk.Frame(master=window)

instructions_label = tk.Label(master=instructions, 
                              text="Choose an option from the following",
                              bg=BG_COLOR)
instructions_label.pack()

instructions.pack()

options_frame = tk.Frame(master=window,
                         bg=BG_COLOR)

white_options = tk.Frame(master=options_frame,
                         bg=BG_COLOR)
white_label = tk.Label(master=white_options, 
                       text="White Heuristic",
                       bg=BG_COLOR)
white_label.pack()
for heuristic in HEURISTIC_OPTIONS_LIST:
    tk.Radiobutton(master=white_options, 
                   text=heuristic[0], 
                   indicatoron=0, 
                   padx=20, 
                   width=20,
                   variable=white_variable, 
                   value=heuristic[1],
                   command=update_white_heuristic
    ).pack(anchor=tk.W)
white_options.grid(row=0, column=0)

black_options = tk.Frame(master=options_frame,
                         bg=BG_COLOR)
black_label = tk.Label(master=black_options, 
                       text="Black Heuristic",
                       bg=BG_COLOR)
black_label.pack()
for heuristic in HEURISTIC_OPTIONS_LIST:
    tk.Radiobutton(master=black_options, 
                   text=heuristic[0], 
                   indicatoron=0, 
                   padx=20, 
                   width=20,
                   variable=black_variable, 
                   value=heuristic[1],
                   command=update_black_heuristic
    ).pack(anchor=tk.W)
black_options.grid(row=0, column=1)

options_frame.pack()

play_game_frame = tk.Frame(master=window,
                           bg=BG_COLOR)

turn_label = tk.Label(master=play_game_frame, 
                      text="",
                      bg=BG_COLOR)
turn_label.pack()

turn_time_label = tk.Label(master=play_game_frame,
                           text="",
                           bg=BG_COLOR)
turn_time_label.pack()

flavor_text = tk.Label(master=play_game_frame, 
                       text="Click to Start",
                       bg=BG_COLOR)
flavor_text.pack()

play_game_button = tk.Button(master=play_game_frame, 
                             text="Play Game", 
                             command=play_game)
play_game_button.pack()

play_game_frame.pack()

game_board = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1,
    bg='#513B0E'
)

for i in range(0, 8, 1):
    board_buttons.append([])
    board_button_funcs.append([])

    for j in range(0, 8, 1):
        frame = tk.Frame(
            master=game_board,
            borderwidth=1,
            bg='#513B0E'
        )
        frame.grid(row=i, column=j)

        board_button_funcs[i].append(partial(resolve_button_click, i, j))

        board_buttons[i].append(tk.Button(master=frame, 
                                        text= 'B' if i == 0 else 'W' if i == 7 else ' ',
                                        borderwidth=1,
                                        image= black_circle if i == 0 else white_circle if i == 7 else empty_square,
                                        bg="#E4D2B6",
                                        command=board_button_funcs[i][j]
        ))
        board_buttons[i][j].pack()

game_board.pack()

reset_game_button = tk.Button(master=window, 
                       text="Reset Game",
                       borderwidth=1,
                       command=reset_game)
reset_game_button.pack()

window.after(50, move)

window.mainloop()
