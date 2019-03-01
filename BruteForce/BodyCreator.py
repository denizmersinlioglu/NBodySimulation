from PhysicsCalculator import *
from Body import Body
from Utils import *
import math
import random


def create_linear_bodies(N):
    bodies = [Body] * N
    for i in range(0, N):
        random_x = 1e18*exp(-1.8)*(.5-random.random())
        random_y = 1e18*exp(-1.8)*(.5-random.random())
        vx = 1e3 if random.random() <= .5 else -1e3
        vy = 1e3 if random.random() <= .5 else -1e3
        mass = random.random()*solar_mass*10+1e20
        red = int(math.floor(mass*254/(solar_mass*10+1e20)))
        blue = int(math.floor(mass*254/(solar_mass*10+1e20)))
        green = 255
        colorval = "#%02x%02x%02x" % (red, green, blue)
        bodies[i] = Body(random_x, random_y, vx, vy, mass, colorval)

    (kinetic_energy, potential_energy) = total_energies(bodies)
    scale_factor = math.sqrt(potential_energy/(2*kinetic_energy))
    for i in range(0, N):
        bodies[i].scale_velocity(scale_factor)
    return bodies


def create_circular_bodies(N):
    bodies = [Body] * N
    for i in range(0, N):
        random_x = 1e18*exp(-1.8)*(.5-random.random())
        random_y = 1e18*exp(-1.8)*(.5-random.random())
        mag_v = circlev(random_x, random_y)
        abs_angle = math.atan(abs(random_y/random_x))
        theta_v = math.pi/2-abs_angle
        vx = -1*signum(random_y)*math.cos(theta_v)*mag_v
        vy = signum(random_x)*math.sin(theta_v)*mag_v

        if random.random() <= .5:
            vx = -vx
            vy = -vy

        mass = random.random()*solar_mass*10+1e20
        red = int(math.floor(mass*254/(solar_mass*10+1e20)))
        blue = int(math.floor(mass*254/(solar_mass*10+1e20)))
        green = 255

        colorval = "#%02x%02x%02x" % (red, green, blue)
        bodies[i] = Body(random_x, random_y, vx, vy, mass, colorval)

    # put a heavy body in the center
    bodies[0] = Body(0, 0, 0, 0, 1e6*solar_mass, "red")
