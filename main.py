#main.py, responsible for the GUI management of the simulator.

from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6 import uic, QtWidgets
import sys
import katyusha
import math

open("log.txt", "w")
with open("track.csv", "w") as outs:
    outs.write("")

kate = katyusha.katyusha([0, 0])
angle = 30
friction_coefficient = 0.75
radians = angle * math.pi / 180
print(friction_coefficient * math.cos(radians) + math.sin(radians))
kate.launch(1)

target_coordinates = [13500, 1000]

angle_of_launch = kate.train(target_coordinates)
print(angle_of_launch)
