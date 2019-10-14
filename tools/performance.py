from context import Grid, Flow, generator
from time import process_time, gmtime
import git

"""
measure the success rates and average runtime of flow generation for various grid sizes
"""

MIN_SIZE = 4        # minimum grid size to generate flows for
MAX_SIZE = 15       # maximum grid size to generate flows for
NUM_TESTS = 30      # number of flow generations to do per grid size

# include current git master branch commit information to help track performance progress
current_commit = git.Repo(search_parent_directories=True).heads.master.commit

# figure out date and time via the count of seconds from epoch to the commit
commit_time = current_commit.authored_date
time_struct = gmtime(commit_time)
month, day, year = time_struct.tm_mon, time_struct.tm_mday, time_struct.tm_year
hour, minute, second = time_struct.tm_hour, time_struct.tm_min, time_struct.tm_sec
datestring = str(month) + "/" + str(day) + "/" + str(year) + " " + str(hour) + ":" + str(minute) + ":" + str(second)

print("Commit: " + str(current_commit.message.strip()))
print(datestring + "\n")

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

print("{:15s}{:18s}{:15s}".format("Grid size", "Success rate", "Average runtime"))

# print out all the collected information
for i in range(MAX_SIZE - MIN_SIZE + 1):
    success_rates[i] = float(success_rates[i]) / NUM_TESTS
    times[i] = times[i] / NUM_TESTS

    size_string = str(i + MIN_SIZE) + "x" + str(i + MIN_SIZE)
    print("{:<15s}{:<18.3f}{:<15.3f}".format(size_string, success_rates[i], times[i]))

print("\nPerformed " + str(NUM_TESTS) + " tests per size")
