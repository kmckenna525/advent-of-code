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


Actually - minor optimization to just make the points sets a member variable instead of recalculating on every intersection check. 
This is a major improvement

General Time Estimate
- Part 1: θ(n^2) 
- Part 2: θ(n^2)

Benchmarks
- Part 1: **1015.962124ms**
- Part 2: **2742.733002ms**


Stats
  5   00:39:38  5378      0   00:40:54  3230      0