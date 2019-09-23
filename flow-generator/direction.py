"""
constants and functions to deal with directioning

"""

# constants for mapping directions to numbers
LEFT_DIRECTION = 0
DOWN_DIRECTION = 1
RIGHT_DIRECTION = 2
UP_DIRECTION = 3

directions = [ LEFT_DIRECTION, DOWN_DIRECTION, RIGHT_DIRECTION, UP_DIRECTION ]

# lambda functions to produce adjacent cell coordinates depending on direction
# x is the column of the cell, and y is the row
next = {
    LEFT_DIRECTION  :   lambda x, y   : (x - 1, y),
    DOWN_DIRECTION  :   lambda x, y   : (x, y - 1),
    RIGHT_DIRECTION :   lambda x, y   : (x + 1, y),
    UP_DIRECTION    :   lambda x, y   : (x, y + 1)
}

# constants for differentiating the head and tail of a path
HEAD = 0
TAIL = 1

def adjacentDirection(cell1, cell2):
    """
    determine whether two given cells are adjacent or not

    @param  cell1   :   2-tuple of first cell's coordinates
    @param  cell2   :   2-tuple of second cell's coordinates

    @return         :   the direction needed to get from cell1 to cell2, or None
                        if they are not adjacent
    """

    for dir in directions:
        if next[dir](*cell1) == cell2:
            return dir

    return None
