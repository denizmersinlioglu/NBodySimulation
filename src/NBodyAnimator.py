from NBodySimulation import NBodySimulation
from tkinter import Tk
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

brute_force = NBodySimulation(100)
