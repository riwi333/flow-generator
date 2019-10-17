import setup_getDegreeMinimizedPaths as setup
from context import Grid, generator
import unittest
from ddt import ddt, data, unpack

# current known test cases (see test_cases() parameters for information)
cases = []
cases.append((  3,
                3,
                [ (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1) ],
                (1, 1),
                (2, 0),
                [ (1, 0), (2, 0) ]
            ))
cases.append((  5,
                5,
                [],
                (1, 3),
                (2, 0),
                [ (1, 2), (1, 1), (1, 0), (2, 0) ]
            ))
cases.append((  5,
                5,
                [ (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1) ],
                (0, 3),
                (2, 0),
                [ (0, 2), (0, 1), (0, 0), (1, 0), (2, 0) ]
            ))

@ddt
class Test_getDegreeMinimizedPaths(unittest.TestCase):
    """
    test the getDegreeMinimizedPaths() function for correctness
    """

    @data(*cases)
    @unpack
    def test_cases(self, rows, cols, occupied, source, dest, dmsp):
        """
        try a few known test cases to make sure the getDegreeMinimizedPaths()
        functions properly

        @param  rows        :   number of rows in grid used for the test case
        @param  cols        :   number of columns in grid used for the test case
        @param  occupied    :   cells marked as occupied for the test case
        @param  source      :   source cell for the test case
        @param  dest        :   destination cell for the test case
        @param  dmsp        :   desired degree-minimized path for the test case
                                (note that the dmsp does not include the source cell)
        """

        grid = setup.getGrid(rows, cols)
        for cell in occupied:
            grid.setCell(cell, True)

        parents = generator.getDegreeMinimizedPaths(grid, source)
        paths = setup.getPathsFromParents(source, parents)

        self.assertEqual(paths[dest], dmsp, setup.FAILURE_MESSAGE)

if __name__ == '__main__':
    unittest.main()
