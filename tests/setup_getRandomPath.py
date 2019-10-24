from context import Grid, Flow, generator
from math import floor
from random import random
import pyglet

"""
helper functions for getRandomPath() test cases
"""

FAILURE_MESSAGE = "Randomized path was determined illegal. Visualizing..."
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
GRID_ORIGIN = (50, 50)
GRID_WIDTH = WINDOW_WIDTH - 2 * GRID_ORIGIN[0]
GRID_HEIGHT = WINDOW_HEIGHT - 2 * GRID_ORIGIN[1]

def testPathLegality(grid, path):
    """
    test if this path is legal (and creates legal components)

    @param  grid    :   grid that the path is placed in
    @param  path    :   path to test

    @return         :   True if the path is legal, and False otherwise
    """

    if len(path) < 3:
        return False

    # make sure the path doesn't touch itself
    if grid.pathDegree(path[0], path) > 1 or grid.pathDegree(path[-1], path) > 1:
        return False
    for i in range(1, len(path) - 1):
        if grid.pathDegree(path[i], path) > 2:
            return False

    empty = list(grid.unoccupied)
    for cell in path:
        empty.remove(cell)

    components = generator.getComponents(grid, empty = empty)

    for component in components:
        if len(component) in [1, 2, 4, 5]:
            return False

    return True

def visualizePath(grid, path):
    """
    draw the grid with the specified path represented by a Flow

    @param  grid    :   grid that the path is placed in
    @param  path    :   path to visualize
    """

    # create the Flow object
    flow = Flow(    grid,
                    [ floor(random() * 256) for x in range(3) ],
                    0,
                    path = path )

    # create the pyglet window and draw the objects
    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    flow.updateGraphics()

    @window.event
    def on_draw():
        grid.draw()
        flow.draw()

    pyglet.app.run()
