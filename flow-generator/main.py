import pyglet
from grid import Grid
from flow import Flow
import generator
from math import floor
from random import random, shuffle
import sys

"""
run the path generation algorithm and display the resulting solved flow puzzle

TODO:
    -   (eventually) add option to play puzzle with controls similar to 'tools/selfdraw.py'
    
"""

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
GRID_ORIGIN = (50, 50)
GRID_WIDTH = WINDOW_WIDTH - 2 * GRID_ORIGIN[0]
GRID_HEIGHT = WINDOW_HEIGHT - 2 * GRID_ORIGIN[1]
MAX_ROWS = 20
MAX_COLS = 20

# list of distinct colors we use for flows
COLORS = [
    (0, 255, 0),        # green
    (0, 0, 255),        # dark blue
    (255, 0, 255),      # fuchsia
    (153, 102, 51),     # brown
    (255, 255, 0),      # yellow
    (255, 153, 0),      # orange
    (255, 0, 0),        # red
    (153, 0, 255),      # purple
    (255, 255, 255),    # white
    (0, 255, 255),      # aqua blue
    (153, 204, 255),    # baby blue
    (153, 0, 0),        # dark red
    (229, 204, 255),    # light purple
    (255, 250, 200),    # beige
    (230, 190, 138),    # rose gold
    (255, 77, 136),     # rose
    (59, 122, 87),      # dark green
    (128, 128, 128),    # gray
    (176, 191, 26),     # acid green
    (70, 153, 144),     # teal
    (0, 175, 255),      # sky blue
    (95, 95, 255),      # royal blue
    (135, 0, 135),      # magenta
    (228, 228, 228)     # light gray
]

assert len(COLORS) >= max([ MAX_ROWS, MAX_COLS ]), "Not enough colors for all grids"

# flag to decide whether the grid should be displayed solved or unsolved
show_solved = True

# get the option to see the grid unsolved (solved by default)
if "--unsolved" in sys.argv:
    sys.argv.remove("--unsolved")
    show_solved = False

if "--solved" in sys.argv:
    sys.argv.remove("--solved")
    show_solved = True

# get the grid dimensions from the command line arguments
try:
    rows = min([ int(sys.argv[1]), MAX_ROWS ])
    cols = min([ int(sys.argv[2]), MAX_COLS ])

except ValueError:
    rows = floor(random() * (MAX_ROWS - 4)) + 4
    cols = min([ rows, MAX_COLS ])
    print("Grid dimensions must be integers; generating a " + str(rows) + "x" + str(cols) + " grid instead")
    cols = rows

except IndexError:
    if len(sys.argv) == 1:
        rows = floor(random() * (MAX_ROWS - 4)) + 4
        cols = min([ rows, MAX_COLS ])
        print("No dimensions provided; generating a " + str(rows) + "x" + str(cols) + " grid")
    else:
        cols = rows

# create the window and the grid
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
grid = Grid(    GRID_ORIGIN,
                GRID_WIDTH,
                GRID_HEIGHT,
                rows,
                cols,
                (179, 179, 179),
                thickness = 5.0,    )

attempts, paths = 0, None
while paths == None:
    grid.clearValues()
    paths = generator.generatePaths(grid)
    attempts += 1

print("Generated paths after " + str(attempts) + " attempt(s)")

paths = generator.simplifyPaths(grid, paths)

# make sure all cells in the list of paths are unique
flatten = lambda multi : [x for arr in multi for x in arr]
assert len(flatten(paths)) == len(set(flatten(paths)))

# make sure we have enough colors for this set of paths
assert len(COLORS) >= len(paths), "Not enough colors for this grid"

# shuffle the list of colors so random ones are chosen
shuffle(COLORS)

flows = []
for path in paths:
    color = COLORS.pop()

    # show the completed flows or just their endpoints based on the given flag
    # (completed flows are shown by default)
    if show_solved:
        flows.append(   Flow(   grid,
                                color,
                                len(flows),
                                path = path   )  )
    else:
        flows.append(   Flow(   grid,
                                color,
                                len(flows),
                                path = [ path[0] ]  ) )
        flows.append(   Flow(   grid,
                                color,
                                len(flows),
                                path = [ path[-1] ]  ) )

# update all the flows' graphics so they can be drawn
for flow in flows:
    flow.updateGraphics()

@window.event
def on_draw():
    grid.draw()

    for flow in flows:
        flow.draw()

pyglet.app.run()
