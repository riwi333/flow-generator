import pyglet
import graphics as graphics
import grid

# TODO: separate functions editing path from functions about drawing the flow
# there should be a single function drawFlow() that creates all vertex lists
# needed to draw the flow; the idea is that the path can be edited as needed,
# and then when the flow is finalized we can use drawFlow() to draw its
# permanent representation

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
    @attribute endpoints        :   2-tuple of 2-tuples the cell locations of the flow's endpoints
    @attribute path             :   list of cells the flow takes up, in drawing order
    @attribute flowBatch        :   batch to hold all of the flow's graphics (lines for the path
                                    and circles for the endpoints)
    @attribute pathLines        :   list of vertex lists used to draw the lines of the flow's path;
                                    pathLines[0] is the line between path[0] and path[1], etc.
    @attribute endpointCircles  :   list of vertex lists for the 0) first and 1) second endpoints'
                                    circles
    """


    def __init__(self, grid, color, index):
        """
        constructor for the Flow class

        See above "required attributes" and "optional" attributes list for parameters
        """

        self.grid = grid
        self.color = color
        self.index = index

        self.endpoints = []
        self.path = []
        self.flowBatch = pyglet.graphics.Batch()
        self.pathLines = []
        self.endpointCircles = []

    def addEndpoint(self, cell):
        """
        mark the given cell as an endpoint for this flow and add it to the path

        @param cell :   2-tuple of 0-indexed (column, row) pair
        """

        self.endpoints.append(cell)

        # add the cell to the path and mark the grid with this Flow object
        self.path.append(cell)
        self.grid.values[ cell[0] ][ cell[1] ] = self

    def addCell(self, next_cell):
        """
        add a cell to this flow's path

        @param cell :   2-tuple of 0-indexed (column, row) pair
        """

        # add the cell to the path and mark it with this Flow object
        self.path.append(next_cell)
        self.grid.values[ next_cell[0] ][ next_cell[1] ] = self

    def addPath(self, path):
        """
        add an ordered list of cells to the path

        @param  path    :   ordered list of cells (first and last are endpoints)
        """

        # ignore paths of length less than 3
        if len(path) < 2:
            return

        self.addEndpoint(path[0])

        for i in range(1, len(path)):
            self.addCell(path[i])

        self.addEndpoint(path[-1])

    def removeCell(self, cell):
        """
        remove the given cell (including endpoints) from the flow and its graphics batch

        @return     :   'cell' if cell exists in the flow path, and None otherwise
        """

        if cell in self.path:
            # if this cell is the first endpoint
            if cell == self.path[0]:
                self.path = self.path[1:]
                del self.endpoints[0]

            # if this cell is the second endpoint
            elif cell == self.path[-1]:
                self.path = self.path[1:]
                del self.endpoints[1]

            # if this cell is within the flow path
            else:
                index = self.path.index(cell)

                # need to remove the line from the previous cell pointing to this cell
                self.path = self.path[: index - 1] + self.path[index :]

            return cell
        else:
            return None

    def updateGraphics(self):
        """
        draw all graphics for the flow's endpoints and path cells and them to
        the flow's graphics batch

        """

        # add the circles used to draw the endpoints to the flow's batch
        self.endpointCircles.append(graphics.generateCircle(self.grid.getCellCenter(self.endpoints[0]),
                                                            0.3 * min(*self.grid.getSpacing()),
                                                            15,
                                                            fill = True,
                                                            batch = self.flowBatch,
                                                            color = self.color  ))

        self.endpointCircles.append(graphics.generateCircle(self.grid.getCellCenter(self.endpoints[1]),
                                                            0.3 * min(*self.grid.getSpacing()),
                                                            15,
                                                            fill = True,
                                                            batch = self.flowBatch,
                                                            color = self.color  ))

        # add the lines used to draw the flow's path to the flow's batch
        for i in range(0, len(self.path) - 1):
            # draw a line between the current cell and the next cell
            self.pathLines.append(graphics.generateLine(self.grid.getCellCenter(self.path[i]),
                                                        self.grid.getCellCenter(self.path[i+1]),
                                                        color = self.color,
                                                        width = 5.0,
                                                        batch = self.flowBatch  ))

    def draw(self):
        """
        draw the flow (endpoints and path) using its batch

        """

        self.flowBatch.draw()
