# Write your solution here. Read from stdin, write to stdout.

import sys
import bisect

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    # counts per color, 1-indexed
    cnt = [0] * (N + 1)
    for i in range(1, N + 1):
        cnt[i] = 1
    # intervals: start -> (end, color)
    intervals = {}
    starts = []
    for i in range(1, N + 1):
        intervals[i] = (i, i)
        starts.append(i)
    # starts is already sorted
    out_lines = []
    for _ in range(Q):
        typ = int(next(it))
        if typ == 1:
            x = int(next(it))
            c = int(next(it))
            # find interval containing x
            idx = bisect.bisect_right(starts, x) - 1
            st = starts[idx]
            en, col = intervals[st]
            if col == c:
                continue
            length = en - st + 1
            cnt[col] -= length
            cnt[c] += length
            # remove current interval
            del intervals[st]
            starts.pop(idx)
            new_start = st
            new_end = en
            # merge left if same color c
            if idx > 0:
                left_start = starts[idx - 1]
                left_end, left_col = intervals[left_start]
                if left_col == c:
                    new_start = left_start
                    # remove left interval
                    del intervals[left_start]
                    starts.pop(idx - 1)
                    idx -= 1  # shift index after removal
            # merge right if same color c
            if idx < len(starts):
                right_start = starts[idx]
                right_end, right_col = intervals[right_start]
                if right_col == c:
                    new_end = right_end
                    del intervals[right_start]
                    starts.pop(idx)
            # insert merged interval
            intervals[new_start] = (new_end, c)
            bisect.insort(starts, new_start)
        else:  # typ == 2
            c = int(next(it))
            out_lines.append(str(cnt[c]))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
