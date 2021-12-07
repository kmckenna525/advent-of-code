# 2021 Day 6

Part 1: just the direct brute force, I bet part 2 will need something better
Part 2: yeah.... I think I need something recursive
Two things: 
1. I bet I can solve for each possible initial clock separately and memoize them
2. I think solving for 1 is days / cycles, plus some fudging with initial clock, then doing the same for each child and child's child
Okay yeah math with memoization worked great. Just ran into an issue where I forgot to add initial fishies to the result

General Time Estimate
- Part 1: θ(initial ^ (days/7))?? I think 
- Part 2: O(days/7 * 7) - we only recurse once per valid starting state which is finite (7 states), so really just depends on number of days

Benchmarks
- Part 1: **1323.673010ms** (0.413179ms after part 2 optimization)
- Part 2: **1.878023ms**



