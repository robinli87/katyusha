#all trajectory plots

import numpy as np
import vispy.plot as vp
import katyusha
import multiprocessing as mp
import math
import threading
import vispy.io as io
import itertools
from vispy.color import get_colormaps

colormaps = itertools.cycle(get_colormaps())

angles = []
for i in range(1, 91):
    angles.append(i * math.pi / 180)

imgsize = (7860, 4320) #8k

fig = vp.Fig(keys='interactive', show=False, fullscreen=True, size=imgsize)
plotwidget = fig[0, 0]
fig.title="Rocket Trajectory"

collection = []

def computation(theta):

    kate = katyusha.katyusha(dt=0.001, initial_fuel_mass=30, shell_mass=15, fuel_burn_rate=2, specific_impulse=2100, rack_length=10,
                         friction_coefficient=0.75, rocket_length=1, flaps_size=0.5, rotation_resistance=10**-2, bernoulli_coefficient=0.0336)
    traj = kate.launch(theta)
    x = kate.x
    y = kate.y


    return([x, y])

def log_result(result):
    collection.append(result)
    colour = next(colormaps)
    graph = plotwidget.plot((result[0], result[1]), marker_size=0, color=colour)


pool = mp.Pool()
for a in angles:
    pool.apply_async(computation, args=(a, ), callback=log_result)

pool.close()
pool.join()

print(len(collection))
#print(angles)

#graph = plotwidget.plot((collection[40][0], collection[40][1]))
def writeout():
    image = fig.render(size=imgsize)
    io.write_png("wonderful.png",image)


writeout()
#fig.show(run=True)
#app.run()
