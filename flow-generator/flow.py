import pyglet
import graphics
import grid
import direction

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
    @attribute path             :   list of cells the flow takes up, in drawing order
    @attribute flowBatch        :   batch to hold all of the flow's graphics (lines for the path
                                    and circles for the endpoints)
    @attribute pathLines        :   list of vertex lists used to draw the lines of the flow's path;
                                    pathLines[0] is the line between path[0] and path[1], etc.
    @attribute endpointCircles  :   list of vertex lists for the 0) first and 1) second endpoints'
                                    circles
    """

    def __init__(self, grid, color, index, path=[]):
        """
        constructor for the Flow class

        See above "required attributes" and "optional" attributes list for parameters
        """

        self.grid = grid
        self.color = color
        self.index = index

        self.path = path
        for cell in self.path:
            self.grid.values[cell] = self.index

        self.flowBatch = pyglet.graphics.Batch()
        self.pathLines = []
        self.endpointCircles = [ None, None ]

    def addCell(self, next_cell, side=direction.HEAD):
        """
        add a cell to this flow's path

        @param      cell    :   2-tuple of 0-indexed (column, row) pair
        @optional   side    :   0 to add cell to the head of the path, 1 to
                                add cell to the tail of the path
        """

        # add the cell to the path and mark it with this Flow object's index in the grid
        if side == direction.HEAD:
            self.path.append(next_cell)
        elif side == direction.TAIL:
            self.path = [ next_cell ] + self.path
        else:
            raise Exception("Invalid 'side' parameter given")

        self.grid.values[next_cell] = self.index

    def removeCell(self, cell):
        """
        remove the given cell from the flow and its graphics batch

        @param  cell    :   2-tuple of 0-indexed (column, row) pair

        @return         :   'cell' if cell exists in the flow path, and None otherwise
        """

        if cell in self.path:
            index = self.path.index(cell)
            self.path = self.path[: index] + self.path[(index + 1) :]

            self.grid.values[cell] = None

            return cell

        else:
            return None

    def resetGraphics(self):
        """
        delete all of the current graphics for this flow

        """

        if not self.endpointCircles[0] == None:
            self.endpointCircles[0].delete()

        if not self.endpointCircles[1] == None:
            self.endpointCircles[1].delete()

        for i in range(len(self.pathLines) - 1):
            self.pathLines[i].delete()

    def updateGraphics(self):
        """
        draw all graphics for the flow's endpoints and path cells and them to
        the flow's graphics batch

        """

        self.resetGraphics()
        self.pathLines = [ None for i in range(len(self.path) - 1) ]

        # add the circles used to draw the endpoints to the flow's batch
        if len(self.path) > 0:
            self.endpointCircles[0] = graphics.generateCircle(  self.grid.getCellCenter(self.path[0]),
                                                                0.3 * min(*self.grid.getSpacing()),
                                                                15,
                                                                fill = True,
                                                                batch = self.flowBatch,
                                                                color = self.color  )

        if len(self.path) > 1:
            self.endpointCircles[1] = graphics.generateCircle(  self.grid.getCellCenter(self.path[-1]),
                                                                0.3 * min(*self.grid.getSpacing()),
                                                                15,
                                                                fill = True,
                                                                batch = self.flowBatch,
                                                                color = self.color  )

        # add the lines used to draw the flow's path to the flow's batch
        for i in range(len(self.path) - 1):
            # draw a line between the current cell and the next cell
            self.pathLines[i] = graphics.generateLine(  self.grid.getCellCenter(self.path[i]),
                                                        self.grid.getCellCenter(self.path[i+1]),
                                                        color = self.color,
                                                        width = 5.0,
                                                        batch = self.flowBatch  )

    def draw(self):
        """
        draw the flow (endpoints and path) using its batch

        """

        self.flowBatch.draw()
