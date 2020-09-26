import numpy as np

def write_file(gamestate):
    # Open gamestate file
    fhandle_write = open('gamestate.txt', 'w') 
    # Write current move gamestate to gamestate file
    for x in gamestate:
        writerow(x)
    fhandle_write.close() # close file

def read_file(gamestate):
    # Open gamestate file for reading
    with open('gamestate.txt') as fhandle_read:
        # Split lines and convert back to array for analysis
        gamestate = [line.split() for line in fhandle_read]
    fhandle_read.close() # close file


