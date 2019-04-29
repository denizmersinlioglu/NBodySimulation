import math

GRAVITY_CONST = 6.673e-11
SOLAR_MASS = 1.98892e30


class Body:

    # create and initialize a new Body
    def __init__(self, rx, ry, vx, vy,  mass, color):
        self.rx = rx        # holds the cartesian X position
        self.ry = ry        # holds the cartesian Y position
        self._rx = 0        # X position for Verlet Algorithm
        self._ry = 0        # Y position for Verlet Algorithm
        self.vx = vx        # velocity component X
        self.vy = vy        # velocity component Y
        self.mass = mass    # color (for fun)
        self.fx = 0         # force component X
        self.fy = 0         # force component Y
        self.color = color  # Color for Fun
        self.isVerletInitialized = False

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
    def distance_to(self, body):
        dx = self.rx - body.rx
        dy = self.ry - body.ry
        return math.sqrt(dx*dx + dy*dy)

    # set the force to 0 for the next iteration
    def reset_force(self):
        self.fx = 0.0
        self.fy = 0.0

    def run_first_verlet_loop(self, dt):
        self._rx = self.rx
        self._ry = self.ry
        self.rx += self.vx*dt + (0.5 * (dt**2) * self.fx / self.mass)
        self.ry += self.vy*dt + (0.5 * (dt**2) * self.fy / self.mass)

    def update_verlet(self, dt):
        if not self.isVerletInitialized:
            self.run_first_verlet_loop(dt)
            self.isVerletInitialized = True

        rx_new = (2 * self.rx) - self._rx + ((dt**2) * self.fx / self.mass)
        ry_new = (2 * self.ry) - self._ry + ((dt**2) * self.fy / self.mass)
        self._rx = self.rx
        self._ry = self.ry
        self.rx = rx_new
        self.ry = ry_new

    def add_force(self, body):
        EPS = 3E4
        dx = body.rx - self.rx
        dy = body.ry - self.ry
        dist = math.sqrt(dx*dx + dy*dy)
        F = GRAVITY_CONST * self.mass * body.mass / (dist**2 + EPS**2)
        self.fx += F * dx / dist
        self.fy += F * dy / dist

    def velocity(self):
        velocity_square = self.vx**2 + self.vy**2
        return math.sqrt(velocity_square)

    def radius(self):
        rx_square = self.rx**2
        ry_square = self.ry**2
        return math.sqrt(rx_square + ry_square)

    def potantial_energy(self, body):
        distance = abs(self.distance_to(body))
        numerator = GRAVITY_CONST * self.mass * body.mass
        return -numerator/distance

    def kinetic_energy(self):
        velocity_square = math.pow(self.vx, 2) + math.pow(self.vy, 2)
        return 0.5 * self.mass * velocity_square

    def inside(self, quad):
        return quad.contains(self.rx, self.ry)

    def add(self, body):
        total_mass = self.mass + body.mass
        rx_center = (self.rx * self.mass + body.rx * body.mass) / total_mass
        ry_center = (self.ry * self.mass + body.ry * body.mass) / total_mass
        vx_center = (self.vx * self.mass + body.vx * body.mass) / total_mass
        vy_center = (self.vy * self.mass + body.vy * body.mass) / total_mass
        return Body(rx_center, ry_center, vx_center, vy_center, total_mass, self.color)

    # convert to string representation formatted nicely
    def to_string(self):
        return str(self.rx) + ", " \
            + str(self.ry) + ", " \
            + str(self.vx) + ", " \
            + str(self.vy) + ", " \
            + str(self.mass)
