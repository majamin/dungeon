# Dungeon

Generates a random dungeon using unicode characters.

## Info

The dungeon is created using two main steps:
1. Generate a random path (random walk) between two points
2. "Paint" the path with a 3x3 block ("fatpath")

TODO:

1. Slow. How to speed it up?
	* When creating the "fatpath", lots of repeated coordinates are generated.
	  The current workaround is to eliminate the duplicates.
	  This is accomplished by converting the path to a dictionary and back to a list.
