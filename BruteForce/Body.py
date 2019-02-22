import math


class Body:
    G = 6.673e-11
    solarmass = 1.98892e30

    # create and initialize a new Body
    def __init__(self, rx, ry, vx, vy,  mass, color):
        self.rx = rx        # holds the cartesian X position
        self.ry = ry        # holds the cartesian Y position
        self.vx = vx        # velocity component X
        self.vy = vy        # velocity component Y
        self.mass = mass    # color (for fun)
        self.fx = 0         # force component X
        self.fy = 0         # force component Y
        self.color = color  # Color for Fun

    # update the velocity and position using a timestep dt
    def update(self, dt):
        self.vx += dt * self.fx / self.mass
        self.vy += dt * self.fy / self.mass
        self.rx += dt * self.vx
        self.ry += dt * self.vy

    # returns the distance between two bodies
    def distanceTo(self, body):
        dx = self.rx - body.rx
        dy = self.ry - body.ry
        return math.sqrt(dx*dx + dy*dy)

    # set the force to 0 for the next iteration
    def resetForce(self):
        self.fx = 0.0
        self.fy = 0.0

    # compute the net force acting between the body a and b, and
    # add to the net force acting on a
    def addForce(self, body):
        EPS = 3E4     # softening parameter (just to avoid infinities)
        dx = body.rx - self.rx
        dy = body.ry - self.ry
        dist = math.sqrt(dx*dx + dy*dy)
        F = (self.G * self.mass * body.mass) / (dist*dist + EPS*EPS)
        self.fx += F * dx / dist
        self.fy += F * dy / dist

    # convert to string representation formatted nicely
    def toString(self):
        return str(self.rx) + ", " \
            + str(self.ry) + ", " \
            + str(self.vx) + ", " \
            + str(self.vy) + ", " \
            + str(self.mass) + "\n"
