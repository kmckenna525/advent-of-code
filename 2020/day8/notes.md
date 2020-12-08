# 2020 Day 8
At first I thought I had to do the racing nodes linked list dealio - but I don't think that solves it for exactly the first loop. Simply storing seen nodes in a set worked fine. 
For part 2, I think maybe there could be a faster solution in tracking the order of the commands seen as you run the program and then changing the instructions in that order instead of line by line like I did? But in the end the worst case is the same, it just might speed up if some instructions are absolutely never seen. 

General Time Estimate
- Part 1: O(n) 
- Part 2: O(n^2)

Benchmarks
- Part 1: **1.760960ms**
- Part 2: **5.497932ms**



