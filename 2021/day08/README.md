# 2021 Day 8

Well this one looks like it will take a while
Part 1 was easy at least! just loop through and count shit

Part 2 took a while to debug - I just kept screwing up python class syntax (forgetting self)
I also ran into a speed bump when I found out the hard way that the signals are not ordered consistently

General Time Estimate
- Part 1: θ(n) 
- Part 2: θ(n) - does up to 2 passes per set of input on the numbers (skips known), but still only grows linearly with number of lines

Benchmarks
- Part 1: **0.566006ms**
- Part 2: **8.327007ms**



