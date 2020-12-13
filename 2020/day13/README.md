# 2020 Day 13
Part 1 was easy. For Part 2 I got completely stuck and had to find hints. I had a correct answer, I just couldn't optimize it properly. Eventually skimmed to find Chinese Remainder Theorem which I had embarassingly completely forgotten, even though I had to prove it in college :|

Using this CRT refresher: https://www.youtube.com/watch?v=ru7mWZJlRQg

So with CRT:
t = 0 (mod bus 0)
t = 1 (mod bus 1)
t = 2 (mod bus 2)
t = 3 (mod bus 3)
... and so on

Loop through all buses.
	Start with LCM of all buses except this bus
	Solve the equivalence at this index as LCM * some number
	Add that result to the running total
That running total is our solution!

(All the buses are prime in general, so they are guaranteed coprime)

Got tripped up AGAIN when I kept getting numbers too large. Just had to modulo the total by the LCM of all buses...

General Time Estimate
- Part 1: θ(n) 
- Part 2: O(n * m) where n is length of list and m is largest number in that list 

Benchmarks
- Part 1: **0.060081ms**
- Part 2: **0.298023ms**



