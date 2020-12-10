# 2020 Day 5
- Epiphany! It's just a binary string. So can convert the Fs/Bs to 0s/1s.
- Did a regex at first to separate row and col, but realized I could just bit shift. Change the program for that.
- Gonna do part 2 the naive way first (shove in a list and sort and voila), and then think of a way to optimize with a second attempt later maybe?
- I actually can't think of a good way to optimize. I think this is it.

General Time Estimate
- Part 1: θ(n) 
- Part 2: O(nlogn) - python uses a merge sort

Benchmarks
- Part 1: **2.110958ms**
- Part 2: **2.229929ms**



