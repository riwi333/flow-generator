import pyglet
import graphics as graphics
from grid import Grid
from flow import Flow
from random import random, shuffle, seed
from datetime import datetime
from math import floor, ceil

"""
functions for dealing with cells in grids

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

def emptyDegree(grid, cell):
    """
    find total number of unoccupied cells this (col, row) is adjacent with

    @param  grid    :   grid of the cell
    @param  cell    :   2-tuple of 0-indexed (column, row) pair

    @return         :   number of adjacent unoccupied cells
    """

    deg = 0
    for direction in directions:
        next_cell = next[direction](*cell)
        if inGrid(grid, next_cell) and isEmpty(grid, next_cell):
            deg = deg + 1

    return deg

def adjacentDirection(cell1, cell2):
    """
    determine whether two given cells are adjacent or not

    @param  cell1   :   2-tuple of first cell's coordinates
    @param  cell2   :   2-tuple of second cell's coordinates

    @return         :   the direction needed to get from cell1 to cell2, or None
                        if they are not adjacent
    """

    for direction in directions:
        if next[direction](*cell1) == cell2:
            return direction

    return None
