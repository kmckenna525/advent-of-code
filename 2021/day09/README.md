# 2021 Day 9

Part 1 was straightforward

Part 2 - It's like an a* search without the searching. We can iterate through the low points and check all the neighbors and collect everything until it hits 9s. Assign each of those coords to a basin and done

General Time Estimate
- Part 1: θ(length * width) map size based 
- Part 2: θ(2 * length * width) map size based too - except we visit each node twice, once to get low points and then again while we're searching out from the low point

Benchmarks
- Part 1: **59.407949ms**
- Part 2: **110.848904ms**



