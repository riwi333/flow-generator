from context import Grid, Flow, generator
from time import process_time, gmtime

"""
measure the success rates and average runtime of flow generation for various grid sizes
"""

MIN_SIZE = 4        # minimum grid size to generate flows for
MAX_SIZE = 13       # maximum grid size to generate flows for
NUM_TESTS = 3      # number of flow generations to do per grid size

# make a grid for each measured size (graphics-related sizing doesn't matter here)
grids = [   Grid(   [0, 0],
                    0, 0,
                    size,
                    size,
                    (0, 0, 0)   )
            for size in range(MIN_SIZE, MAX_SIZE + 1)   ]

success_rates, times = [], []
for i in range(MAX_SIZE - MIN_SIZE + 1):
    success, runtime = 0, float(0)
    for j in range(NUM_TESTS):
        # run the flow generation algorithm and measure its runtime
        initial_time = process_time()
        paths, remaining = generator.generateFlows(grids[i])
        runtime += process_time() - initial_time

        # if there are no more empty cells in the grid, generateFlows() succeeded
        if len(remaining) == 0:
            success += 1

        # clear all the marked values in the grid to reset it for the next test
        grids[i].clearValues()

    success_rates.append(success)
    times.append(runtime)

for i in range(MAX_SIZE - MIN_SIZE + 1):
    success_rates[i] = float(success_rates[i]) / NUM_TESTS
    times[i] = times[i] / NUM_TESTS
    print(str(i + MIN_SIZE) + "x" + str(i + MIN_SIZE) + ": ")
    print("Success rate: " + str(success_rates[i]))
    print("Average runtime: " + str(times[i]))
