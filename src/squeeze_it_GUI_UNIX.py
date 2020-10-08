"""
    squeeze_it_GUI.py

    Description:
    This file creates a user interface for the game of Squeeze-it (Mak-Yek) and
    allows players to play against one another hotseat-style, play against the 
    minimax AI, or pit different minimax heuristics against one another
"""

import tkinter as tk            # For GUI
import minimax                  # Minimax w/ ab-pruning implementation
import time                     # For getting the runtime of the minimax (minimax.py)
from copy import deepcopy       # For copying game states so they may be changed
from functools import partial   # For dynamically creating instances of function executions to be applied to the 8x8 grid of buttons so clicks on the buttons may be resolved
import func                     # Implementation of helper functions (func.py)
import heurisitcs               # Series of heuristics to be used by the minimax (heurisitcs.py)

"""****************CONSTANTS*********************"""
GRID_HEIGHT = 8
GRID_WIDTH = 8
WC = 'W'
BC = 'B'
EC = ' '
BG_COLOR = "#FFEEE5"

# List of heuristic options available to the user
# "player" implies the user will be making moves
HEURISTIC_OPTIONS_LIST = [
    ("Player Controlled", "player"),
    ("Simple Minimax", "simple"),
    ("Aggressive Minimax", "aggressive"),
    ("Defensive Minimax", "defensive"),
    ("Center Minimax", "stay_in_center")
]

#GUI Globals
window = tk.Tk()
window.iconbitmap("images\\squeezeit.ico")  # Add icon

# Tkinter variables for heuristic radio buttons
white_variable = tk.StringVar()
black_variable = tk.StringVar()

# Images to represent pieces on the board
black_circle = tk.PhotoImage(file = r"images/black_circle.png")
white_circle = tk.PhotoImage(file = r"images/white_circle.png")
empty_square = tk.PhotoImage(file = r"images/empty_square.png")

"""*********************GLOBALS**************************"""

# Current game state
grid = [
    [BC, BC, BC, BC, BC, BC, BC, BC ], 
    [EC, EC, EC, EC, EC, EC, EC, EC ], 
    [EC, EC, EC, EC, EC, EC, EC, EC ], 
    [EC, EC, EC, EC, EC, EC, EC, EC ], 
    [EC, EC, EC, EC, EC, EC, EC, EC ], 
    [EC, EC, EC, EC, EC, EC, EC, EC ], 
    [EC, EC, EC, EC, EC, EC, EC, EC ], 
    [WC, WC, WC, WC, WC, WC, WC, WC ]]

cur_move = dict([("W", (-1, -1, -1, -1)), ("B", (-1, -1, -1, -1))]) # Current move selected by W or B (only used by player heuristic)
current_player = 'W'                                                # Current player making a move
turn_count = 1                                                      # Turns elapsed 
turn_time = 0                                                       # How long it took for the turn to be made (not calculated for player)
player_heuristics = dict([("W", "player"), ("B", "player")])        # Chosen heuristic of W and B
board_buttons = []                                                  # Array for storing references to the board buttons on the GUI
turn_label = ""                                                     # Will be a tkinter label object that shows the current turn number
flavor_text = ""                                                    # Will be a tkinter label object that shows flavor text describing the game
board_button_funcs = []                                             # Array for storing partial functions that control the functionality of their respective button in board_buttons
start_game = False                                                  # Boolean indicating whether the game has started

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

# Count the number of pieces a player has on the board
def countPieces(player):
    global grid
    counter = 0

    for x in range(0, 8, 1):
        for y in range(0, 8, 1):
            if grid[y][x] == player:
                counter += 1
    
    return counter

# Check if the game is finished
def game_over():
    global turn_count
    global grid

    if turn_count > 100:
        return True
    elif countPieces("W") == 0:
        return True
    elif countPieces("B") == 0:
        return True
    return False

# Update all Tkinter objects with their respective internal values
def update_GUI():
    global grid
    global board_buttons
    global current_player
    global cur_move
    global turn_count
    global turn_label
    global turn_time_label
    global turn_time

    # Iterate through each board button and replace the image with an image that reflects the internal representation of the board
    for i in range(8):
        for j in range(8):
            board_buttons[i][j]["image"] = black_circle if grid[i][j] == "B" else white_circle if grid[i][j] == "W" else empty_square
            board_buttons[i][j]["bg"] = '#E4D2B6'
    
    # If the current player has selected a piece, lets highlight the piece
    if cur_move[current_player][0] != -1 and cur_move[current_player][1] != -1:
        board_buttons[cur_move[current_player][1]][cur_move[current_player][0]]["bg"] = 'yellow'
    
    # If the game is over, indicate such. Otherwise, show the turn count
    turn_label["text"] = "Turn: " + str(turn_count) if not game_over() else "Game Over!"

    # Show the time it took the last turn to complete
    turn_time_label["text"] = "Time: " + str(turn_time)

    # If we have not started the game, either we need to start it or it just finished
    if not start_game:
        if turn_count <= 1:
            # Need to start
            flavor_text["text"] = "Click to Start"
        else:
            # Just finished. Check who won.
            white_score = heurisitcs.simple_heuristic(grid, "W")
            flavor_text["text"] = "White Wins!" if white_score > 0 else "Black Wins!" if white_score < 0 else "Its a Tie!"
    else:
        # In the middle of a game, so lets see whose turn it is
        if current_player == "W":
            flavor_text["text"] = "White's Turn"
        else:
            flavor_text["text"] = "Black's Turn"

# Called when the white heuristic radio button is clicked
def update_white_heuristic():
    global player_heuristics

    player_heuristics["W"] = white_variable.get()

# Called when the black heuristic radio button is clicked
def update_black_heuristic():
    global player_heuristics

    player_heuristics["B"] = black_variable.get()

#Move function
def move():
    global grid
    global cur_move
    global current_player
    global turn_time
    global turn_count
    global player_heuristics
    global start_game

    # Open file to store runtimes
    heuristic_runtime_file = open("heuristic_runtimes.csv", "a")

    # See if we are in the middle of a game
    if start_game and not game_over():
        
        # See if we are dealing with a human player or an AI
        if player_heuristics[current_player] != "player":
            # AI, so get the next move with the minimax

            # Start timer
            start_turn_time = int(round(time.time()*1000))

            # Get the move
            grid = func.make_move(grid, current_player, minimax.get_next_move(grid, current_player, player_heuristics[current_player]))
            
            # Stop the timer
            cur_turn_time = int(round(time.time()*1000))

            # Calculate time elapsed
            turn_time = cur_turn_time - start_turn_time

            # Record the runtime in the output file
            heuristic_runtime_file.write(f"\"{player_heuristics[current_player]}\",\"{turn_time}\"\n")

            # Change player
            if current_player == "W":
                current_player = "B"
            else:
                current_player = "W"

            # Increment turn counter
            turn_count += 1
        else:
            # Dealing with a human, so lets see if they have provided a move
            if cur_move[current_player][0] != -1 and cur_move[current_player][1] != -1 and cur_move[current_player][2] != -1 and cur_move[current_player][3] != -1:
                # We have a valid move to do

                # Make move
                grid = func.make_move(grid, current_player, cur_move[current_player])

                # Reinitailize the move
                cur_move[current_player] = (-1, -1, -1, -1)

                # Change player
                if current_player == "W":
                    current_player = "B"
                else:
                    current_player = "W"
                
                # Increment turn counter
                turn_count += 1
    elif turn_count > 1:
        # Someone just won, so stop the game
        start_game = False
    
    # Update the GUI
    update_GUI()

    # Close the runtime file
    heuristic_runtime_file.close()

    # Schedule move() to run again in 50 milliseconds
    window.after(50, move)

# Sees what needs to be changed when the player clicks a button on the board
def resolve_button_click(i, j):
    global start_game

    # Ignore if the game has not started
    if start_game:
        global grid
        global player_heuristics
        global current_player
        global cur_move

        # Only care about clicks if the player is a human
        if player_heuristics[current_player] == "player":
            # Lets see what they clicked

            if cur_move[current_player][0] == -1 and cur_move[current_player][1] == -1 and grid[i][j] == current_player:
                # Player had not clicked anything yet but just clicked one of their own pieces
                cur_move[current_player] = (j, i, -1, -1)
            elif cur_move[current_player][0] != -1 and cur_move[current_player][1] != -1 and cur_move[current_player][2] == -1 and cur_move[current_player][3] == -1:
                # The player had already clicked one of their own pieces and just clicked another spot, so they want to make a move

                # Create the move they seem to want
                temp_move = (cur_move[current_player][0], cur_move[current_player][1], j, i)

                # See if the move is valid
                if func.is_valid_move(grid, current_player, temp_move):
                    # Valid move, so set their current move to the move we just tested. It will now by updated on the next execution of move()
                    cur_move[current_player] = temp_move
                else:
                    # Not a valid move, so reinitailize their current move and let them try again
                    cur_move[current_player] = (-1, -1, -1, -1)
        
        print(cur_move[current_player])

# Start the game
def play_game():
    global start_game
    start_game = True

# Reinitialize the internal components
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

# Set the title and color of the window
window.title('Squeeze-It!')
window["bg"] = '#FFEEE5'

# Initialize the heuristics of white and black
white_variable.set("player")
black_variable.set("player")

# Create a frame to house the instructions, put a label with the instructions inside, and pack
instructions = tk.Frame(master=window)
instructions_label = tk.Label(master=instructions, 
                              text="Choose an option from the following",
                              bg=BG_COLOR)
instructions_label.pack()
instructions.pack()

# Create a frame to house the heuristic radio buttons
options_frame = tk.Frame(master=window,
                         bg=BG_COLOR)

# Create a frame to house the white heuristic radio buttons and fill it with a packed label indicating such
white_options = tk.Frame(master=options_frame,
                         bg=BG_COLOR)
white_label = tk.Label(master=white_options, 
                       text="White Heuristic",
                       bg=BG_COLOR)
white_label.pack()

# Create a radio button for each possible heuristic and pack them
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

# Pack the white options into the options frame on a grid in the top left
white_options.grid(row=0, column=0)


# Create a frame to house the black heuristic radio buttons and fill it with a packed label indicating such
black_options = tk.Frame(master=options_frame,
                         bg=BG_COLOR)
black_label = tk.Label(master=black_options, 
                       text="Black Heuristic",
                       bg=BG_COLOR)
black_label.pack()

# Create a radio button for each possible heuristic and pack them
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
    
# Pack the black options into the options frame on a grid in the top right
black_options.grid(row=0, column=1)

# Pack the options
options_frame.pack()

# Create a frame to house the turn label, turn time, flavor text, and play game button.
# Pack them all
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

# Create a frame to house the game board
game_board = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1,
    bg='#513B0E'
)

# Create an 8x8 series of buttons organized on a grid that call
# resolve_button_click() when clicked, passing the coordinates of
# the click
for i in range(0, 8, 1):
    # Initialize array rows
    board_buttons.append([])
    board_button_funcs.append([])

    for j in range(0, 8, 1):
        # Create a frame for this button and pack it into game_board on a grid
        frame = tk.Frame(
            master=game_board,
            borderwidth=1,
            bg='#513B0E'
        )
        frame.grid(row=i, column=j)

        # Dynamically create a custom function call for this button and store it in the array
        board_button_funcs[i].append(partial(resolve_button_click, i, j))

        # Create the button and pack it into it's specified spot in the grid
        board_buttons[i].append(tk.Button(master=frame, 
                                        text= 'B' if i == 0 else 'W' if i == 7 else ' ',
                                        borderwidth=1,
                                        image= black_circle if i == 0 else white_circle if i == 7 else empty_square, # Initialize to starting state
                                        bg="#E4D2B6",
                                        command=board_button_funcs[i][j]    # Provided reference to created function call
        ))
        board_buttons[i][j].pack()
game_board.pack()

# Create a button to reset the game back to its initial state
reset_game_button = tk.Button(master=window, 
                       text="Reset Game",
                       borderwidth=1,
                       command=reset_game)
reset_game_button.pack()

# Schedule the move function to run
window.after(50, move)

# Start it all up
window.mainloop()
