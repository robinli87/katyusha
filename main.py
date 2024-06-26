#main.py, responsible for the GUI management of the simulator.

from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6 import uic, QtWidgets
import sys
import katyusha
import math
import os

open("log.txt", "w")
with open("track.csv", "w") as outs:
    outs.write("")

kate = katyusha.katyusha(dt=0.001, initial_fuel_mass=300, shell_mass=60, fuel_burn_rate=20, specific_impulse=2300, rack_length=60,
                         friction_coefficient=0.75, rocket_length=2, flaps_size=0.1, rotation_resistance=10**-2, bernoulli_coefficient=0.004)

target_coordinates = [100000, 1000]
with open("parameters.dat", "w") as f:
    f.write(str(target_coordinates[0]) + ",")
    f.write(str(target_coordinates[1]) + "\n")

#print("searching for optimum angle of launch")
#angle_of_launch = kate.train(target_coordinates)
#print(angle_of_launch)

angle_of_launch = 70#write in degrees
angle_of_launch = angle_of_launch * math.pi / 180

print(kate.launch(angle_of_launch, log=True))
os.system("python3 plotter2.py")
