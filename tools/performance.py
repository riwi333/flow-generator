from context import Grid, Flow, generator
from time import process_time, gmtime
import git

"""
measure the success rates and average runtime of flow generation for various grid sizes
"""

MIN_SIZE = 4        # minimum grid size to generate flows for
MAX_SIZE = 20       # maximum grid size to generate flows for
NUM_TESTS = 30      # number of flow generations to do per grid size

# include current git master branch commit information to help track performance progress
current_repo = git.Repo(search_parent_directories=True)
current_branch = current_repo.active_branch.name
current_commit = current_repo.heads[current_branch].commit

# figure out date and time via the count of seconds from epoch to the commit
commit_time = current_commit.authored_date
time_struct = gmtime(commit_time)
month, day, year = time_struct.tm_mon, time_struct.tm_mday, time_struct.tm_year
hour, minute, second = time_struct.tm_hour, time_struct.tm_min, time_struct.tm_sec
datestring = str(month) + "/" + str(day) + "/" + str(year) + " " + str(hour) + ":" + str(minute) + ":" + str(second)

print("Commit ID: " + current_repo.heads[current_branch].object.hexsha)
print("Commit branch: " + current_branch)
print("\"" + str(current_commit.message.strip()) + "\"")
print(datestring + "\n")

# make a grid for each measured size (graphics-related sizing doesn't matter here)
grids = [   Grid(   [0, 0],
                    0, 0,
                    size,
                    size,
                    (0, 0, 0)   )
            for size in range(MIN_SIZE, MAX_SIZE + 1)   ]

success_rates, success_times, fail_times, expected_times = [], [], [], []
for i in range(MAX_SIZE - MIN_SIZE + 1):
    success, s_time, f_time = float(0), float(0), float(0)
    for j in range(NUM_TESTS):
        # run the flow generation algorithm and measure its runtime
        time = process_time()
        paths = generator.generatePaths(grids[i])
        time = process_time() - time

        # check if generatePaths() succeeded (if not, it returns a None object)
        if paths == None:
            f_time += time
        else:
            success += 1
            s_time += time

        # clear all the marked values in the grid to reset it for the next test
        grids[i].clearValues()

    success_rates.append(success)
    success_times.append(s_time)
    fail_times.append(f_time)

print("{:15s}{:18s}{:22s}{:22s}{:22s}".format("Grid size", "Success rate", "Successful runtime", "Failed runtime", "Expected runtime"))

# print out all the collected information
for i in range(MAX_SIZE - MIN_SIZE + 1):
    if success_rates[i] == 0:
        success_times[i] = float('nan')
        fail_times[i] = fail_times[i] / NUM_TESTS

    elif success_rates[i] == NUM_TESTS:
        success_times[i] = success_times[i] / NUM_TESTS
        fail_times[i] = float('nan')

    else:
        success_times[i] = success_times[i] / success_rates[i]
        fail_times[i] = fail_times[i] / (NUM_TESTS - success_rates[i])

    success_rates[i] = success_rates[i] / NUM_TESTS

    # calculate the expected runtime using the success rate as the parameter
    # of a geometric random variable
    if success_rates[i] == 0:
        expected_times.append(float('nan'))
    else:
        expected = success_times[i] + fail_times[i] / success_rates[i]
        expected_times.append(expected)

    size_string = str(i + MIN_SIZE) + "x" + str(i + MIN_SIZE)
    print("{:<15s}{:<18.3f}{:<22.3f}{:<22.3f}{:<22.3f}".format(size_string, success_rates[i], success_times[i], fail_times[i], expected_times[i]))

print("\nPerformed " + str(NUM_TESTS) + " tests per size")
