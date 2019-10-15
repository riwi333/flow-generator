from context import Grid, Flow, graphics
import pyglet
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

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
GRID_SIZE = 8

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

# dictionary mapping indices to the grid's Flow objects
flows, index = {}, 0

# set up the cursor
flow_selected = False   # boolean of whether or now we're currently drawing a flow
cursor_cell = (0, 0)    # start the cursor in the bottom left corner
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

    for i in flows.keys():
        flows[i].updateGraphics()
        flows[i].draw()

# dictionary of arrow key mappings to coordinate changes
keys = {    pyglet.window.key.LEFT: ( -1, 0 ),
            pyglet.window.key.RIGHT: ( 1, 0 ),
            pyglet.window.key.DOWN: ( 0, -1 ),
            pyglet.window.key.UP: ( 0, 1 )  }

# control drawing with the keyboard
@window.event
def on_key_press(symbol, modifiers):
    global flow_selected, flows, index, cursor_cell, cursor, grid

    assert grid.inBounds(cursor_cell), "Cursor cell out of bounds"

    # press the spacebar to start drawing a flow; press it again to stop
    if symbol == pyglet.window.key.SPACE:
        # if we're not currently drawing a flow, make a new one
        if flow_selected is False and grid.isEmpty(cursor_cell):
            flows[index] = Flow(    grid,
                                    [ floor(random() * 256) for x in range(3) ],
                                    index,
                                    path=[]   )

            # make sure the initial endpoint is drawn
            flows[index].addCell(cursor_cell)
            flow_selected = True

        # if we're currently drawing a flow, put its second endpoint down and stop
        elif flow_selected is True:
            assert not grid.isEmpty(cursor_cell), "Endpoint of flow still unoccupied"

            flow_selected = False
            index += 1

    # press the backspace key on a flow (or while drawing a flow) to delete it
    elif symbol == pyglet.window.key.BACKSPACE and not grid.isEmpty(cursor_cell):
        flow_index = grid.values[cursor_cell]

        condition1 = flow_selected is True
        condition2 = flow_selected is False and not flow_index == None

        # delete either the current flow being drawn or a finished flow
        if condition1 or condition2:
            # mark each cell in the flow as unoccupied
            for cell in flows[flow_index].path:
                grid.resetCell(cell)

            # delete the Flow object
            del flows[flow_index]

            flow_selected = False

    # move the cursor and flows with the arrow keys
    elif symbol in keys.keys():
        next_cell = ( cursor_cell[0] + keys[symbol][0], cursor_cell[1] + keys[symbol][1] )

        # make sure the calculated new cursor position is within the grid
        if grid.inBounds(next_cell):
            # if we're currently drawing a flow, the cursor should not be able to pass
            # through occupied cells
            if ( flow_selected is True and grid.isEmpty(next_cell) ) or flow_selected is False:
                graphics.moveCircle(cursor, grid.getCellCenter(cursor_cell), grid.getCellCenter(next_cell))
                cursor_cell = next_cell

        # if a flow is being drawn, add this next (empty, within the grid) cell to it
        if flow_selected is True:
            if grid.inBounds(cursor_cell) and grid.isEmpty(cursor_cell):
                flows[index].addCell(cursor_cell)

pyglet.app.run()
