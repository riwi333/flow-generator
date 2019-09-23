from grid import Grid
from flow import Flow
import generator
import fix

START_SIZE = 5
END_SIZE = 10
SAMPLES = 200

# see what fraction of grids are filled, using no fixes
success_rate = [ 0 for x in range(START_SIZE, END_SIZE) ]
for size in range(START_SIZE, END_SIZE):
    grid = Grid(    [0, 0],
                    0,
                    0,
                    size,
                    size)

    for test in range(SAMPLES):
        flows, empty = generator.generateFlows(grid, size)
        grid, flows, empty = fix.fix1(grid, flows, empty)

        # success
        if len(empty) == 0:
            index = size - START_SIZE
            success_rate[index] = success_rate[index] + 1

        grid.clearValues()

print("Success rates:")
for i in range(START_SIZE, END_SIZE):
    index = i - START_SIZE
    print("Size " + str(i) + ": " + str(float(success_rate[index]) / SAMPLES))
