import pyglet
from grid import Grid
from flow import Flow
import generator
import graphics
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

# flag to decide whether or not this grid will be played
interactive = False

# get the option to see the grid unsolved (solved by default)
if "--unsolved" in sys.argv:
    sys.argv.remove("--unsolved")
    show_solved = False

if "--solved" in sys.argv:
    sys.argv.remove("--solved")
    show_solved = True

# get the option to play the grid (off by default)
if "--interactive" in sys.argv:
    sys.argv.remove("--interactive")
    interactive = True
    show_solved = False

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

flows, index = [], 0
for path in paths:
    color = COLORS.pop()

    # show the completed flows or just their endpoints based on the given flag
    # (completed flows are shown by default)
    if show_solved:
        flows.append(   Flow(   grid,
                                color,
                                index,
                                path = path   )  )
    else:
        flows.append(   Flow(   grid,
                                color,
                                index,
                                path = [ path[0] ]  ) )
        flows.append(   Flow(   grid,
                                color,
                                index,
                                path = [ path[-1] ]  ) )

    index += 1

# create necessary objects for the interactive version
if interactive:
    # note that since each individual endpoint is considered a flow, each flow has two
    # indices: 1) its flow index (endpoints that should be connected have the same flow
    # index) and 2) its index in the flows[] list
    flow_index = None
    list_index = None

    keys = {    pyglet.window.key.LEFT: ( -1, 0 ),
                pyglet.window.key.RIGHT: ( 1, 0 ),
                pyglet.window.key.DOWN: ( 0, -1 ),
                pyglet.window.key.UP: ( 0, 1 )  }

    endpoints = {}
    for i in range(len(flows)):
        endpoints[ flows[i].path[0] ] = ( flows[i].index, i )

    cursor_cell = (0, 0)
    while cursor_cell in endpoints:
        cursor_cell = ( floor(cols * random()), floor(rows * random()) )
    cursor_batch = pyglet.graphics.Batch()
    cursor = graphics.generateCircle(   grid.getCellCenter(cursor_cell),
                                        0.1 * min(grid.getSpacing()),
                                        10,
                                        fill = True,
                                        batch = cursor_batch    )

@window.event
def on_key_press(symbol, modifiers):
    # don't do anything with key presses if this isn't interactive
    if interactive is False:
        return

    global cursor_cell, cursor, flow_index, list_index, flows, grid

    if symbol == pyglet.window.key.SPACE:
        # if we're not currently drawing a flow, start drawing with whatever flow
        # the cursor is on top of
        if list_index is None:
            # TODO: make sure a flow hasn't already been drawn on the endpoint
            if cursor_cell in endpoints:
                flow_index, list_index = endpoints[cursor_cell]

        # otherwise, if we're already drawing one, reset it back to its original
        # state and unselect it
        else:
            flow = flows[list_index]

            print(flow.flowBatch._dump_draw_list())

            while len(flow.path) > 1:
                flow.removeCell(flow.path[-1])

            flow.updateGraphics()
            print(flow.flowBatch._dump_draw_list())

            flow_index, list_index = None, None

    # if we're not currently drawing a flow, reset whatever flow the cursor is on top of
    elif symbol == pyglet.window.key.BACKSPACE:
        if list_index is None:
            """
            if cursor_cell in endpoints:
                flow = flows[endpoints[cursor_cell][1]]

                while len(flow.path) > 1:
                    flow.removeCell(flow.path[-1])
            """

            pass

    # move the cursor and connect flows with the arrow keys
    elif symbol in keys:
        next_cell = ( cursor_cell[0] + keys[symbol][0], cursor_cell[1] + keys[symbol][1] )

        # make sure the new cursor is within the grid
        if grid.inBounds(next_cell):
            if list_index is None:
                # if we're not drawing a flow, move the cursor to its new location
                graphics.moveCircle(cursor, grid.getCellCenter(cursor_cell), grid.getCellCenter(next_cell))
                cursor_cell = next_cell
            else:
                # if moving to the next cell will complete the flow, stop drawing
                if next_cell in endpoints:
                    if endpoints[next_cell][0] == flow_index:
                        flows[list_index].addCell(next_cell)
                        graphics.moveCircle(cursor, grid.getCellCenter(cursor_cell), grid.getCellCenter(next_cell))
                        cursor_cell = next_cell

                        flow_index, list_index = None, None

                # otherwise just add this next empty cell to the current flow
                else:
                    if grid.isEmpty(next_cell):
                        flows[list_index].addCell(next_cell)
                        graphics.moveCircle(cursor, grid.getCellCenter(cursor_cell), grid.getCellCenter(next_cell))
                        cursor_cell = next_cell

@window.event
def on_draw():
    window.clear()

    if interactive:
        cursor_batch.draw()

    grid.draw()

    for flow in flows:
        flow.updateGraphics()
        flow.draw()

pyglet.app.run()
