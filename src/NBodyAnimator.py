import sys
from NBodySimulation import NBodySimulation

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

BRUTE_FORCE = NBodySimulation(100)
