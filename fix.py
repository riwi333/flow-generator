from grid import Grid
from flow import Flow
import generator

def fixFlows(grid, flows, empty, fixes=[]):
    """
    attempt to fix this grid's flows by filling all empty cells

    """

    for fix in fixes:
        if fix == 1:
            grid, flows, empty = fix1(grid, flows, empty)

    return (grid, flows, empty)

def fix1(grid, flows, empty):
    """
    fix1: if an empty cell is adjacent to a flow's endpoint, and that cell
    has a flowDegree < 2, extend the flow to cover that cell (and adjacent
    cells in the same direction, if possible)

    """

    removed = []

    for emptyCell in empty:
        # flowLength needs to be anything greater than the maximum flow length
        flowLength, flowDirection, flowEndpoint, extendedFlow = grid.rows ** 2, None, None, None

        for flow in flows:
            endpoint, direction = None, None

            # try the first endpoint of this flow
            direction = generator.adjacentDirection(flow.endpoints[0], emptyCell)
            if not direction == None:
                endpoint = flow.endpoints[0]

            # try the second endpoint of this flow
            else:
                direction = generator.adjacentDirection(flow.endpoints[1], emptyCell)
                if not direction == None:
                    endpoint = flow.endpoints[1]

            # make sure we use the flow with the shortest length to cover the empty cell
            if not endpoint == None and not direction == None:
                if len(flow.path) < flowLength:
                    flowDirection, flowEndpoint, extendedFlow = direction, endpoint, flow
                    flowLength = len(flow.path)

        # if we found an endpoint that works, extend the flow to cover the empty cell
        if not flowEndpoint == None and not flowDirection == None:
            newPath = [ flowEndpoint ]

            # see if other there are any other adjacent empty cells in the same direction
            current = emptyCell
            flowCondition1 = len(newPath) == 1 and generator.flowDegree(grid, current, extendedFlow.index) == 1
            flowCondition2 = len(newPath) > 1 and generator.flowDegree(grid, current, extendedFlow.index) == 0
            while generator.inGrid(grid, current) and generator.isEmpty(grid, current) and (flowCondition1 or flowCondition2):
                newPath.append(current)
                current = generator.next[flowDirection](*current)

            print(extendedFlow.path)
            print(newPath)

            # add the path of empty cells to the flow
            if flowEndpoint == extendedFlow.endpoints[0]:
                extendedFlow.extendPath(newPath, flowEndpoint)
            else:
                extendedFlow.extendPath(newPath, flowEndpoint)

            print(extendedFlow.path)

            for i in range(1, len(newPath)):
                removed.append(newPath[i])

    for cell in removed:
        empty.remove(cell)

    return (grid, flows, empty)

# fix2: add flows of length 3
