import setup_getRandomPath as setup
from setup_getDegreeMinimizedPaths import getGrid
from context import Grid, generator, Flow
import unittest
from ddt import ddt, data, unpack
from random import random, choices
from math import ceil
import itertools

NUM_TESTS = 1000
MIN_ROWS = 4
MAX_ROWS = 20
MIN_COLS = 4
MAX_COLS = 20

# generate test cases by randomizing source cells
cases = []
for i in range(NUM_TESTS):
    rows = MIN_ROWS + ceil(random() * (MAX_ROWS - MIN_ROWS))
    cols = MIN_COLS + ceil(random() * (MAX_COLS - MIN_COLS))
    potential_sources = list(itertools.product(range(cols), range(rows)))

    # remove the corners of the grid from the list of potential sources
    potential_sources.remove((0, 0))
    potential_sources.remove((0, rows - 1))
    potential_sources.remove((cols - 1, 0))
    potential_sources.remove((cols - 1, rows - 1))

    source = choices(potential_sources)[0]

    cases.append(( rows, cols, source ))

@ddt
class Test_getRandomPath(unittest.TestCase):
    """
    test the getRandomPath() function to ensure its output paths are legal: must have
    a length of at least 3 and don't form components of size less than 6 (except 3)
    """

    @data(*cases)
    @unpack
    def test_cases(self, rows, cols, source):
        """
        run the test cases and test legality

        @param  rows        :   number of rows in grid used for the test case
        @param  cols        :   number of columns in grid used for the test case
        @param  source      :   source cell for the randomized path
        """

        grid = getGrid(rows, cols, origin = setup.GRID_ORIGIN, width = setup.GRID_WIDTH, height = setup.GRID_HEIGHT)
        path = generator.getRandomPath(grid, source)

        try:
            self.assertTrue(setup.testPathLegality(grid, path), setup.FAILURE_MESSAGE)

        # if the randomized path is illegal (assertion raised), show the illegal path in the grid
        except AssertionError:
            print("Source: " + str(source))
            setup.visualizePath(grid, path)
