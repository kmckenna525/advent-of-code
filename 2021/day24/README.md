# 2021 Day 24

Part 1: This was gonna take an insanely long time, and I was an hour in. So I started decompiling by hand and figured out the patterns. It's treating the number in z as a stack and pushing each input (+ offset) onto it. If it equals the proper paired input, then it is propertly popped off. Once I had the "manual" I was able to just find the number directly. Used the code I wrote to verify the answer I found

Part 2: Just same in opposite way. 

#### General Time Estimate
- Part 1: N/A 
- Part 2: N/A

#### Benchmarks
- Part 1: **xxxms**
- Part 2: **xxxms**

#### Stats
```
 24   02:17:35   698      0   02:20:46   629      0
```
