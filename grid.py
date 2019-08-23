import pyglet
import graphics as graphics

class Grid:
    """
    class to represent and draw grids

    required attributes:
    --------------------
    @attribute  origin      :   tuple of x- and y- coordinates of bottom left corner of grid
    @attribute  width       :   total width of grid
    @attribute  height      :   total height of grid
    @attribute  rows        :   number of rows in the grid
    @attribute  cols        :   number of columns in the grid

    optional attributes (default value):
    ------------------------------------
    @attribute  color       :   3-tuple of the RGB value to color the grid lines with (255, 255, 255)
    @attribute  thickness   :   width of grid lines (1.0)
    @attribute  label       :   boolean of whether rows and columns of the grid should be labelled (False)
    @attribute  alpha       :   boolean of whether columns should be labelled with letters A-Z or not (False)
    @attribute  labelColor  :   4-tuple of RGBA value to color row/colum labels with (255, 255, 255, 255)

    internal attributes:
    -------------------
    @attribute  batch       :   batch of all lines generated to create grid
    @attribute  labelBatch  :   batch of all labels generated for the grid
                                (None if the grid is unlabelled)
    @attribute  values      :   optional mapping of grid cells to some set of values
    """

    @staticmethod
    def generateGrid(origin, width, height, rows, cols, color=(255, 255, 255), thickness=1.0):
        """
        generate a batch of vertex lists for lines to draw a grid

        @param origin           :   tuple of x- and y-coordinates of bottom left corner of grid
        @param width            :   total width of grid
        @param height           :   total height of grid
        @param rows             :   number of rows in the grid
        @param cols             :   number of columns in the grid
        @optional color         :   3-tuple of the RGB value to color the grid with
        @optional thickness     :   thickness of grid lines

        @return                 :   'vertex_list' object used to draw generated grid
        """

        # create the batch of vertex lists used to draw the grid
        grid = pyglet.graphics.Batch()

        # TODO: the top and bottom horizontal lines should be treated specially;
        #       grids with thick lines appear to miss their corners

        # generate all the horizontal lines in the grid
        for i in range(rows + 1):
            # calculate the number of empty pixels between each row's grid line
            # TODO: incorporate thickness into calculation
            vertical_space = float(height) / rows

            graphics.generateLine(  [ origin[0], origin[1] + i * vertical_space ],
                                    [ origin[0] + width, origin[1] + i * vertical_space ],
                                    color=color, width=thickness, batch=grid    )

        # generate all the vertical lines in the grid
        for i in range(cols + 1):
            # calculate the number of empty pixels between each column's grid line
            # TODO: incorporate thickness into calculation
            horizontal_space = float(width) / cols

            graphics.generateLine(  [ origin[0] + i * horizontal_space, origin[1] ],
                                    [ origin[0] + i * horizontal_space, origin[1] + height ],
                                    color=color, width=thickness, batch=grid    )

        return grid

    def __init__(self, origin, width, height, rows, cols, color=(255, 255, 255), thickness=1.0, label=False, alpha=False, labelColor=(255, 255, 255, 255)):
        """
        constructor for Grid class

        See class docstring for parameters
        """

        # TODO: width and height should vary with window size (if window has been
        #       resized, find by what ratios and multiply the existing grid width
        #       and height by them)

        self.origin = origin
        self.width = width      # TODO: need to adjust for thickness
        self.height = height    # TODO: need to adjust for thickness
        self.rows = rows
        self.cols = cols
        self.color = color
        self.thickness = thickness

        # get the batch of the grid for drawing
        self.batch = Grid.generateGrid(self.origin, self.width, self.height, self.rows, self.cols, color=self.color, thickness=self.thickness)

        # get the batch of grid labels, if requested (otherwise labelBatch is None)
        self.label = label
        self.alpha = alpha
        self.labelColor = labelColor
        self.labelBatch = self.generateLabels(self.labelColor)

        # initialize the cell-value mapping (all un-assigned by being set to None)
        self.values = [ [ None for x in range(self.cols) ] for y in range(self.rows) ]

    def draw(self):
        """
        draw the grid using its vertex list

        """

        self.batch.draw()

        # draw the grid's labels, if it has any
        if self.label is True:
            self.labelBatch.draw()

    def getCellCenter(self, cell):
        """
        get the coordinates of the center of the cell at (col, row)

        @param cell :   2-tuple of 0-indexed (column, row) pair

        @return     :   2-tuple of x- and y-coordinates of the cell's center in the window
        """

        center_x = self.origin[0] + float(self.width) / self.cols * (cell[0] + 0.5)
        center_y = self.origin[1] + float(self.height) / self.rows * (cell[1] + 0.5)

        return [ center_x, center_y ]

    def getSpacing(self):
        """
        get the horizontal and vertical spacing between cells in the grid

        @return :   2-tuple with the width and height of the grid's cells in pixels, respectively
        """

        return [ float(self.width) / self.cols, float(self.height) / self.rows ]

    def generateLabels(self, labelColor):
        """
        generate a batch of labels for cells along the left and top sides of the grid
        if self.alpha = True, columns are labelled with capital letters (A, B, C, ...)
        otherwise, both rows and columns are numbered

        @param labelColor   :   4-tuple of RGBA value to color row/colum labels with

        @return             :   batch of pyglet.window.Label objects for the labels
        """

        if self.label is False:
            return None

        labelBatch = pyglet.graphics.Batch()

        # positioning for column/row labels
        horizontal_space = float(self.width) / self.cols
        vertical_space = float(self.height) / self.rows

        # shortest distance between the edge of the grid and the label
        label_space = min(horizontal_space, vertical_space) / 4

        # find the position of the first column label, taking line thickness into account
        col_pos = self.getCellCenter([0, self.rows - 1])
        col_pos[1] = col_pos[1] + 0.5 * vertical_space + self.thickness + label_space

        # find the position of the first row label, taking line thickness into account
        row_pos = self.getCellCenter([0, 0])
        row_pos[0] = row_pos[0] - 0.5 * horizontal_space - self.thickness - label_space

        # create labels for the columns
        for i in range(self.cols):
            if self.alpha is True:
                text = chr(65 + i)
            else:
                text = str(i + 1)

            pyglet.text.Label(  text,
                                font_name = 'Times New Roman',
                                font_size = 10,     # TODO: this should adjust with grid size
                                x = col_pos[0],
                                anchor_x = 'left',
                                y = col_pos[1],
                                anchor_y = 'bottom',
                                color = labelColor,
                                batch = labelBatch  )

            col_pos[0] = col_pos[0] + horizontal_space

        # create labels for the rows
        for i in range(self.rows):
            text = str(i + 1)

            # TODO: for some reason the row labels aren't completely centered vertically
            pyglet.text.Label(  text,
                                font_name = 'Times New Roman',
                                font_size = 10,     # TODO: this should adjust with grid size
                                x = row_pos[0],
                                anchor_x = 'left',
                                y = row_pos[1],
                                anchor_y = 'bottom',
                                color = labelColor,
                                batch = labelBatch  )

            row_pos[1] = row_pos[1] + vertical_space

        return labelBatch

    def getCellLabel(self, cell):
        """
        get the text of the label for this cell

        @param cell     : 2-tuple of 0-indexed (column, row) pair

        @return         :   text of the label covering cell (col, row); if there
                            is no label, an empty string is returned
        """
        if not self.label is True:
            return ""

        elif self.alpha is True:
            return chr(65 + cell[0]) + str(cell[1] + 1)

        else:
            return str(cell[0] + 1) + "-" + str(cell[1] + 1)
