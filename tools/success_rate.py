from context import Grid, Flow, generator

"""
measure the success rates of flow generation for various grid sizes
"""

MIN_SIZE = 4        # minimum grid size to generate flows for
MAX_SIZE = 20       # maximum grid size to generate flows for
NUM_TESTS = 30      # number of flow generations to do per grid size

# make a grid for each measured size (graphics-related sizing doesn't matter here)
grids = [   Grid(   [0, 0],
                    0, 0,
                    size,
                    size,
                    (0, 0, 0)   )
            for size in range(MIN_SIZE, MAX_SIZE + 1)   ]

success_rates = []
for i in range(MAX_SIZE - MIN_SIZE + 1):
    success = 0
    for j in range(NUM_TESTS):
        paths, remaining = generator.generateFlows(grids[i])

        # if there are no more empty cells in the grid, generateFlows() succeeded
        if len(remaining) == 0:
            success += 1

        # clear all the marked values in the grid to reset it for the next test
        grids[i].clearValues()

    success_rates.append(success)

for i in range(MAX_SIZE - MIN_SIZE + 1):
    success_rates[i] = float(success_rates[i]) / NUM_TESTS
    print(str(i + MIN_SIZE) + "x" + str(i + MIN_SIZE) + ": " + str(success_rates[i]))
