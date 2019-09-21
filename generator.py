from grid import Grid
from flow import Flow
from random import random, shuffle, seed
from datetime import datetime
from math import floor, ceil
import cells
import itertools

"""
functions for handling flow generation

"""

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
            next_cell = cells.next[direction](*current)
            if cells.inGrid(grid, next_cell) is True and cells.isEmpty(grid, next_cell) is True and visited[ next_cell[0] ][ next_cell[1] ] is False:
                visited[ next_cell[0] ][ next_cell[1] ] = True
                parents[ next_cell[0] ][ next_cell[1] ] = current
                queue.append(next_cell)

    return parents

def getDegreeMinimizedShortestPaths(grid, cell):
    """
    find the shortest paths from the start cell to all reachable unoccupied cells in the grid with
    minimum total cells.emptyDegree()

    @param  grid    :   grid of the starting cell
    @param  cell    :   starting cell we find paths for

    @return         :   a tuple of 1) a 2D list of the parent cell of each cell in its shortest path and
                        2) the number of reachable cells from the starting cell (the number of cells in
                        its component, not including itself)
    """

    # Dial's algorithm; emptyDegree() edge weights

    pass

def randomStep(grid, path, last_direction=None, flow_index=None):
    """
    add a cell to the path adjacent to its last cell (one step in a random walk)

    @param      grid            :   grid the path is contained in
    @param      path            :   ordered list of cells in the path
    @optional   last_direction  :   last direction the walk traveled in
    @optional   flow_index      :   index of flow the path is being made for

    @return                     :   2-tuple of path with added cell and the
                                    direction traveled in (or the original path
                                    and None if no cell could be added)
    """

    # randomize which direction the next step is in from the last cell in the path
    step_directions = [ cells.LEFT_DIRECTION, cells.DOWN_DIRECTION, cells.RIGHT_DIRECTION, cells.UP_DIRECTION ]
    if not last_direction == None:
        del step_directions[(last_direction + 2) % 4]
    shuffle(step_directions)

    # choose a cell in a direction that meets requirements
    for direction in step_directions:
        next_cell = cells.next[direction](*path[-1])

        # the next cell needs to:
        # 1) be in the grid
        # 2) unoccupied
        # 3) if flow is given, have a flow degree < 2

        if cells.inGrid(grid, next_cell) and cells.isEmpty(grid, next_cell):
            if flow_index == None or cells.flowDegree(grid, next_cell, flow_index) < 2:
                return ( path + [ next_cell ], direction )

    # if we reach here, no cell could be added to the path
    return ( path, None )

def generateFlows(grid, n_flows):
    """
    randomly generate solved flow puzzles

    @param  grid    :   grid the flows will be placed on
    @param  n_flows :   number of flows to put on the grid

    @return         :   a tuple of 0) list containing all Flow()
                        objects, in order of index and 1) a list
                        of all the cell coordinate tuples that
                        are still unoccupied
    """

    GRID_SIZE = grid.cols

    flows, empty = [], list(itertools.product([i for i in range(GRID_SIZE)], repeat=2))

    # create the first Flow by random walking for a few steps
    flows.append(Flow(  grid,
                        color = [ floor(random() * 255) for x in range(3) ],
                        index = 0))

    path = [ empty[floor(random() * GRID_SIZE ** 2)] ]
    last_direction = None
    flows[0].addCell(path[0])

    for i in range(floor(GRID_SIZE * 1.5)):
        path, last_direction = randomStep(grid, path, last_direction=last_direction, flow_index=0)

        if last_direction == None:
            break
        else:
            flows[0].addCell(path[-1])

    return (flows, empty)
