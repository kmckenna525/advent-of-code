# 2021 Day 12

Part 1: DFS to collect all paths from start to end

Part 2: Just add one more rescurse for each small node

#### General Time Estimate
- Part 1: O(n!)? - DFS is θ(nodes + connections), but this adds some backtracking ability... So maybe O(n!) for the worst case of all large nodes?
- Part 2: O(n!)? - same, but actual case is as if there is one extra node per small node calculation

#### Benchmarks
- Part 1: **112.816811ms**
- Part 2: **3873.629093ms**


#### Stats 
```
 12   00:26:47  2345      0   00:46:18  2454      0
```