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
from Quad import Quad
from BHTree import BHTree

mass_scale = 1.98892e19
radius = 1e5


class NBodySimulation:
    def __init__(self, N):
        self.master = Tk()
        self.canvas = Canvas(self.master)
        self.master.title("Brute Force")
        if N > 1000:
            self.N = 1000
        else:
            self.N = N
        self.bodies = [None] * N
        self.starting_time = datetime.datetime.now()
        self.update_time = 0
        self.update_dt = 0
        self.frame_count = 0
        self.method = "BruteForce"
        self.quad = Quad(0, 0, 10*radius)
        self.setup_recording()
        self.setup_menu()
        self.setup_canvas()
        self.start_bodies(self.N)
        self.draw_animation()
        self.update_animation()

    def setup_recording(self):
        self.is_recording_data = BooleanVar()
        self.is_recording_data.set(False)
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
        animation_menu.add_command(label="Reset Animation", command=self.reset)
        animation_menu.add_command(
            label="Change Body Count", command=self.change_body_count)
        animation_menu.add_separator()
        animation_menu.add_command(label="Brute Force", command=self.setup_brute_force)
        animation_menu.add_command(label="Barnes Hut", command=self.setup_barnes_hut)

        record_menu.add_checkbutton(
            label="Recording Data", onvalue=1, offvalue=0, variable=self.is_recording_data)

        record_menu.add_checkbutton(
            label="Recording Data", onvalue=1, offvalue=0, variable=self.is_recording_data)
        record_menu.add_command(label="Change Recording Directory",
                                command=self.choose_directory)

        mainMenu.add_cascade(label="Animation", menu=animation_menu)
        mainMenu.add_cascade(label="Recording", menu=record_menu)

    def setup_canvas(self):
        self.canvas.config(width=1200, height=800)
        self.canvas.pack()

    def start(self):
        self.frame_count = 0
        self.update_time = millis()

    def reset(self):
        self.canvas.delete("all")
        self.start_bodies(self.N)
        self.draw_animation()

    def setup_brute_force(self):
        self.master.title("Brute Force")
        self.method = "BruteForce"

    def setup_barnes_hut(self):
        self.master.title("Barnes Hut")
        self.method = "BarnesHut"

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
            + self.bodies[0].toString() + "\n"
        print("[Frame: " + str(self.frame_count) + "] is recorded")
        f.write(data)
        f.close()

    def update_animation(self):
        while True:
            startTime = time.time()
            self.frame_count += 1
            self.draw_animation()
            self.update_dt = millis() - self.update_time
            self.update_time = millis()
            if self.is_recording_data.get() == 1:
                self.record_data()
            if self.method == "BarnesHut":
                self.addforcesBarnesHut()
            else:
                self.addforcesBruteForce()
            self.master.update()
            self.master.update_idletasks()
            endTime = time.time()
            elapsedTime = endTime - startTime
            self.master.title(self.method + "FPS: {}".format(int(1/elapsedTime)))

    def draw_animation(self):
        self.canvas.delete("all")
        for body in self.bodies:
            x = round(body.rx*600/radius) + 600
            y = round(body.ry*400/radius) + 400
            self.canvas.create_oval(x, y, x+8, y+8, fill=body.color)

    def start_bodies(self, N):
        # Initialize N bodies with random positions and linear velocities
        self.starting_time = datetime.datetime.now()
        for i in range(0, N):
            random_x = radius * (.5 - 1.2 * random.random())
            random_y = radius * (.5 - 1.2 * random.random())
            vx = random.random() if random.random() < .5 else -random.random()
            vy = random.random() if random.random() < .5 else -random.random()
            mass = (0.5 * random.random() + 0.5)*mass_scale
            red = int(math.floor(mass*254/(mass_scale)))
            blue = int(math.floor(mass*254/(mass_scale)))
            green = 255
            colorval = "#%02x%02x%02x" % (red, green, blue)
            self.bodies[i] = Body(random_x, random_y, vx, vy, mass, colorval)

        (kinetic_energy, potential_energy) = total_energies(self.bodies)
        scale_factor = math.sqrt(abs(potential_energy)/(2*kinetic_energy))
        for body in self.bodies:
            body.scale_velocity(scale_factor)

        (velocity_cmx, velocity_cmy) = velociy_cm(self.bodies)
        (position_cmx, position_cmy) = position_cm(self.bodies)
        for body in self.bodies:
            body.scale_cm_position(position_cmx, position_cmy)
            body.scale_cm_velocity(velocity_cmx, velocity_cmy)

    def addforcesBruteForce(self):
        # Use the method in Body to reset the forces, then add all the new forces
        for body in self.bodies:
            body.resetForce()
            # Notice-2 loops-->N ^ 2 complexity
            for other in self.bodies:
                if body is other:
                    continue
                body.addForce(other)

        for body in self.bodies:
            # Then, loop again and update the bodies using timestep dt
            body.update(1)

    # The BH algorithm: calculate the forces

    def addforcesBarnesHut(self):
        thetree = BHTree(self.quad)
        # If the body is still on the screen, add it to the tree
        for body in self.bodies:
            if (body.inside(self.quad)):
                thetree.insert(body)
            # Now, use out methods in BHTree to update the forces,
            # traveling recursively through the tree
        for body in self.bodies:
            body.resetForce()
            if (body.inside(self.quad)):
                thetree.updateForce(body)
                # Calculate the new positions on a time step dt(1e11 here)
                body.update(1)