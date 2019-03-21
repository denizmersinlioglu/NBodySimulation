import time
import datetime
import math
import random

solar_mass = 1.98892e30
G = 6.67e-11


def circlev(rx, ry):
    r2 = math.sqrt(rx*rx+ry*ry)
    numerator = G*1e6*solar_mass
    return math.sqrt(numerator/r2)


def total_energies(bodies):
    kinetic_energy = 0
    potential_energy = 0
    for body in bodies:
        velocity_square = math.pow(body.vx, 2) + math.pow(body.vy, 2)
        kinetic_energy += 0.5 * body.mass * velocity_square
        for other in bodies:
            if body is other:
                continue
            potential_energy = 0.5 * body.potantial_energy(other)
    return (kinetic_energy, potential_energy)


def velociy_cm(bodies):
    total_mass = 0
    total_mvx = 0
    total_mvy = 0
    for body in bodies:
        total_mass += body.mass
        total_mvx += body.mass * body.vx
        total_mvy += body.mass * body.vy
    return (total_mvx/total_mass, total_mvy/total_mass)


def position_cm(bodies):
    total_mass = 0
    total_mrx = 0
    total_mry = 0
    for body in bodies:
        total_mass += body.mass
        total_mrx += body.mass * body.rx
        total_mry += body.mass * body.ry
    return (total_mrx/total_mass, total_mry/total_mass)


def millis():
    return int(round(time.time() * 1000))


def exp(value):
    return -math.log(1 - random.random()) / value


def signum(int):
    if(int < 0):
        return -1
    elif(int > 0):
        return 1
    else:
        return int
