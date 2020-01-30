# ----------------------------------------------------------------------
#
#  ____
# |  _ \ _   _ _ __   __ _  ___  ___  _ __
# | | | | | | | '_ \ / _` |/ _ \/ _ \| '_ \
# | |_| | |_| | | | | (_| |  __/ (_) | | | |
# |____/ \__,_|_| |_|\__, |\___|\___/|_| |_|
#                    |___/
#
# ----------------------------------------------------------------------
#
# Description: Fun with dungeons
#
# Author: Marian Minar
#
# ----------------------------------------------------------------------

import dunfuns

# small map
mywalk = dunfuns.path(end = (0,30), seed = 35217) # small with one obstacle
mydun = dunfuns.dungeon(mywalk)
dunfuns.drawWorld(mydun.points)
print("Path start: " + str(mywalk.start))
print("Path end: " + str(mywalk.end))
print("Path wander: " + str(mywalk.wander))
print("Path seed: " + str(mywalk.seed))

# Good world to test A* in. Doesn't look good :-(
# mywalk = dunfuns.path(end = (0,40), wander = 10, seed = 1938)
# mypath = dunfuns.findPath(start = (0, 0), end = (-12, 38), allow = mydun.points)
