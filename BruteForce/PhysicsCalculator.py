import random
import math

solar_mass = 1.98892e30
gravitational_constant = 6.67e-11


def circlev(rx, ry):
    r2 = math.sqrt(rx*rx+ry*ry)
    numerator = gravitational_constant*1e6*solar_mass
    return math.sqrt(numerator/r2)


def total_energies(bodies):
    iteration_range = range(0, len(bodies))
    kinetic_energy = 0
    potential_energy = 0
    for i in iteration_range:
        velocity_square = math.pow(bodies[i].vx, 2) + math.pow(bodies[i].vy, 2)
        kinetic_energy += 0.5 * bodies[i].mass * velocity_square
        for j in iteration_range:
            if j != i:
                potential_energy = 0.5 * bodies[i].potantial_energy(bodies[j])
            else:
                continue
    return (kinetic_energy, potential_energy)


def velociy_cm(bodies):
    iteration_range = range(0, len(bodies))
    total_mass = 0
    total_mvx = 0
    total_mvy = 0
    for i in iteration_range:
        total_mass += bodies[i].mass
        total_mvx += bodies[i].mass * bodies[i].vx
        total_mvy += bodies[i].mass * bodies[i].vy
    return (total_mvx/total_mass, total_mvy/total_mass)


def position_cm(bodies):
    iteration_range = range(0, len(bodies))
    total_mass = 0
    total_mrx = 0
    total_mry = 0
    for i in iteration_range:
        total_mass += bodies[i].mass
        total_mrx += bodies[i].mass * bodies[i].rx
        total_mry += bodies[i].mass * bodies[i].ry
    return (total_mrx/total_mass, total_mry/total_mass)
