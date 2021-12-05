# 2021 Day 5

Just did a brute force checking of every point in the line. I coded without assuming horz and vert, so part 2 was a freebie.
To optimize - I'm checking half the permutations, but still basically n^2. 

I think maybe finding the min coord and max coord in the entire set and then iterating over every point and checking if present on more than one line may be faster, and would require less allocations? But idk and I don't have time to test

General Time Estimate
- Part 1: θ(n^2) 
- Part 2: θ(n^2)

Benchmarks
- Part 1: **3989.426851ms**
- Part 2: **14948.225975ms**



