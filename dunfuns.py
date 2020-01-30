#-----------------------------------------------------------------------------
#  ____
# |  _ \ _   _ _ __   __ _  ___  ___  _ __
# | | | | | | | '_ \ / _` |/ _ \/ _ \| '_ \
# | |_| | |_| | | | | (_| |  __/ (_) | | | |
# |____/ \__,_|_| |_|\__, |\___|\___/|_| |_|
#                    |___/
#  _____                 _   _
# |  ___|   _ _ __   ___| |_(_) ___  _ __  ___
# | |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# |  _|| |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#
#------------------------------------------------------------------------------

from numpy.random import choice as choice
from numpy.random import seed as setSeed

# ---------------------------------------------------- FUNCTION Pull ----------

# This function helps the random walk function work.
# This function creates a set, pull, which includes directions (-1, 0, 1).
# If wander is high, the Pull will not be as strong in a specific direction.
# `wander` dilutes the pulling vectors, effectively slowing convergence.

def Pull(m, n, wander):
    if m < n:
        pull = choice([1, 1] + ([-1,0,1] * wander), 1)[0]
    elif m == n:
        pull = choice([0, 0] + ([-1,0,1] * wander), 1)[0]
    else:
        pull = choice([-1, -1] + ([-1,0,1] * wander), 1)[0]
    return pull

# -------------------------------------------------- CLASS path --------

# A path is a random walk, from start to end.
# Higher `wander` values slows convergence to the end point (see Pull above).

class path:

    def __init__(self, start = (0,0), end = (0,20), wander = 10, seed = None):
        self.start = start
        self.end = end
        self.seed = seed
        self.wander = wander
        self.points = self.makePath()

    def makePath(self):
        path = []

        # if user did not set a seed, pick one at random
        if self.seed == None:
            self.seed = choice(range(100000), 1)[0]
            setSeed(seed = self.seed)
        # if user set a seed, set it here
        else:
            setSeed(seed = self.seed)

        # current location is start
        loc = self.start
        path.append(self.start)
        nextCoor = 0

        # generate path
        while loc != self.end:
            loc = path[-1]
            previousCoor = path[-1]
            nextCoor = (previousCoor[0] + Pull(loc[0], self.end[0], self.wander), \
                    previousCoor[1] + Pull(loc[1], self.end[1], self.wander))
            if loc != self.end:
                path.append(nextCoor)

        return path

# ------------------------------------------------------- CLASS dungeon -------

# Takes a `path` class object and "fattens" the path to make caverns, etc.

class dungeon:

    def __init__(self, path):
        self.path = path
        self.points = self.fatPath()

    # print dungeon
    def fatPath(self):
        fatpath = []

        # adds a chunky block to each point on the path
        for point in self.path.points:
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    fatpath.append((point[0]+i, point[1]+j))

        # remove duplicates (increases speed by a factor of 4)
        fatpath = list(dict.fromkeys(fatpath))

        return fatpath

# --------------------------------------------------- FUNCTION findPath -------

# Finds the fastest path between two points using the A* algorithm.
# User has the option to either "allow" points, or determine "no go" points.
# "allow" and "noGo" are mutually exclusive.
# If both "allow" and "noGo" are empty, `findPath` assumes 100% freedom,
# effectively making a straight-line path.

def findPath(end, start = (0,0), allow = [], noGo = []):

    # Distance function
    # Manhattan
    def dist(coor1, coor2):
        return abs(coor1.coor[0]-coor2.coor[0]) + abs(coor1.coor[1]-coor2.coor[1])

    # point class helps find shortest paths (A*)
    class point:
        def __init__(self, coorx, coory):
            self.x = coorx; self.y = coory; self.coor = (self.x, self.y)
            self.parent = None
            self.gscore, self.hscore, self.fscore = 0, 0, 0
            self.nbrs = self.get_nbrs()

        def get_nbrs(self):
            nbrs = []
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if i == 0 and j == 0:
                        continue
                    else:
                        nbrs.append((self.x + i, self.y + j))
            return nbrs
        def __eq__(self, other):
            return (str(self.coor) == str(other))
        def __repr__(self):
            return "(%i, %i)" % (self.x, self.y)

    # initialize path, open and closed lists
    path, openList, closedList = [], [], []

    # convert start and end to class
    start = point(start[0], start[1])
    end = point(end[0], end[1])

    # delay = 0 # debug

    # A* start:
    openList.append(start)
    while openList != []:
        # time.sleep(delay) # debug
        minF = min([point.fscore for point in openList])
        current = [point for point in openList if point.fscore == minF][0]
        # print("Current node is: " + str(current)) # debug
        openList.remove(current)
        # print(str( current ) + " removed from open and add to closed:") # debug
        # print("open list: " + str(openList)) # debug
        if current not in closedList:
            closedList.append(current)
        # print("closed list: " + str(closedList)) # debug
        # print("Scanning children:") # debug
        if current == end:
            break
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                else:
                    child = point(current.x + i, current.y + j)
                # print("\tCurrent child: " + str(child)) # debug
                child.parent = current
                if allow == []:
                    if child in closedList or child in noGo:
                        # print("\t\tchild " + str( child ) + " is not traversable") # debug
                        continue
                else:
                    if child in closedList or child not in allow:
                        # print("\t\tchild " + str( child ) + " is not traversable") # debug
                        continue
                if child.gscore < current.gscore or child not in openList:
                    child.gscore = current.gscore + dist(child, current)
                    child.hscore = dist(child, end)
                    child.fscore = child.gscore + child.hscore
                    # print("\t\t F = G + H: " + str(child.fscore) + " = " + str(child.gscore) + " + " + str(child.hscore)) # debug
                    current = child.parent
                    if child not in openList:
                        # print("\t\tchild " + str(child) + " not in open list ... adding it") # debug
                        openList.append(child)

    # Trace backwards

    tracePoint = closedList[-1]
    path.append(tracePoint)

    while tracePoint != start:
        mylist = [point for point in closedList if point in tracePoint.nbrs]
        fMin = min([point.fscore for point in mylist])
        tracePoint = [point for point in mylist if point.fscore == fMin][0]
        path.append(tracePoint)

    return [point.coor for point in path]


# --------------------------------------------------- FUNCTION drawWorld ------

# Attempt at making a graphical representation of paths, sprites, etc.

def drawWorld(layer1, layer2 = [], layer3 = []):

    combined = layer1 + layer2 + layer3
    xMin = min([point[0] for point in combined])
    xMax = max([point[0] for point in combined])
    yMin = min([point[1] for point in combined])
    yMax = max([point[1] for point in combined])
    # print(str(xMin) + " " + str(xMax) + " " + str(yMin) + " " + str(yMax)) # debug

    for i in range(xMin - 2, xMax + 3):
        for j in range(yMin - 2, yMax + 3):
            if (i,j) in layer3:
                print('\u25AA', end = '')
            elif (i,j) in layer2:
                print('\u2592', end = '')
            elif (i,j) in layer1:
                print(' ', end = '')
            else:
                print('\u2593', end = '')
        print('')


