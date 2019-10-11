from grid import Grid
from flow import Flow
from random import random, shuffle, seed, choice
from datetime import datetime
from math import floor, ceil
import direction

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

    @return             :   a dictionary giving the parent cell of each cell in its shortest path (or None if
                            the cell is unreachable)
    """

    # use Dijkstra to find all SSSPs with w(u, v) = grid.degree(v)

    assert not empty == [], "No unoccupied cells available"
    assert grid.isEmpty(source), "Source cell is already occupied"

    # set the maximum distance larger than any possible total degree of a path
    MAX_DISTANCE = 4 * len(empty)

    # initalize vertex "distances" (distance in this function refers to the sum
    # of the degrees of cells in paths from the source cell)
    distances = { cell : MAX_DISTANCE for cell in empty }
    distances[source] = 0

    # initialize list of unvisited cells (ignoring occupied cells)
    unvisited = list(empty)

    # initialize returned objects
    parents = { cell : None for cell in empty }

    while len(unvisited) > 0:
        min_distance = MAX_DISTANCE + 1
        min_cell = None

        # find the cell with minimum calculated distance from the source
        for cell in unvisited:
            if distances[cell] < min_distance:
                min_distance, min_cell = distances[cell], cell

        # mark this cell as visited
        unvisited.remove(min_cell)

        # iterate through all neighbors of the minimum-distance cell
        for dir in direction.directions:
            adj_cell = direction.next[dir](*min_cell)

            if grid.inBounds(adj_cell) and grid.isEmpty(adj_cell) and adj_cell in unvisited:
                # if we can reach this neighbor cell "faster" (with lesser total degree) via the current
                # minimum-distance cell, update the neighbor's cell distance and make the minimum-distance
                # cell its parent
                if distances[adj_cell] > distances[min_cell] + grid.degree(adj_cell):
                    distances[adj_cell] = distances[min_cell] + grid.degree(adj_cell)
                    parents[adj_cell] = min_cell

    return parents

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

    flows, empty, index = [], grid.getAllCellCoordinates(), 0

    # DEBUG
    tries = 0

    while len(empty) > 0 and tries < 20:
        # sort the empty cells in order of ascending degree
        empty.sort( key = lambda cell : grid.degree(cell) )

        """
        # DEBUG
        print("Unoccupied: " + str(empty))
        """

        # choose a cell to start this flow with
        attempts = 0
        while attempts < len(empty):
            # get the empty cell of lowest degree that we haven't tried yet (the "source" of this flow)
            source = empty[attempts]

            """
            # DEBUG
            print("Source: " + str(source))
            """

            # find all directed edges of paths from this source cell to other empty cells with minimum total degree;
            # also get a list of cells in the source's component block (not including the source)
            parents = getDegreeMinimizedShortestPaths(grid, empty, source)

            """
            # DEBUG
            print("Parents:")
            for cell in parents.keys():
                print(str(cell) + ": " + str(parents[cell]))
            """

            # find which cells are within this source's component block (NOT including the source)
            block = []
            for cell in parents.keys():
                # if the parent of this cell is 'None', then the source cannot reach it
                if not parents[cell] == None:
                    block.append(cell)

            block_size = len(block) + 1

            # find all the minimized paths from this source cell by following the edges (note that the generated paths
            # do not include the source)
            minimized_paths = {}
            for cell in block:
                minimized_paths[cell], current = [], cell
                while not current == source:
                    minimized_paths[cell].append(current)

                    assert not parents[current] == None, "No parent cell for " + str(current)

                    current = parents[current]

                # since we follow each path from the sink to the source, we need to reverse the current paths
                minimized_paths[cell].reverse()

            """
            # DEBUG
            print("Minimized paths:")
            for sink in minimized_paths.keys():
                print(str(sink) + ": " + str(minimized_paths[sink]))
            """

            # find which sinks are of legal length (at least 3 cells long) and fit properly within the block
            potential_sinks = []
            for sink in minimized_paths.keys():
                path_length = len(minimized_paths[sink]) + 1

                # find out how many unoccupied cells would be left in the source's component if we used this
                # path for the next flow
                remaining_in_block = block_size - path_length

                # the block the flow resides in, if not empty, should have either 3 or at least 6 remaining unoccupied cells
                # NOTE: blocks of size 4, if arranged in a 2x2 square, cannot be filled legally; multiple arrangements of
                # blocks of size 5 also cannot be filled legally; blocks with at least 6 unoccupied cells, however can
                # always be filled legally
                if path_length >= 3 and (remaining_in_block == 0 or remaining_in_block == 3 or remaining_in_block >= 6):
                    # TODO: check if occupying the cells in this path will increase the number of components of unoccupied
                    # cells; each block should be of a size following the same rules as 'remaining_in_block'

                    potential_sinks.append(sink)

            # make sure at least one path is legal
            if len(potential_sinks) > 0:
                # randomly choose a path that works and create the flow for it

                # TODO: weight each path's probability of being chosen so that longer
                # paths are more likely to be used

                sink = choice(potential_sinks)
                path = [ source ] + minimized_paths[sink]
                flows.append(Flow(  grid,
                                    color = [ floor(random() * 256) for x in range(3) ],
                                    index = index,
                                    path = path ))

                """
                # DEBUG
                print("Path: " + str(path))
                """

                # remove all cells in the path from the list of unoccupied cells
                for cell in path:
                    assert cell in empty, "Final path cell " + str(cell) + " already occupied"

                    empty.remove(cell)

                # update the flow index and start the next flow
                index += 1
                break

            # if none of the paths were legal, try a new source cell
            else:
                attempts += 1

            """
            # DEBUG
            print("\n")
            """

        # DEBUG
        tries += 1

    return (flows, empty)

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
    step_directions = list(direction.directions)
    if not last_direction == None:
        del step_directions[(last_direction + 2) % 4]
    shuffle(step_directions)

    # choose a cell in a direction that meets requirements
    for dir in step_directions:
        next_cell = direction.next[dir](*path[-1])

        # the next cell needs to:
        # 1) be in the grid
        # 2) unoccupied
        # 3) if flow is given, have a flow degree < 2

        if grid.inBounds(next_cell) and grid.isEmpty(next_cell):
            if flow_index == None or grid.valueDegree(next_cell, flow_index) < 2:
                return ( path + [ next_cell ], dir )

    # if we reach here, no cell could be added to the path
    return ( path, None )
