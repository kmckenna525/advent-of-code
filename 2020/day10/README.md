# 2020 Day 10
- Part 1: I overthought it and started building a graph.... THEN I realized I can just assume the sorted list is the main solution.
- Part 2: Okay now I need that graph. At first did straight dfs, but then remembered to memoize it when it was taking like... an hour.

General Time Estimate
- Part 1: O(nlogn) - from sorting the list
- Part 2: O(nlogn) - I think memoizing makes it so we only calculate the paths from each node once, plus the sort we did

Benchmarks
- Part 1: **0.125170ms**
- Part 2: **1.028061ms**



