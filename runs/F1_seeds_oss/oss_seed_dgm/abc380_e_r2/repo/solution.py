# Solution for the 1D Bucket Tool problem.
# Uses an ordered map of intervals (start -> (end, color)) with binary search.
# Each query of type 1 recolors the whole contiguous segment of the same color
# containing cell x, and merges with adjacent intervals of the new color.
# Queries of type 2 output the current count of cells of a given color.

import sys
import bisect

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))

    # count of cells for each color (1-indexed)
    cnt = [0] * (N + 1)
    for i in range(1, N + 1):
        cnt[i] = 1

    # intervals: start -> (end, color)
    intervals = {}
    starts = []  # sorted list of interval start positions
    for i in range(1, N + 1):
        intervals[i] = (i, i)
        starts.append(i)

    out = []
    for _ in range(Q):
        typ = int(next(it))
        if typ == 1:
            x = int(next(it))
            newc = int(next(it))
            # locate interval containing x
            idx = bisect.bisect_right(starts, x) - 1
            s = starts[idx]
            e, oldc = intervals[s]
            if oldc == newc:
                continue
            length = e - s + 1
            cnt[oldc] -= length
            cnt[newc] += length
            # remove current interval
            del intervals[s]
            starts.pop(idx)
            # prepare new merged interval boundaries
            new_s = s
            new_e = e
            # check left neighbor (if any) for possible merge
            if idx - 1 >= 0:
                left_start = starts[idx - 1]
                left_end, left_color = intervals[left_start]
                if left_end == s - 1 and left_color == newc:
                    # merge with left interval
                    new_s = left_start
                    # remove left interval
                    del intervals[left_start]
                    starts.pop(idx - 1)
                    idx -= 1  # new interval will be inserted at this position
            # check right neighbor (after possible left removal)
            if idx < len(starts):
                right_start = starts[idx]
                right_end, right_color = intervals[right_start]
                if right_start == e + 1 and right_color == newc:
                    # merge with right interval
                    new_e = right_end
                    # remove right interval
                    del intervals[right_start]
                    starts.pop(idx)
            # insert the new (or merged) interval
            intervals[new_s] = (new_e, newc)
            bisect.insort(starts, new_s)
        else:  # typ == 2
            c = int(next(it))
            out.append(str(cnt[c]))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
