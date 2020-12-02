# Day 1
## Attempt 1
Just bulldozed through 
- minor optimization by starting second (and then third) loops at 1 (and 2)
- minor optimization by exiting early

General Big O estimate
- Part 1: (O(n^2) = 40,000)
- Part 2: (O(n^3) = 8,000,000)

Benchmarks
- Part 1: **17,353 iterations** in **3.629923ms** (worst case: 39,601 iterations)
- Part 2: **1,374,483 iterations** in **414.558887ms** (worst case: 7,762,392 iterations)

## Attempt 2
Major optimization - don't need j to ever be < i! Can just start j at i + 1. Once we've evaluated something in position i, we never need j to be that number ever again. I think this is still O(n^2) technically, but it's like... halfish in practice. It made a much bigger difference in part 2 - it's late and I don't have the brain power to prove it, but I think it generalizes for k to start at j + 1? I certainly got the same answer. 

Benchmarks
- Part 1: **13,612 iterations** in **2.850056ms** (worst case: 19,900 iterations)
- Part 2: **584,628 iterations** in **176.265001ms** (worst case: 1,293,699 iterations)



