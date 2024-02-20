# Brainstorm area


## Measuring Unexpected Things

One idea for measuring "unexpected things" would have to be measuring how close the path comes to the end square before it is the end. So like if you have a path where halfway through it passes by the end before returning to finally end, that would be unexpected.

## Need to implement

- we're only gonna measure the amount of fun that a maze is, as they don't tend to get extremely difficult
- 'fun' will be measured based on: length of solution path and two 'unexpected' factors: how close the path gets to the end before actually getting there, and whether numbers are next to each other (that are not consecutive)

the base amount of fun will be determined by length of path, and the final score will be slightly influenced by these two extra factors

5 - should only be reachable when having max length and both of these extra factors
4 - reachable by max length and one of the two factors
3 - reachable just by going maxish length
2 - reachable at 2/3 of max length
1 - reachable at 1/3 of max length


max length for 20x20 - 50%
max length for 15x12 - 70%
