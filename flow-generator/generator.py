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

def getDegreeMinimizedShortestPaths(grid, empty, source):
    """
    find the shortest paths from the start cell to all reachable unoccupied cells in the grid with
    minimum total cells.emptyDegree()

    @param  grid        :   grid of the starting cell
    @param  empty       :   list of all tuples of unoccupied cells in this grid
    @param  source      :   starting cell we find paths for
    @param

    @return             :   a tuple of 1) a 2D list of the parent cell of each cell in its shortest path and
                            2) the number of reachable cells from the starting cell (the number of cells in
                            its component, not including itself)
    """

    # use Dijkstra to find all SSSPs with w(u, v) = cells.emptyDegree(v)

    MAX_DISTANCE = grid.cols ** 2

    # initalize vertex distances
    distances = { cell : MAX_DISTANCE for cell in empty }
    distances[source] = 0

    # initialize list of unvisited cells (ignoring occupied cells)
    unvisited = list(empty)
    for cell in unvisited:
        if not cells.isEmpty(grid, cell):
            queue.remove(cell)

    parents = { cell : None for cell in cells.permutate(grid.cols) }
    block_size = 0

    while len(unvisited) > 0:
        min_distance = MAX_DISTANCE + 1
        min_cell = None
        for cell in unvisited:
            if distances[cell] < min_distance:
                min_distance = distances[cell]
                min_cell = cell

        unvisited.remove(min_cell)

        for direction in cells.directions:
            adj_cell = cells.next[direction](*min_cell)
            if cells.inGrid(grid, adj_cell) and cells.isEmpty(grid, adj_cell):
                if distances[adj_cell] > distances[min_cell] + cells.emptyDegree(grid, adj_cell):
                    distances[adj_cell] = distances[min_cell] + cells.emptyDegree(grid, adj_cell)

                    if parents[adj_cell] == None:
                        block_size = block_size + 1

                    parents[adj_cell] = min_cell

    return ( parents, block_size )

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

    # we assume the grids are square, so grid.cols == grid.rows
    GRID_SIZE = grid.cols

    flows, empty = [], list(itertools.product([i for i in range(GRID_SIZE)], repeat=2))

    # print(empty)

    # create the first Flow by random walking for a few steps
    flows.append(Flow(  grid,
                        color = [ floor(random() * 255) for x in range(3) ],
                        index = 0))

    path, last_direction = [ empty[floor(random() * GRID_SIZE ** 2)] ], None
    flows[0].addCell(path[0])

    for i in range(floor(GRID_SIZE * 1.2)):
        path, last_direction = randomStep(grid, path, last_direction=last_direction, flow_index=0)

        if last_direction == None:
            break
        else:
            flows[0].addCell(path[-1])

    # mark the used cells as occupied
    for cell in path:
        empty.remove(tuple(cell))

    index = 1
    for x in range(5 * GRID_SIZE):
        # get all empty cells adjacent to occupied cells
        front = []
        for cell in empty:
            for direction in cells.directions:
                next_cell = cells.next[direction](*cell)
                if cells.inGrid(grid, next_cell) and not cells.isEmpty(grid, next_cell):
                    front.append(cell)
                    break

        # print(front)
        # print("")

        endpoints = []
        for cell in front:
            if cells.emptyDegree(grid, cell) == 1:
                endpoints.append(cell)
                break

        if len(endpoints) > 0:
            endpoint1 = endpoints.pop(floor(random() * len(endpoints)))
        else:
            endpoint1 = front[floor(random() * len(front))]

        parents, block_size = getDegreeMinimizedShortestPaths(grid, empty, endpoint1)

        # print(endpoint1)
        # print(parents)

        shortestPaths = { cell : None for cell in cells.permutate(GRID_SIZE) }
        for cell in shortestPaths.keys():
            if not parents[cell] == None:
                path = [ cell ]
                parent = parents[cell]
                while not parent == None:
                    path.append(parent)
                    parent = parents[ parent ]

                if path[-1] == endpoint1:
                    shortestPaths[cell] = path

        """
        for key, value in shortestPaths.items():
            if not value == None:
                print(str(key) + ": " + str(value))
        """

        endpoint2 = None
        while len(endpoints) > 0 and endpoint2 == None:
            endpoint2 = endpoints[floor(random() * len(endpoints))]
            if shortestPaths[endpoint2] == None or len(shortestPaths[endpoint2]) < 3:
                endpoints.remove(endpoint2)
                endpoint2 = None

        if endpoint2 == None:
            for cell in front:
                if not shortestPaths[cell] == None:
                    length = len(shortestPaths[cell])
                    remainder = block_size - length
                    if length >= 3 and (remainder == 0 or remainder == 3 or remainder >= 6):
                            endpoint2 = cell
                            break

        if endpoint2 == None or shortestPaths[endpoint2] == None:
            continue

        flows.append(Flow(  grid,
                            color = [ floor(random() * 255) for x in range(3) ],
                            index = index))

        for cell in shortestPaths[endpoint2]:
            flows[index].addCell(cell)
            empty.remove(cell)

        index = index + 1

    return (flows, empty)
