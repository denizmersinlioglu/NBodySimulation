from BruteForce import BruteForce
from tkinter import Tk
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

master = Tk()
brute_force = BruteForce(master, 100)
