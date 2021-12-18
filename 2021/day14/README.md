# 2021 Day 14

This sounds a lot like 2015 day 19

Part 1: just did as written in instructions

Part 2: well, that doesn't work very quickly... So immediately I see that it's a tree structure. Every pair in the rules spawns two new pairs that also may be found in the rules. Maybe we just follow that tree for each element and count the leaves we find? We can even memo the results for loops

Memo did the trick!

General Time Estimate
- Part 1: ?? I don't want to do time analysis todayyyyyy
- Part 2: ?? 

Benchmarks
- Part 1: **7.968903ms**; **3.604889ms** after part 2!
- Part 2: **19.793987ms**



Stats
 14   00:20:47  3478      0   01:11:04  3509      0