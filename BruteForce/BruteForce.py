from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from Utils import *
import random
import time
import datetime
import math
import os
from Body import Body


class BruteForce:
    def __init__(self, master, N):
        self.master = master
        self.canvas = Canvas(master)
        if N > 1000:
            self.N = 1000
        else:
            self.N = N
        self.bodies = [None] * N
        self.should_run = False
        self.starting_time = datetime.datetime.now()
        self.update_time = 0
        self.update_dt = 0
        self.frame_count = 0

        self.setup_recording()
        self.setup_menu()
        self.setup_canvas()

        self.start_bodies(self.N)
        self.draw_animation()
        self.update_animation()

    def setup_recording(self):
        self.is_recording_data = BooleanVar()
        self.is_recording_data.set(True)
        path = os.path.dirname(__file__) + "/data"
        if os.path.exists(path):
            self.recording_directory = path
            print("Path assigned: " + path)
        else:
            os.mkdir(path)
            self.recording_directory = path
            print("Path created and assigned: " + path)

    def setup_menu(self):
        mainMenu = Menu(self.master)
        self.master.configure(menu=mainMenu)

        record_menu = Menu(mainMenu)
        animation_menu = Menu(mainMenu)

        animation_menu.add_command(label="Start Animation", command=self.start)
        animation_menu.add_command(label="Stop Animation", command=self.stop)
        animation_menu.add_separator()
        animation_menu.add_command(label="Reset Animation", command=self.reset)
        animation_menu.add_separator()
        animation_menu.add_command(
            label="Change Body Count", command=self.change_body_count)

        record_menu.add_checkbutton(
            label="Recording Data", onvalue=1, offvalue=0, variable=self.is_recording_data)
        record_menu.add_command(label="Change Recording Directory",
                                command=self.choose_directory)

        mainMenu.add_cascade(label="Animation", menu=animation_menu)
        mainMenu.add_cascade(label="Recording", menu=record_menu)

    def setup_canvas(self):
        self.canvas.config(width=500, height=500)
        self.canvas.pack()

    def stop(self):
        self.should_run = False

    def start(self):
        self.frame_count = 0
        self.should_run = True
        self.update_time = millis()

    def reset(self):
        self.should_run = False
        self.start_bodies(self.N)
        self.draw_animation()

    def change_body_count(self):
        answer = simpledialog.askinteger("Body Count", "Please enter a body count for N body simulation",
                                         parent=self.master,
                                         minvalue=2, maxvalue=1000)
        if answer is not None:
            print("Body count changed to: ", answer)
            self.N = answer
            self.bodies = [None] * self.N
            self.reset()
        else:
            print("Body count not changed")

    def choose_directory(self):
        path = filedialog.askdirectory(parent=self.master)
        if path is not None:
            self.recording_directory = path
            print("Path assigned: " + path)
        else:
            print("Path not changed")

    def record_data(self):
        file_dir = self.recording_directory + \
            "/" + str(self.starting_time) + ".txt"
        f = open(file_dir, "a+")
    #    for i in range(0, self.N):
        data = "[Frame: " + str(self.frame_count) + " | " \
            + "Body: " + str(1) + " | " \
            + "dt: " + str(self.update_dt) + "] " \
            + self.bodies[1].toString() + "\n"
        print("[Frame: " + str(self.frame_count) + "] is recorded")
        f.write(data)
        f.close()

    def update_animation(self):
        if self.should_run:
            self.frame_count += 1
            self.draw_animation()

            self.update_dt = millis() - self.update_time
            self.update_time = millis()
            if self.is_recording_data.get() == 1:
                self.record_data()

        self.master.after(1, self.update_animation)

    def draw_animation(self):
        self.canvas.delete("all")
        for i in range(0, self.N):
            radius = 1e18
            x = round(self.bodies[i].rx*250/radius) + 250
            y = round(self.bodies[i].ry*250/radius) + 250
            self.canvas.create_oval(x, y, x+8, y+8, fill=self.bodies[i].color)
        self.addforces(self.N)

    def circlev(self, rx, ry):
        # the bodies are initialized in circular orbits around the central mass.
        # This is just some physics to do that
        solar_mass = 1.98892e30
        r2 = math.sqrt(rx*rx+ry*ry)
        numerator = (6.67e-11)*1e6*solar_mass
        return math.sqrt(numerator/r2)

    def start_bodies(self, N):
        # Initialize N bodies with random positions and circular velocities
        self.starting_time = datetime.datetime.now()
        solar_mass = 1.98892e30
        for i in range(0, N):
            px = 1e18*exp(-1.8)*(.5-random.random())
            py = 1e18*exp(-1.8)*(.5-random.random())
            mag_v = self.circlev(px, py)
            abs_angle = math.atan(abs(py/px))
            theta_v = math.pi/2-abs_angle
            vx = -1*signum(py)*math.cos(theta_v)*mag_v
            vy = signum(px)*math.sin(theta_v)*mag_v

            if random.random() <= .5:
                vx = -vx
                vy = -vy

            mass = random.random()*solar_mass*10+1e20
            red = int(math.floor(mass*254/(solar_mass*10+1e20)))
            blue = int(math.floor(mass*254/(solar_mass*10+1e20)))
            green = 255

            colorval = "#%02x%02x%02x" % (red, green, blue)
            self.bodies[i] = Body(px, py, vx, vy, mass, colorval)

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
