# Santa Claus 2 solution
"""
We have N house points (Xi, Yi) (distinct) and a starting point (Sx, Sy) with no house there.
Santa performs M axis‑aligned moves.  Each move is either vertical (U/D) or horizontal (L/R) and travels
a distance Ci.  The path consists of closed line segments, and we need:
  * the final coordinates after all moves,
  * the number of distinct houses that lie on any segment (including segment endpoints).

Constraints: N, M ≤ 2·10^5, coordinates up to 1e9 (and final coordinates may be larger).
A naïve O(N·M) scan is impossible.

Observation
-----------
A house (x, y) is visited iff one of the following holds:
  * there exists a **vertical** segment with constant x where y lies between the segment's y‑range, or
  * there exists a **horizontal** segment with constant y where x lies between the segment's x‑range.
Thus we can treat vertical and horizontal segments separately.

Algorithm
----------
1. Simulate the walk, storing each segment as an interval:
   * vertical: key = x, interval = [y1, y2] (inclusive)
   * horizontal: key = y, interval = [x1, x2] (inclusive)
2. For each key we may have many intervals.  Merge overlapping/touching intervals so that the list
   becomes sorted and disjoint.  Merging all keys costs O(M log M) overall.
3. For each house we query:
   * if its x exists in the vertical‑dictionary, binary‑search the merged intervals for that x to see
     whether its y belongs to any interval;
   * otherwise (or additionally) if its y exists in the horizontal‑dictionary, binary‑search there for its x.
   If either test succeeds we count the house.
   The query per house is O(log k) where k is the number of merged intervals for that coordinate.
4. Keep track of the current position while simulating; it becomes the final answer.

Both time and memory fit easily within the limits:
  * O((N+M) log M) time,
  * O(M) extra memory for the intervals.
"""

import sys
from bisect import bisect_right

# ---------- interval utilities ----------

def merge_intervals(intervals):
    """Merge a list of closed intervals [(l, r), ...] into a sorted list of non‑overlapping intervals.
    Intervals are inclusive on both ends.  Overlapping or touching intervals are merged.
    """
    if not intervals:
        return []
    intervals.sort()
    merged = []
    cur_l, cur_r = intervals[0]
    for l, r in intervals[1:]:
        # If l is within or exactly next to current interval, merge.
        if l <= cur_r + 1:
            if r > cur_r:
                cur_r = r
        else:
            merged.append((cur_l, cur_r))
            cur_l, cur_r = l, r
    merged.append((cur_l, cur_r))
    return merged


def value_in_intervals(val, intervals):
    """Return True if val is inside any of the closed intervals (sorted, non‑overlapping)."""
    # Find index of first interval with left > val.
    # bisect_right on (val, inf) works because tuples compare lexicographically.
    idx = bisect_right(intervals, (val, float('inf')))
    if idx == 0:
        return False
    l, r = intervals[idx - 1]
    return l <= val <= r

# ---------- main solver ----------

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    sx = int(next(it))
    sy = int(next(it))

    houses = [(int(next(it)), int(next(it))) for _ in range(N)]

    # Store raw intervals per coordinate.
    vert = {}   # x -> list of (y1, y2)
    horiz = {}  # y -> list of (x1, x2)

    cx, cy = sx, sy
    for _ in range(M):
        d = next(it).decode()
        c = int(next(it))
        if d == 'U':
            nx, ny = cx, cy + c
            lo, hi = cy, ny
            if lo > hi:
                lo, hi = hi, lo
            vert.setdefault(cx, []).append((lo, hi))
        elif d == 'D':
            nx, ny = cx, cy - c
            lo, hi = ny, cy
            if lo > hi:
                lo, hi = hi, lo
            vert.setdefault(cx, []).append((lo, hi))
        elif d == 'R':
            nx, ny = cx + c, cy
            lo, hi = cx, nx
            if lo > hi:
                lo, hi = hi, lo
            horiz.setdefault(cy, []).append((lo, hi))
        elif d == 'L':
            nx, ny = cx - c, cy
            lo, hi = nx, cx
            if lo > hi:
                lo, hi = hi, lo
            horiz.setdefault(cy, []).append((lo, hi))
        else:
            # Should never happen
            raise ValueError('Invalid direction')
        cx, cy = nx, ny

    # Merge intervals for each coordinate for fast binary search.
    for k in list(vert.keys()):
        vert[k] = merge_intervals(vert[k])
    for k in list(horiz.keys()):
        horiz[k] = merge_intervals(horiz[k])

    visited = 0
    for x, y in houses:
        ok = False
        if x in vert and value_in_intervals(y, vert[x]):
            ok = True
        elif y in horiz and value_in_intervals(x, horiz[y]):
            ok = True
        if ok:
            visited += 1

    # Output final position and count.
    sys.stdout.write(f"{cx} {cy} {visited}\n")

if __name__ == "__main__":
    solve()
