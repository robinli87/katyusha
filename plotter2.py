#plotter2

import sys
import numpy as np
from vispy import scene, app
import threading
import time
from vispy.scene.visuals import Polygon, Ellipse, Rectangle, RegularPolygon

canvas = scene.SceneCanvas(keys='interactive', show=True, fullscreen=True)
grid = canvas.central_widget.add_grid(margin=10)
grid.spacing = 0

title = scene.Label("Plot Title", color='white')
title.height_max = 40
grid.add_widget(title, row=0, col=0, col_span=2)



right_padding = grid.add_widget(row=1, col=2, row_span=1)
right_padding.width_max = 50

view = grid.add_view(row=1, col=1, border_color='white')



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
    global xaxis
    global yaxis
    plot = scene.LinePlot((x, y), parent=view.scene, color='b', marker_size=0)
    view.camera = scene.cameras.panzoom.PanZoomCamera(aspect=1, rect=(-100, -100, max(x), max(y)))
    yaxis = scene.AxisWidget(orientation='left',
                        axis_label='Y Axis',
                        axis_font_size=12,
                        axis_label_margin=50,
                        tick_label_margin=5, domain=(0, max(y)))
    yaxis.width_max = 80
    grid.add_widget(yaxis, row=1, col=0)

    xaxis = scene.AxisWidget(orientation='bottom',
                            axis_label='X Axis',
                            axis_font_size=12,
                            axis_label_margin=50,
                            tick_label_margin=5, domain=(0, max(y)))

    xaxis.height_max = 80
    grid.add_widget(xaxis, row=2, col=1)
    xaxis.link_view(view)
    yaxis.link_view(view)

def animate():
    rocket = Rectangle(center=(x[0], y[0]), width=100, height=100, parent=view.scene, color='r')
    for i in range(0, len(x)):
        rocket.center = (x[i], y[i])
        time.sleep(0.001)


update()
plot()
threading.Thread(target=animate).start()
#animate()

app.run()
