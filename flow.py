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


    def __init__(self, grid, color):
        """
        constructor for the Flow class

        See above "required attributes" and "optional" attributes list for parameters
        """

        self.grid = grid
        self.color = color
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

        self.path.append(cell)

    def addCell(self, next_cell):
        # get the cell we just left
        current_cell = self.path[-1]

        # draw a line between the last cell and this new cell add it to the batch
        graphics.generateLine(  self.grid.getCellCenter(current_cell),
                                self.grid.getCellCenter(next_cell),
                                color = self.color,
                                width = 5.0,                # the width should adjust with grid spacing
                                batch = self.flowBatch  )

        self.path.append(next_cell)

    def draw(self):
        self.flowBatch.draw()