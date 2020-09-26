import numpy as np

def write_file(gamestate):
    fhandle_write = open('gamestate.txt', 'w')
    for x in gamestate:
        writerow(x)
    fhandle_write.close()

def read_file(gamestate):
    with open('gamestate.txt') as fhandle_read:
        gamestate = [line.split() for line in fhandle_read]
    fhandle_read.close()


