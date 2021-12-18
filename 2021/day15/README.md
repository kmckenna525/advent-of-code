# 2021 Day 15

Part 1: return of the coords! okay yeah this is same as 2015 22 but the graph is this map
Part 2: Took 44sec, A* instead would make this reasonable?? Nah it didn't work out :(
It's really hard to come up with an admissable heuristic

Well apparently manhattan distance works fine. idk why I bothered with the other heuristic iterations ugh
It's probably because we need to consider the best case scenario and THEN leave it to be proven wrong to actually get the optimal path
Otherwise the optimal path might look really bad 


General Time Estimate
- Part 1: θ(E + V log V) (Dijkstra) 
- Part 2: θ(E + V log V) (Dijkstra) 

Benchmarks
- Part 1: **833.487034ms**; A* is **487.225056ms**
- Part 2: **44473.677158ms**; A* is 1/4 the time **10312.047005ms**


Stats
 15   00:13:00   615      0   00:49:27  1499      0
