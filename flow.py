import pyglet
import graphics as graphics
import grid

class Flow:
    """
    class to represent and draw a single flow

    required attributes:
    --------------------
    @attribute grid     :   grid that flow belongs to
    @attribute color    :   3-tuple of the RGB values for the flow
    @attribute index    :   number assigned to this flow

    optional attributes (default value):
    ------------------------------------
    @attribute

    internal attributes:
    --------------------
    @attribute endpoints    :   2-tuple of 2-tuples the cell locations of the flow's endpoints
    @attribute path         :   list of cells the flow takes up, in drawing order
    @attribute flowBatch    :   batch to hold all of the flow's graphics (lines for the path
                                and circles for the endpoints)
    """


    def __init__(self, grid, color, index):
        """
        constructor for the Flow class

        See above "required attributes" and "optional" attributes list for parameters
        """

        self.grid = grid
        self.color = color
        self.index = index

        self.path = []
        self.flowBatch = pyglet.graphics.Batch()

    def addEndpoint(self, cell):
        """
        add the given endpoints to the flow

        @param cell :   2-tuple of 0-indexed (column, row) pair
        """

        # add the circles used to draw the endpoints to the flow's batch
        graphics.generateCircle(    self.grid.getCellCenter(cell),
                                    0.3 * min(*self.grid.getSpacing()),
                                    15,
                                    fill = True,
                                    batch = self.flowBatch,
                                    color = self.color  )

        # add the cell to the path and mark it with this Flow object
        self.path.append(cell)
        self.grid.values[cell] = self

    def addCell(self, next_cell):
        """
        add a cell to this flow's path (internally and drawing-wise)

        @param cell :   2-tuple of 0-indexed (column, row) pair
        """

        # get the cell we just left
        current_cell = self.path[-1]

        # draw a line between the last cell and this new cell add it to the batch
        graphics.generateLine(  self.grid.getCellCenter(current_cell),
                                self.grid.getCellCenter(next_cell),
                                color = self.color,
                                width = 5.0,                # the width should adjust with grid spacing
                                batch = self.flowBatch  )

        # add the cell to the path and mark it with this Flow object
        self.path.append(next_cell)
        self.grid.values[next_cell] = self

    def addPath(self, path):
        """
        add an ordered list of cells to the path

        @param  path    :   ordered list of cells (first and last are endpoints)
        """

        # ignore paths of length less than 3
        if len(path) < 2:
            return

        self.addEndpoint(path[0])
        self.addEndpoint(path[-1])

        for i in range(1, len(path) - 1):
            self.addCell(path[i])

    def draw(self):
        """
        draw the flow (endpoints and path) using its batch

        """

        self.flowBatch.draw()
