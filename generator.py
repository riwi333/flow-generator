import pyglet
import graphics as graphics
from grid import Grid
from flow import Flow
from random import random, seed, shuffle
from datetime import datetime
from math import floor, ceil

"""
randomly generate solved flow puzzles

"""

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
GRID_SIZE = 5

# functions to add length to current coordinates depending on direction
add = [     lambda x, y   : [x - 1, y],
            lambda x, y   : [x, y - 1],
            lambda x, y   : [x + 1, y],
            lambda x, y   : [x, y + 1]    ]

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

cells = [ [ -1 for y in range(GRID_SIZE) ] for x in range(GRID_SIZE) ]

# return the index of the flow at this cell
def cellFlow(cell):
    return cells[ cell[0] ][ cell[1] ]

def isEmpty(cell):
    return cellFlow(cell) == -1

# boolean of whether this (col, row) tuple is in the grid
def cellInGrid(cell, grid):
    if 0 <= cell[0] < grid.cols:
        if 0 <= cell[1] < grid.rows:
            return True

    return False

# number of flow cells adjecent to this cell
def degree(cell, grid, flow):
    deg = 0
    for func in add:
        next_cell = func(*cell)
        if cellInGrid(next_cell, grid) and cells[ next_cell[0] ][ next_cell[1] ] == flow:
            deg = deg + 1

    return deg


# TODO: make sure paths only go into empty cells
def bfs(start, grid):
    global distances, visited, parents

    Q = [ start ]
    visited[ start[0] ][ start[1] ] = True
    parents[ start[0] ][ start[1] ] = start

    while not Q == []:
        cell = Q.pop(0)

        for i in range(4):
            next_cell = add[i](*cell)
            if cellInGrid(next_cell, grid) and isEmpty(next_cell) and visited[ next_cell[0] ][ next_cell[1] ] is False:
                visited[ next_cell[0] ][ next_cell[1] ] = True
                parents[ next_cell[0] ][ next_cell[1] ] = cell
                Q.append(next_cell)



# ------------------------------------------------------------------------------

# seed the random generator
seed(datetime.now())

# record of which flow (0-indexed) is covering each cell
cells = [ [-1 for y in range(GRID_SIZE) ] for x in range(GRID_SIZE) ]

# create the window and the grid
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
grid = Grid(    [ 100, 56 ],
                760, 427,
                GRID_SIZE,
                GRID_SIZE,
                (179, 179, 179),
                thickness = 5.0,    )

# list of the grid's Flow objects
flows = []
n_flow = 0
# max_flows = ceil(random() * GRID_SIZE)

flows.append(Flow(  grid,
                    [ floor(random() * 255) for x in range(3) ] ))

endpoint1 = [ floor(random() * grid.cols), floor(random() * grid.rows) ]

flows[0].addEndpoint(endpoint1)
#flows[0].addEndpoint(endpoint2)

#print("Endpoint2 = " + str(endpoint2))

distances = [ [ 1000 for x in range(GRID_SIZE) ] for y in range(GRID_SIZE) ]
parents = [ [ None for x in range(GRID_SIZE) ] for y in range(GRID_SIZE) ]
visited = [ [ False for x in range(GRID_SIZE) ] for y in range(GRID_SIZE) ]
bfs(endpoint1, grid)

paths = []

wanted = floor(random() * GRID_SIZE) + 2
closest_dist_path = []
closest_dist = 1000

for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        cell, path, distance = [i, j], [ [i, j] ], 0
        while not cell == endpoint1:
            cell = parents[ cell[0] ][ cell[1] ]
            path.append(cell)
            distance = distance + 1

        distances[i][j] = distance

        if abs(wanted - distance) < abs(wanted - closest_dist):
            closest_dist_path = path
            closest_dist = distance

# reverse closest path so it starts at the first endpoint
closest_dist_path.reverse()

print("Wanted shortest distance = " + str(wanted))
print("Actual shortest distance = " + str(closest_dist))
print("Best shortest path = ", str(closest_dist_path))


# add the shortest path with the distance closest to the wanted distance
# flows[0].addEndpoint(closest_dist_path[0])

cells[ closest_dist_path[0][0] ][ closest_dist_path[0][1] ] = 0
for i in range(1, closest_dist + 1):
    cells[ closest_dist_path[i][0] ][ closest_dist_path[i][1] ] = 0
    flows[0].addCell(closest_dist_path[i])

n_steps = floor(random() * 3) + 4
current = closest_dist_path[-1]
last2dir, endpoint2 = [-1, -1], []

print("# random steps = " + str(n_steps))

for i in range(n_steps):
    directions = [ LEFT, DOWN, RIGHT, UP ]

    """
    if last2dir in ( [DOWN, RIGHT], [ DOWN, LEFT ] ) or last2dir[1] == DOWN:
        directions.remove(UP)
    elif last2dir in ( [UP, RIGHT], [UP, LEFT] ) or last2dir[1] == UP:
        directions.remove(DOWN)
    elif last2dir in ( [LEFT, UP], [LEFT, DOWN] ) or last2dir[1] == LEFT:
        directions.remove(RIGHT)
    elif last2dir in ( [RIGHT, UP], [RIGHT, DOWN] ) or last2dir[1] == RIGHT:
        directions.remove(LEFT)
    """

    # randomize which directions we may go in
    shuffle(directions)

    print(current)
    print("degree = " + str(degree(current, grid, 0)))
    print(directions)

    for d in directions:
        next_cell = add[d](*current)

        print("direction = " + str(d) + " | next = " + str(next_cell))

        if cellInGrid(next_cell, grid) and isEmpty(next_cell) and degree(next_cell, grid, 0) < 2:
            flows[0].addCell(next_cell)
            cells[ next_cell[0] ][ next_cell[1] ] = 0
            current = next_cell

            if last2dir == [-1, -1]:
                last2dir = [ d, d ]
            else:
                last2dir = [ last2dir[1], d ]

            break

    print("")

# the endpoint appears twice in the path after the last loop
#del flows[0].path[-1]

endpoint2 = flows[0].path[-1]
flows[0].addEndpoint(endpoint2)

print("Endpoint1 = " + str(endpoint1))
print("Endpoint2 = " + str(endpoint2))

# strategy: add random walk for a few vertices and then use shortest path?
# random + deterministric = still kinda random

# find path then draw flow for it
print(flows[0].path)

"""
for i in range(GRID_SIZE):
    print(parents[i])

for i in range(GRID_SIZE):
    print(distances[i])
"""

@window.event
def on_draw():
    window.clear()

    grid.draw()

    for flow in flows:
        flow.draw()

pyglet.app.run()
