import pyglet
import graphics
from grid import Grid
from flow import Flow
from random import random, seed
from datetime import datetime
from math import floor

"""
tool allowing you to draw custom flows on a grid

Controls:
- Use the arrows keys to move the cursor around
- Press the spacebar to start a flow, and spacebar again to end it
- Press backspace while the cursor is on a flow to erase it (even
while drawing it)

"""

# TODO: code only allows you to delete the first flow without issues

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
GRID_SIZE = 7

# seed the random generator
seed(datetime.now())

# create the window and the grid
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
grid = Grid(    [ 50, 50 ],
                700, 400,
                GRID_SIZE,
                GRID_SIZE,
                (179, 179, 179),
                thickness = 5.0,    )

# list of the grid's Flow objects
flows = []
n_flow = 0

# set up the cursor
flow_selected = False                       # boolean of whether or now we're currently drawing a flow
cursor_cell = ( 0 , grid.rows - 1 )         # start the cursor in the top left corner
cursor_batch = pyglet.graphics.Batch()
cursor = graphics.generateCircle(   grid.getCellCenter(cursor_cell),
                                    0.2 * min(*grid.getSpacing()),
                                    15,
                                    fill = True,
                                    batch = cursor_batch )

# draw the grid, flows, and cursor on the window
@window.event
def on_draw():
    window.clear()

    grid.draw()
    cursor_batch.draw()

    for flow in flows:
        flow.updateGraphics()
        flow.draw()

# dictionary of arrow key mappings to coordinate changes
keys = {    pyglet.window.key.LEFT: ( -1, 0 ),
            pyglet.window.key.RIGHT: ( 1, 0 ),
            pyglet.window.key.DOWN: ( 0, -1 ),
            pyglet.window.key.UP: ( 0, 1 )  }

# control drawing with the keyboard
@window.event
def on_key_press(symbol, modifiers):
    global flow_selected, flows, n_flow, cursor_cell, cursor, grid

    next_cell = cursor_cell

    print(cursor_cell)
    print(grid.values[cursor_cell])
    print(flow_selected)
    print("")

    # press the spacebar to start drawing a flow; press it again to stop
    if symbol == pyglet.window.key.SPACE:
        # if we're not currently drawing a flow, make a new one
        if flow_selected is False and grid.values[cursor_cell] == None:
            flows.append(Flow(  grid,
                                [ floor(random() * 255) for x in range(3) ],
                                n_flow  ))

            # make sure the initial endpoint is drawn
            flows[n_flow].addCell(cursor_cell)
            flow_selected = True

        # if we're currently drawing a flow, put its second endpoint down and stop
        elif flow_selected is True and grid.values[cursor_cell] == n_flow:
                flows[n_flow].addCell(cursor_cell)

                n_flow = n_flow + 1
                flow_selected = False

    # press the backspace key on a flow (or while drawing a flow) to delete it
    elif symbol == pyglet.window.key.BACKSPACE and not grid.values[cursor_cell] == None:
        flow_index = grid.values[cursor_cell]

        condition1 = flow_selected is True
        condition2 = flow_selected is False and flow_index > -1

        # delete either the current flow being drawn or a finished flow
        if condition1 or condition2:
            # update the record of which flow belongs to each cell
            for cell in grid.getAllCellCoordinates():
                if not grid.isEmpty(cell) and grid.values[cell] > flow_index:
                    grid.values[cell] = grid.values[cell] - 1

                elif grid.values[cell] == flow_index:
                    grid.values[cell] = None

            # delete the Flow object
            flow_object = flows.pop(flow_index)
            del flow_object

            # update the number of Flows if needed
            if condition2:
                n_flow = n_flow - 1

            flow_selected = False

    # move the cursor and flows with the arrow keys
    elif symbol in keys.keys():
        next_cell = ( cursor_cell[0] + keys[symbol][0], cursor_cell[1] + keys[symbol][1] )

        # if a flow is being drawn, add this next (empty, within the grid) cell to it
        if flow_selected is True:
            if grid.inBounds(next_cell) and grid.isEmpty(next_cell):
                flows[n_flow].addCell(next_cell)
            else:
                next_cell = cursor_cell

        if flow_selected is False:
            if not grid.inBounds(next_cell):
                next_cell = cursor_cell

    # update the cursor's position on the grid
    graphics.moveCircle(cursor, grid.getCellCenter(cursor_cell), grid.getCellCenter(next_cell))
    cursor_cell = next_cell

pyglet.app.run()
