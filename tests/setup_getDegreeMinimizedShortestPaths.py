from context import Grid
import copy

FAILURE_MESSAGE = "Incorrect path generated"

"""
helper functions for getDegreeMinimizedShortestPaths() test cases
"""

def getGrid(rows, cols):
    """
    create a grid with the given number of columns/rows; the grid is not
    meant to be actually drawn, so we neglect attributes like position,
    color, and line thickness

    @param  rows    :   desired number of rows in the grid
    @param  cols    :   desired number of columns in the grid

    @return         :   Grid object with the desired characteristics
    """

    assert rows * cols > 0, "Either the desired number of rows or columns was 0"

    return Grid([0, 0], 0, 0, rows = rows, cols = cols)

def getPathsFromParents(source, parents):
    """
    form a mapping of the destination cell of a path to the path taken from
    the source as calculated by getDegreeMinimizedShortestPaths()

    @param  source  :   source cell of the generated paths
    @param  parents :   parents{} dictionary returned from
                        getDegreeMinimizedShortestPaths()

    @return         :   a dictionary mapping destination cells to paths (not
                        including the source cell)
    """

    assert parents[source] == None, "Given source cell " + str(source) + " is not the correct source"

    paths = {}
    for dest in parents.keys():
        paths[dest], current = [], dest
        while not current == source:
            paths[dest].append(current)

            assert not parents[current] == None, "No parent cell for " + str(current)

            current = parents[current]

        # paths are generated from destination cell to source, so path needs to be
        # reversed
        paths[dest].reverse()

    return paths
