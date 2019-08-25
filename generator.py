import pyglet
import graphics as graphics
from grid import Grid
from flow import Flow
from random import random, shuffle, seed
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
            if inGrid(grid, next_cell) is True and isEmpty(grid, next_cell) is True and visited[ next_cell[0] ][ next_cell[1] ] is False:
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

    # seed the random generator
    seed(datetime.now())

    # we assume the grid is square (# cols = # rows)
    grid_size = grid.cols

    # list of grid's Flow objects and the index of the flow we're creating
    flows, index = [], 0

    # list of all the currently unoccupied cells in the grid
    empty = []
    for i in range(grid_size):
        for j in range(grid_size):
            empty.append([i, j])

    for n in range(n_flows):
        # if all the cells in this grid are already taken, stop creating flows
        if len(empty) == 0:
            break

        # create a new Flow object of random color
        flows.append(Flow(  grid,
                            [ floor(random() * 255) for x in range(3) ],
                            index   ))

        # print("Creating flow #" + str(index))

        """
        # find a working endpoint to start with
        start = generator.chooseEndpoint(grid)
        print("Start point: " + str(start))
        if start == None:
            break
        """

        start = None

        # see if there are any unoccupied cells of degree 1: it has to be
        # an endpoint of some flow in order to fill the grid, so let's just make
        # it the starting point of this one
        for cell in empty:
            if isEmpty(grid, cell) is True and emptyDegree(grid, cell) == 1:
                start = cell
                break

        # if there are no empty cells with degree 1, randomly choose a cell to start with
        if start == None:
            start = empty[ floor(random() * len(empty)) ]

        # find all shortest paths from this endpoint to all reachable cells in the grid
        shortestPaths = getAllShortestPaths(grid, start)

        # print(shortestPaths)

        # choose a distance we want to aim for in a shortest path
        distance_goal = floor(random() * 2 * float(len(empty)) / grid_size) + 3

        # print("Distance goal: " + str(distance_goal))

        # find a shortest path with distance as close to the goal as possible
        closest_distance_path = []
        closest_distance = grid_size ** 2   # needs to be greater than max shortest distance

        for i in range(grid_size):
            for j in range(grid_size):
                cell, path, distance = [i, j], [], 0
                path.append(cell)

                # keep moving along parent cells until we get back to the start cell
                while not cell == start:
                    cell = shortestPaths[ cell[0] ][ cell[1] ]

                    # if shortestPaths() gives None, this cell is not reachable
                    if cell == None:
                        break

                    path.append(cell)
                    distance = distance + 1

                if cell == None:
                    continue

                # see if this path has a distance close to our goal
                if abs(distance_goal - distance) < abs(distance_goal - closest_distance):
                    closest_distance_path = path
                    closest_distance = distance

        # if this path only has a length of 1, there were no reachable cells from the
        # starting point, so delete this flow (*most likely*, this means that no other
        # flows can fit into the grid)
        # we also reject paths of length 2, since the minimum legal path length is 3
        if len(closest_distance_path) < 3:
            del flows[-1]
            continue

        # since paths are searched backwards, reverse the best path
        closest_distance_path.reverse()

        # print("Closest path: " + str(closest_distance_path))
        # print("Actual distance: " + str(closest_distance))

        """
        # all flows must have a length of at least 3
        if closest_distance < 3:
            # print("Flow failed")
            # empty.append(start)
            del flows[-1]
            continue
        """

        # print(closest_distance_path)
        # print("")

        # update the grid with this flow's shortest distance path
        for cell in closest_distance_path:
            grid.values[ cell[0] ][ cell[1] ] = flows[index]
            empty.remove(cell)

        # print(empty)

        # random walk for a few steps after the shortest path (# of steps should
        # vary with # of flows)
        full_path = closest_distance_path

        walk_steps = floor(random() * float(len(empty)) / grid_size)

        for i in range(walk_steps):
            next_path = randomStep(grid, full_path, flow_index = index)

            if next_path == None:
                break
            else:
                # update the complete path and the grid
                full_path = next_path
                grid.values[ full_path[-1][0] ][ full_path[-1][1] ] = flows[index]
                empty.remove([ full_path[-1][0], full_path[-1][1] ])

        # print("Max random steps: " + str(walk_steps))
        # print("Full path: " + str(full_path))

        flows[index].addPath(full_path)

        index = index + 1

    return ( flows, empty )
