#plot data in vispy

import vispy.plot as vp
import numpy as np
import threading
import time

fig = vp.Fig(keys='interactive', show=False)
plotwidget = fig[0, 0]
fig.title="Rocket Trajectory"

x = []
y = []
t = []

runFlag = True

def update():
    with open("track.csv", "r") as datafile:
        nextline = datafile.readline()
        while nextline != "":
            line = nextline.split(",")
            x.append(float(line[0]))
            y.append(float(line[1]))
            t.append(line[-2])

            nextline = datafile.readline()

        runflag = False

def plot():
    time.sleep(0.5)
    graph = plotwidget.plot((x, y), title=t[-1])
    while runFlag == True:
        graph.set_data((x,y))
        time.sleep(1)

threading.Thread(target=update).start()
threading.Thread(target=plot).start()

fig.show(run=True)

