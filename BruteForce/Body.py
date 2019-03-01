import math

gravitational_constant = 6.67e-11


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

    def scale_cm_velocity(self, velocity_cmx, velocity_cmy):
        self.vx = self.vx - velocity_cmx
        self.vy = self.vy - velocity_cmy

    def scale_cm_position(self, position_cmx, position_cmy):
        self.rx = self.rx - position_cmx
        self.ry = self.ry - position_cmy

    def scale_velocity(self, scale_factor):
        self.vx = self.vx * scale_factor
        self.vy = self.vy * scale_factor

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

    def velocity(self):
        velocity_square = math.pow(self.vx, 2) + math.pow(self.vy, 2)
        return math.sqrt(velocity_square)

    def radius(self):
        rx_square = math.pow(self.rx, 2)
        ry_square = math.pow(self.ry, 2)
        return math.sqrt(rx_square + ry_square)

    def potantial_energy(self, body):
        distance = abs(body.radius() - self.radius())
        numerator = gravitational_constant * self.mass * body.mass
        return numerator/distance

    def kinetic_energy(self):
        velocity_square = math.pow(self.vx, 2) + math.pow(self.vy, 2)
        return 0.5 * self.mass * velocity_square

    # convert to string representation formatted nicely
    def toString(self):
        return str(self.rx) + ", " \
            + str(self.ry) + ", " \
            + str(self.vx) + ", " \
            + str(self.vy) + ", " \
            + str(self.mass)
