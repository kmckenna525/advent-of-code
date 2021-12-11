# 2021 Day 11

Part 1: Can take the Coord class and CaveMap from day 9. Smooth - only issues were tiny bugs using the coord instead of the neighbor :| 
Part 2: Really too easy... basically already solved just had to change the main running logic

General Time Estimate
- Part 1: θ(n) - only grows with the target number of steps, each step just iterates the 10x10 grid 3-4 times (depending on number of flashes)
- Part 2: O(infinity) - I think the input is guaranteed to eventually synchronize, but not sure if that's always the case. Could go forever

Benchmarks
- Part 1: **84.125996ms**
- Part 2: **219.936848ms**



