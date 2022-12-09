# 2022 Day 9
Took me 5 min just to read this shit yo

Brain fart for initializing the set - it inits on an iterable so my tuple was adding a 0, not (0,0). Slowed me down on part 2, should have gotten the result + 1 and then fixed it instead. But I'm pretty happy with my placement considering it's my first time using numpy.

#### General Time Estimate
- Part 1: θ(n) where n is the total number of single unit steps the head takes
- Part 2: θ(n) except this time it's * 9 worst case which doesn't matter for this analysis, but you do see it in the time it took.

#### Benchmarks
- Part 1: **80.932856ms**
- Part 2: **331.882000ms**

#### Stats
```
  9   00:21:23    2249      0   00:29:19    1218      0
```
