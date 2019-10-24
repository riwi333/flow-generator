from context import Grid, Flow, generator
from time import process_time, gmtime
import git

"""
given generated paths for grids of various sizes, measure the runtime and performance of
the path simplification process
"""

MIN_SIZE = 4        # minimum grid size to generate flows for
MAX_SIZE = 20       # maximum grid size to generate flows for
NUM_TESTS = 20      # number of flow generations to do per grid size

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

generate_times, simplify_times, initial_length, final_length = [], [], [], []
for i in range(MAX_SIZE - MIN_SIZE + 1):
    g_time, s_time, init, final = float(0), float(0), float(0), float(0)
    for j in range(NUM_TESTS):
        # get a list of successfully generated paths
        g_t, paths = None, None
        while paths == None:
            grids[i].clearValues()
            g_t = process_time()
            paths = generator.generatePaths(grids[i])
            g_t = process_time() - g_t

        # keep track of how long the succesful generation process took
        g_time += g_t

        # measure the runtime of path simplification and the initial and final number of paths in the grid
        init += len(paths)
        start_time = process_time()
        paths = generator.simplifyPaths(grids[i], paths)
        s_time += process_time() - start_time
        final += len(paths)

        # clear the grid so we can generate new paths for it
        grids[i].clearValues()

    generate_times.append(g_time)
    simplify_times.append(s_time)
    initial_length.append(init)
    final_length.append(final)

print("{:15s}{:33s}{:27s}{:27s}{:27s}".format("Grid size", "Successful generation time", "Simplification time", "Initial # paths", "Final # paths"))

# print out all the collected information
for i in range(MAX_SIZE - MIN_SIZE + 1):
    generate_times[i] = generate_times[i] / NUM_TESTS
    simplify_times[i] = simplify_times[i] / NUM_TESTS
    initial_length[i] = initial_length[i] / NUM_TESTS
    final_length[i] = final_length[i] / NUM_TESTS

    size_string = str(i + MIN_SIZE) + "x" + str(i + MIN_SIZE)
    print("{:<15s}{:<33.3f}{:<27.3f}{:<27.3f}{:<27.3f}".format(size_string, generate_times[i], simplify_times[i], initial_length[i], final_length[i]))

print("\nPerformed " + str(NUM_TESTS) + " tests per size")
