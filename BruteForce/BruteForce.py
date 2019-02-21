from tkinter import *
import random
import time
import math
from Body import Body


class BruteForce:
    def __init__(self, master, N):
        self.master = master
        self.canvas = Canvas(master)
        if N > 1000:
            self.N = 1000
        else:
            self.N = N
        self.bodies = []
        self.should_run = False

        self.setup_menu()
        self.setup_canvas()

        self.start_the_bodies(self.N)
        self.draw()

    def setup_menu(self):
        mainMenu = Menu(self.master)
        self.master.configure(menu=mainMenu)

        fileMenu = Menu(mainMenu)
        animationMenu = Menu(mainMenu)

        animationMenu.add_command(label="Start Animation", command=self.start)
        animationMenu.add_command(label="Stop Animation", command=self.stop)
        animationMenu.add_separator()
        animationMenu.add_command(label="Reset Animation", command=self.reset)

        fileMenu.add_command(label="New File", command=self.file1)

        mainMenu.add_cascade(label="File", menu=fileMenu)
        mainMenu.add_cascade(label="Animation", menu=animationMenu)

    def setup_canvas(self):
        self.canvas.config(width=500, height=500)
        self.canvas.pack()

    def stop(self):
        self.should_run = False

    def start(self):
        self.should_run = True

    def reset(self):
        print("reset")

    def file1(self):
        print("file1")

    def draw(self):
        if self.should_run:
            self.canvas.delete("all")
            for i in range(0, self.N):
                radius = 1e18
                x = round(self.bodies[i].rx*250/radius) + 250
                y = round(self.bodies[i].ry*250/radius) + 250
                self.canvas.create_oval(
                    x, y, x+8, y+8, fill=self.bodies[i].color)
            self.addforces(self.N)
        self.master.after(1, self.draw)

    def circlev(self, rx, ry):
        # the bodies are initialized in circular orbits around the central mass.
        # This is just some physics to do that
        solar_mass = 1.98892e30
        r2 = math.sqrt(rx*rx+ry*ry)
        numerator = (6.67e-11)*1e6*solar_mass
        return math.sqrt(numerator/r2)

    def start_the_bodies(self, N):
        # Initialize N bodies with random positions and circular velocities
        solar_mass = 1.98892e30
        for i in range(0, N):
            px = 1e18*self.exp(-1.8)*(.5-random.random())
            py = 1e18*self.exp(-1.8)*(.5-random.random())
            mag_v = self.circlev(px, py)
            abs_angle = math.atan(abs(py/px))
            theta_v = math.pi/2-abs_angle
            vx = -1*self.signum(py)*math.cos(theta_v)*mag_v
            vy = self.signum(px)*math.sin(theta_v)*mag_v

            if random.random() <= .5:
                vx = -vx
                vy = -vy

            mass = random.random()*solar_mass*10+1e20
            red = int(math.floor(mass*254/(solar_mass*10+1e20)))
            blue = int(math.floor(mass*254/(solar_mass*10+1e20)))
            green = 255

            colorval = "#%02x%02x%02x" % (red, green, blue)
            self.bodies.append(Body(px, py, vx, vy, mass, colorval))

        # put a heavy body in the center
        self.bodies[0] = Body(0, 0, 0, 0, 1e6*solar_mass, "red")

    def addforces(self, N):
        # Use the method in Body to reset the forces, then add all the new forces
        for i in range(0, self.N):
            self.bodies[i].resetForce()
            # Notice-2 loops-->N ^ 2 complexity
            for j in range(0, self.N):
                if (i != j):
                    self.bodies[i].addForce(self.bodies[j])

        # Then, loop again and update the bodies using timestep dt
        for i in range(0, self.N):
            self.bodies[i].update(1e11)

    def exp(self, value):
        return -math.log(1 - random.random()) / value

    def signum(self, int):
        if(int < 0):
            return -1
        elif(int > 0):
            return 1
        else:
            return int
