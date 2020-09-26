import numpy as np

def write_file(gamestate):
    fhandle_write = open('gamestate.txt', 'w')
    for i in gamestate:
        writerow(i)

def read_file(gamestate):
    fhandle_read = open('gametate.txt', 'r')

