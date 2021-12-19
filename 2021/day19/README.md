# 2021 Day 19

Part 1: Initial thought: wtf. Also, it looks like each scanner output can instead be represented as a vector space of beacons relative to each other. So if I map out each beacon's vector to each of it's neighbors, we can just compare beacons and check: for scanner outputs a and b, does any beacon in a have more than 12 vector overlaps with any beacon in b? I'm not sure how many we need to check to be sure that we've covered them all either, because that's a lot to check. I'll start with all of them??

Running into issues with possible rotations and translations and mapping back to the source set :| 


Part 2: easy since I have positions


#### General Time Estimate
- Part 1: ??? I'm tired
- Part 2: ???

#### Benchmarks
- Part 1: **36071.795940ms**
- Part 2: **36064.917088ms**

#### Stats
```
 19   05:27:01  2401      0   05:39:53  2274      0
```
