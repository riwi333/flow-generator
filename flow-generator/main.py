import pyglet
from grid import Grid
from flow import Flow
import generator
from math import floor
from random import random

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
GRID_SIZE = 11

# create the window and the grid
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
grid = Grid(    [ 50, 50 ],
                700, 400,
                GRID_SIZE,
                GRID_SIZE,
                (179, 179, 179),
                thickness = 5.0,    )

paths, empty = generator.generateFlows(grid)

flows = []
for path in paths:
    flows.append(   Flow(   grid,
                            [ floor(random() * 256) for x in range(3) ],
                            len(flows),
                            path=path   )  )

# update all the flows' graphics so they can be drawn
for flow in flows:
    flow.updateGraphics()

@window.event
def on_draw():
    grid.draw()

    for flow in flows:
        flow.draw()

pyglet.app.run()
