import pyglet
import graphics as graphics
from grid import Grid
from flow import Flow
from random import random, shuffle
from datetime import datetime
from math import floor, ceil

"""
functions for handling flow generation

"""

# constants for mapping directions to numbers
LEFT_DIRECTION = 0
DOWN_DIRECTION = 1
RIGHT_DIRECTION = 2
UP_DIRECTION = 3

directions = [ LEFT_DIRECTION, DOWN_DIRECTION, RIGHT_DIRECTION, UP_DIRECTION ]

# lambda functions to produce adjacent cell coordinates depending on direction
# x is the column of the cell, and y is the row
next = {
    LEFT_DIRECTION  :   lambda x, y   : [x - 1, y],
    DOWN_DIRECTION  :   lambda x, y   : [x, y - 1],
    RIGHT_DIRECTION :   lambda x, y   : [x + 1, y],
    UP_DIRECTION    :   lambda x, y   : [x, y + 1]
}

def isEmpty(grid, cell):
    """
    determine if this cell is occupied by a flow or not

    @param  grid    :   grid of the cell
    @param  cell    :   2-tuple of 0-indexed (column, row) pair

    @return         :   boolean of whether cell is not occupied
    """

    return grid.values[ cell[0] ][ cell[1] ] == None

def inGrid(grid, cell):
    """
    determine if this (col, row) pair fits in the grid or not

    @param  grid    :   grid of the cell
    @param  cell    :   2-tuple of 0-indexed (column, row) pair

    @return         :   boolean of whether (col, row) lies within the grid
    """

    if 0 <= cell[0] < grid.cols:
        if 0 <= cell[1] < grid.rows:
            return True

    return False

def flowDegree(grid, cell, flow):
    """
    find number of cells occupied by the given flow this (col, row) is adjacent with

    @param  grid    :   grid of the cell
    @param  cell    :   2-tuple of 0-indexed (column, row) pair
    @param  flow    :   index of flow we're looking for

    @return         :   number of adjacent cells occupied by the flow
    """

    flowDeg = 0
    for direction in directions:
        next_cell = next[direction](*cell)

        if inGrid(grid, next_cell) and not grid.values[ next_cell[0] ][ next_cell[1] ] == None:
            if flow == None or grid.values[ next_cell[0] ][ next_cell[1] ].index == flow:
                flowDeg = flowDeg + 1

    return flowDeg

def degree(grid, cell):
    """
    find total number of occupied cells this (col, row) is adjacent with

    @param  grid    :   grid of the cell
    @param  cell    :   2-tuple of 0-indexed (column, row) pair

    @return         :   number of adjacent occupied cells
    """

    deg = 0
    for direction in directions:
        next_cell = next[direction](*cell)
        if inGrid(grid, next_cell) and not isEmpty(grid, next_cell):
            deg = deg + 1

    return deg

def getAllShortestPaths(grid, cell):
    """
    find the shortest paths from the start cell to all unoccupied cells in the grid

    @param  grid        :   grid of the start cell
    @param  cell        :   starting cell we find paths for

    @return             :   a 2D list of the parent cell of each cell in its shortest path
    """

    visited = [ [ False for x in range(grid.cols) ] for y in range(grid.rows) ]
    parents = [ [ None for x in range(grid.cols) ] for y in range(grid.rows) ]

    # perform a breadth-first search on the grid, starting with the starting cell
    # to find all its shortests paths
    queue = [ cell ]

    # mark the starting cell as visited (note that the only cell with a parent of None
    # is the starting cell)
    visited[ cell[0] ][ cell[1] ] = True

    while not queue == []:
        current = queue.pop(0)

        for direction in directions:
            next_cell = next[direction](*current)
            if inGrid(grid, next_cell) and isEmpty(grid, next_cell) and visited[ next_cell[0] ][ next_cell[1] ] is False:
                visited[ next_cell[0] ][ next_cell[1] ] = True
                parents[ next_cell[0] ][ next_cell[1] ] = current
                queue.append(next_cell)

    return parents

def randomStep(grid, path, flow_index=None):
    """
    add a cell to the path adjacent to its last cell (one step in a random walk)

    @param      path        :   ordered list of cells in the path
    @optional   flow_index  :   index of flow the path is being made for

    @return                 :   path with added cell, or None if no cell could be added
    """

    # randomize which direction the next step is in from the last cell in the path
    step_directions = [ LEFT_DIRECTION, DOWN_DIRECTION, RIGHT_DIRECTION, UP_DIRECTION ]
    shuffle(step_directions)

    # choose a cell in a direction that meets requirements
    for direction in step_directions:
        next_cell = next[direction](*path[-1])

        # the next cell needs to:
        # 1) be in the grid
        # 2) unoccupied
        # 3) if flow is given, have a flow degree < 2

        if inGrid(grid, next_cell) and isEmpty(grid, next_cell):
            if flow_index == None or flowDegree(grid, next_cell, flow_index) < 2:
                return path + [ next_cell ]

    # if we reach here, no cell could be added to the path
    return None

def chooseEndpoint(grid):
    """
    find a random point on the grid with adjacent empty cells

    @param  grid    :   grid of the endpoint

    @return         :   random available point, or None if there are none
    """

    available = []
    for i in range(grid.cols):
        for j in range(grid.rows):
            if isEmpty(grid, [i, j]) and degree(grid, [i, j]) < 4:
                available.append([i, j])

    if available == []:
        return None
    else:
        return available[ floor(random() * len(available)) ]
