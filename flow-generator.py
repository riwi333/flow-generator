import pyglet
from grid import Grid
from flow import Flow
import generator
from random import random, seed
from datetime import datetime
from math import floor

"""
randomly generate solved flow puzzles

"""

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
GRID_SIZE = 7

# seed the random generator
seed(datetime.now())

# create the window and the grid
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
grid = Grid(    [ 50, 50 ],
                700, 400,
                GRID_SIZE,
                GRID_SIZE,
                (179, 179, 179),
                thickness = 5.0,    )

# list of grid's Flow objects
flows = []
index = 0

print(generator.degree(grid, [0, 0]))

n_flows = 11

for i in range(n_flows):
    # create a new Flow object
    flows.append(Flow(  grid,
                        [ floor(random() * 255) for x in range(3) ],
                        index   ))

    print("Creating flow #" + str(index))

    # find a working endpoint to start with
    start = generator.chooseEndpoint(grid)
    print("Start point: " + str(start))
    if start == None:
        break

    # find all shortest paths for this endpoint
    shortestPaths = generator.getAllShortestPaths(grid, start)
    #print(shortestPaths)

    # choose a distance we want to aim for in a shortest path
    # TODO: this should probably vary with # of flows
    distance_goal = floor(random() * GRID_SIZE) + 2

    print("Distance goal: " + str(distance_goal))

    # find a shortest path with distance as close to the goal as possible
    closest_distance_path = []
    closest_distance = GRID_SIZE ** 2   # anything > than max shortest distance

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell, path, distance = [i, j], [], 0
            path.append(cell)

            # keep moving along parent cells until we get back to the start cell
            while not cell == start:
                cell = shortestPaths[ cell[0] ][ cell[1] ]

                # if shortestPaths() gives None, this cell is not reachable
                if cell == None:
                    break

                path.append(cell)
                distance = distance + 1

            if cell == None:
                continue

            # see if this path has a distance close to our goal
            if abs(distance_goal - distance) < abs(distance_goal - closest_distance):
                closest_distance_path = path
                closest_distance = distance

    # since paths are searched backwards, reverse the best path
    closest_distance_path.reverse()

    print("Closest path: " + str(closest_distance_path))
    print("Actual distance: " + str(closest_distance))

    # update the grid with this flow's shortest distance path
    for cell in closest_distance_path:
        grid.values[ cell[0] ][ cell[1] ] = flows[index]

    # random walk for a few steps after the shortest path (# of steps should
    # vary with # of flows)
    full_path = closest_distance_path
    walk_steps = floor(random() * GRID_SIZE)
    for i in range(walk_steps):
        next_path = generator.randomStep(grid, full_path, flow_index = index)

        if next_path == None:
            break
        else:
            # update the complete path and the grid
            full_path = next_path
            grid.values[ full_path[-1][0] ][ full_path[-1][1] ] = flows[index]

    print("Max random steps: " + str(walk_steps))
    print("Full path: " + str(full_path))

    # in order to help avoid empty groups of two, full path's endpoints
    # should have a shortest distance > 2 (which shortestPaths already contains)
    flows[index].addPath(full_path)

    index = index + 1

    # TODO: need a bunch of heuristics to make sure grids are filled like
    # 95% of the time (if heuristics fail but are very likely to work, we
    # can just throw out bad grids and restart the process)

#-------------------------------------------------------------------------------

@window.event
def on_draw():
    window.clear()

    grid.draw()
    for flow in flows:
        flow.draw()

pyglet.app.run()
