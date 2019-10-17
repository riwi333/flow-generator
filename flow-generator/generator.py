from grid import Grid
from random import random, shuffle, seed, choices
from datetime import datetime
from math import floor, ceil
import direction

"""
functions for handling path generation

"""

# TODO:
#   -   randomize initial path and choice of source cell, making sure that degree(source)
#       is still minimzed
#
#   -   more unit tests!
#
#   -   figure out conditions to allow components of size 4 and 5 (not all components of
#       those sizes will make illegal paths, but right now the algorithm throws them out
#
#   -   find a way to measure the "uniqueness" of a given set of paths; the algorithm
#       should be able to generate several sets that are decently different from each other
#
#   -   actually write a README.md file for this
#
#   -   test algorithm on rectangular grids (i.e. 5x6, 9x11); alter the Grid class to
#       allow arbitrary grid shapes? (make a new branch for this)
#
#   -   try to implement Dial's algorithm again?
#

def getDegreeMinimizedPaths(grid, source):
    """
    find paths from the start cell to all reachable unoccupied cells in the grid with
    minimum total cells.degree()

    @param      grid        :   grid of the starting cell
    @param      source      :   starting cell we find paths for

    @return                 :   a dictionary giving the parent cell of each cell in its minimized path (or None if
                                the cell is unreachable)
    """

    # use Dijkstra's algorithm to find all SSSPs with w(u, v) = grid.degree(v)

    assert len(grid.unoccupied) > 0, "No unoccupied cells available"
    assert grid.isEmpty(source), "Source cell is already occupied"

    # set the maximum distance larger than any possible total degree of a path
    MAX_DISTANCE = 4 * len(grid.unoccupied)

    # initalize vertex "distances" (distance in this function refers to the sum
    # of the degrees of cells in paths from the source cell)
    distances = { cell : MAX_DISTANCE for cell in grid.unoccupied }
    distances[source] = 0

    # initialize list of unvisited cells (ignoring occupied cells)
    unvisited = list(grid.unoccupied)

    # initialize returned objects
    parents = { cell : None for cell in grid.unoccupied }

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

def getEmptyComponents(grid, empty=None):
    """
    perform a BFS to identify the connected components of empty cells in the grid

    @param      grid    :   grid containing the relevant cells
    @optional   empty   :   list of unoccupied cells to use *instead* of the grid's set of
                            unoccupied cells

    @return             :   list of lists of cells separated by components
    """

    if empty is None:
        unoccupied = list(grid.unoccupied)
    else:
        unoccupied = list(empty)

    assert len(unoccupied) > 0

    # initialize the queue and visited dictionary
    visited, queue, components = { cell : False for cell in unoccupied }, [], []

    # push the source cell of the first component into the queue
    queue.append(unoccupied[0])
    components.append([])

    while len(queue) > 0:
        # find all the cells in this current component
        while len(queue) > 0:
            # pop the first element out of the queue and add it to this component
            cell, visited[cell] = queue.pop(0), True
            components[-1].append(cell)

            # add neighbors of the popped cell that have not been visited to the queue
            for dir in direction.directions:
                neighbor = direction.next[dir](*cell)
                if grid.inBounds(neighbor) and grid.isEmpty(neighbor) and visited[neighbor] == False:
                    visited[neighbor] = True
                    queue.append(neighbor)

        # determine if there are any remaining unvisited cells; if so, put the first
        # one we find into a new component
        for cell in visited.keys():
            if visited[cell] == False:
                queue.append(cell)
                visited[cell] = True
                components.append([])
                break

        # if we reach this point and the queue is still empty, there are
        # no more unvisited empty cells, so we've found all the components

    return components

def generatePaths(grid):
    """
    randomly generate paths to create solved Flow puzzles

    @param  grid    :   grid the paths will be placed in

    @return         :   list containing all viable paths used to fill the grid
    """

    # TODO: make the first flow path a random walk instead of being calculated

    final_paths, index = [], 0

    tries = 0

    # seed the random generator
    seed(datetime.now())

    while len(grid.unoccupied) > 0 and tries < 100:
        # sort the empty cells in order of ascending degree
        sorted_unoccupied = sorted(grid.unoccupied, key = lambda cell : grid.degree(cell))

        """
        # DEBUG
        print("Path #" + str(index) + ":")
        print("Unoccupied: " + str(grid.unoccupied))
        """

        # choose a cell to start this path with
        attempts = 0
        while attempts < len(grid.unoccupied):
            # get the empty cell of lowest degree that we haven't tried yet (the "source" of this path)

            # TODO: randomize which lowest-degree cell we use; ex. if there's multiple 1-degree cells,
            # randomly choose one of them instead of whichever one gets sorted first in the empty list

            source = sorted_unoccupied[attempts]

            """
            # DEBUG
            print("Source: " + str(source))
            """

            # find all directed edges of paths from this source cell to other empty cells with minimum total degree;
            # also get a list of cells in the source's component block (not including the source)
            parents = getDegreeMinimizedPaths(grid, source)

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

            """
            # DEBUG
            print("Source component: " + str(block))
            print("Source component size: " + str(block_size))
            """

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

            # randomize a permutation of the minimized paths' sinks that attempts to given longer paths lesser indices
            sinks, randomized_sinks = list(minimized_paths.keys()), []
            for i in range(len(minimized_paths.keys())):
                # weigh the probability of choosing any path linearly by its length
                total_length = float(sum([ len(minimized_paths[sink]) for sink in sinks ]))
                weights = [ len(minimized_paths[sink]) / total_length for sink in sinks ]
                choice = choices(sinks, weights = weights, k = 1)[0]
                randomized_sinks.append(choice)
                sinks.remove(choice)

            """
            # DEBUG
            print([ len(minimized_paths[sink]) for sink in randomized_sinks ])
            """

            # test the randomized list of sinks until we find one that's legal length (at least 3 cells long) and fits
            # properly within the block
            chosen_sink = None
            for sink in randomized_sinks:
                path_length = len(minimized_paths[sink]) + 1

                # find out how many unoccupied cells would be left in the source's component if we used this
                # path next
                remaining_in_block = block_size - path_length

                assert remaining_in_block >= 0

                # the block the path resides in, if not empty, should have either 3 or at least 6 remaining unoccupied cells
                # NOTE: blocks of size 4, if arranged in a 2x2 square, cannot be filled legally; multiple arrangements of
                # blocks of size 5 also cannot be filled legally; blocks with at least 6 unoccupied cells, however can
                # always be filled legally
                if path_length >= 3 and (remaining_in_block == 0 or remaining_in_block == 3 or remaining_in_block >= 6):
                    satisfied = True

                    # test this path to see if occupying its cells will create illegal components
                    # NOTE: if the path fills its component (remaining_in_block' == 0) we  don't need to check for this
                    if remaining_in_block > 0:
                        test_empty = list(sorted_unoccupied)

                        # temporarily mark the cells in this path as occupied so we can find the resulting unoccupied components
                        test_empty.remove(source)
                        grid.setCell(source, index)
                        for cell in minimized_paths[sink]:
                            test_empty.remove(cell)
                            grid.setCell(cell, index)

                        # get the unoccupied components that would be made by this path
                        components = getEmptyComponents(grid, empty=test_empty)

                        """
                        # DEBUG
                        print("Testing path: " + str(minimized_paths[sink]))
                        print("Resulting components:")
                        for component in components:
                            print(component)
                        """

                        # see if the unoccupied components this path forms satisfies the 'remaining_in_block' rules
                        for component in components:
                            component_size = len(component)
                            if not (component_size == 0 or component_size == 3 or component_size >= 6):
                                satisfied = False
                                break

                        # unmark the cells of this path as occupied in the grid
                        grid.resetCell(source)
                        for cell in minimized_paths[sink]:
                            grid.resetCell(cell)

                    # if all the resulting components are legal, use this as the next path
                    if satisfied:
                        chosen_sink = sink
                        break

            # make sure at least one path is legal
            if not chosen_sink == None:
                # add the path with this sink to the list of calculated paths
                path = [ source ] + minimized_paths[sink]
                final_paths.append(path)

                """
                # DEBUG
                print("Path: " + str(path))
                print("Path length: " + str(len(path)))
                print("Resulting components:")
                for component in components:
                    print(component)
                """

                # remove all cells in the path from the list of unoccupied cells
                for cell in path:
                    assert grid.isEmpty(cell), "Final path cell " + str(cell) + " already occupied"

                    grid.setCell(cell, index)

                # update the path index and start the next path
                index += 1
                break

            # if none of the paths were legal, try a new source cell
            else:
                attempts += 1

            """
            # DEBUG
            print("\n")
            """

        tries += 1

    return final_paths

def simplify(grid, path1, path2):
    """
    determine whether the two paths in the grid can be properly combined, and if
    so combine them

    @param  grid    :   grid the paths are contained in
    @param  path1   :   first path we want to combine
    @param  path2   :   second path we want to combine

    @return         :   a combined path, or None if none were possible
    """

    # count how many times the paths are adjacent to each other
    pathSum = sum([ grid.pathDegree(cell, path2) for cell in path1 ])

    # if the paths are only adjacent once, check if the adjacent cells are
    # both endpoints; if so return the combined path
    if pathSum == 1:
        if direction.isAdjacent(path1[0], path2[0]):
            return path2[::-1] + path1
        if direction.isAdjacent(path1[0], path2[-1]):
            return path2 + path1
        if direction.isAdjacent(path1[-1], path2[0]):
            return path1 + path2
        if direction.isAdjacent(path1[-1], path2[-1]):
            return path2 + path1[::-1]

    return None

def simplifyPaths(grid, paths):
    """
    combine paths to minimize the overall number of paths in the grid

    @param  grid    :   grid the paths are contained in
    @param  paths   :   list of paths to simplify

    @return         :   reduced list of viable paths
    """

    # sort the paths by length so shorter paths are combined first
    simplified = sorted(paths, key = lambda p : len(p))

    # combine paths as many paths as possible
    while True:
        # iterate through pairs of paths until we find one that can be combined
        for path1 in simplified:
            for path2 in simplified:
                if not path1[0] == path2[0]:
                    combined = simplify(grid, path1, path2)

                    # if we can combine these paths, remove them from the list of
                    # reduced paths
                    if not combined == None:
                        simplified.remove(path1)
                        simplified.remove(path2)
                        break
            if not combined == None:
                break

        # add this combined path to the list of reduced paths
        if not combined == None:
            simplified.append(combined)
        else:
            break

    return simplified
