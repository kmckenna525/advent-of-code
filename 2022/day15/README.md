# 2022 Day 15

Part 1: Used a set to dedupe all possible x values

Part 2: First I tried the brute force literally mark up the cave map. That did not run in any sort of reasonable time. Reminded of the cubes one from last year, so I looked at that and came up with some x ranges that could be condensed down into non overlapping/touching ranges for each possible y value. Then if there is a gap in the input at all, that's the open spot. I think there could be an error since it allows invalid x values in the range - but it worked for my input so w/e

#### General Time Estimate
Not today

#### Benchmarks
- Part 1: **685.357094ms**
- Part 2: **79859.046936ms**

#### Stats
```
 15   00:42:42    2597      0   01:31:16    2395      0
```
