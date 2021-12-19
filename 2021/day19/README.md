# 2021 Day 19

Part 1: Initial thought: wtf. Also, it looks like each scanner output can instead be represented as a vector space of beacons relative to each other. So if I map out each beacon's vector to each of it's neighbors, we can just compare beacons and check: for scanner outputs a and b, does any beacon in a have more than 12 vector overlaps with any beacon in b? I'm not sure how many we need to check to be sure that we've covered them all either, because that's a lot to check. I'll start with all of them, and just allow early out for when we find a match


Part 2: 

#### General Time Estimate
- Part 1: θ(n) 
- Part 2: θ(n)

#### Benchmarks
- Part 1: **xxxms**
- Part 2: **xxxms**

#### Stats
```
```
