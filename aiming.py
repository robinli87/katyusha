#aiming.py
# sketches graph of loss against launch angle

import katyusha
import vispy.plot as vp
import numpy as np
import math
import multiprocessing as mp

fig = vp.Fig(keys='interactive', show=False)
plotwidget = fig[0, 0]
fig.title="Loss function"

target_coordinates = [100000, 1000]

kate = katyusha.katyusha(dt=0.001, target=target_coordinates)

angles = range(0, 90)
for a in angles:
    a = a * math.pi / 180

losses = [None]*90

def computation(i):

    return([kate.miss(angles[i]), i])

def log_result(result):
    index = result[1]
    value = result[0]
    losses[index] = value

print("computing loss spectrum")

pool = mp.Pool()

for i in range(0, len(angles)):
    #each angle is a thread
    pool.apply_async(computation, args=(i, ), callback = log_result)

pool.close()
pool.join()

optimum = min(losses)

bestangle = angles[losses.index(optimum)]
print(bestangle)

angles = np.linspace(bestangle-1, bestangle+1, 100)
losses = np.linspace(bestangle-1, bestangle+1, 100)

def computation(i):

    return([kate.miss(angles[i]), i])

def log_result(result):
    index = result[1]
    value = result[0]
    losses[index] = value

print("computing loss spectrum")

pool = mp.Pool()

for i in range(0, len(angles)):
    #each angle is a thread
    pool.apply_async(computation, args=(i, ), callback = log_result)

pool.close()
pool.join()


plotwidget.plot((angles, losses))

fig.show(run=True)
