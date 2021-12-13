# 2015 Day 22

Just did a version of Dijkstra where distance is spell cast (it's kind of BFS with a priority queue that decides what we go deep on). 
Part 2 revealed a bug in how I was checking win conditions - I was not calculating a win from poison on the boss's turn

General Time Estimate
- Part 1: θ(E + V log V) (Dijkstra) Total possible edges and vertices depends on all possible game endings, but it is finite since there are no loops you can get into from the abilities given
- Part 2: θ(E + V log V) (Dijkstra) 

Benchmarks
- Part 1: **95.452070ms**
- Part 2: **164.155006ms**

