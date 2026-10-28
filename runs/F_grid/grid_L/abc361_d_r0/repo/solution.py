import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    t = data[2]
    # Encode colours: bit i = 1 if cell i holds a black stone (cells 0..N+1).
    # State: (mask, k) where empty cells are k and k+1 (mask bits there are 0).
    start_mask = 0
    for i, ch in enumerate(s):
        if ch == 'B':
            start_mask |= 1 << i
    target_mask = 0
    for i, ch in enumerate(t):
        if ch == 'B':
            target_mask |= 1 << i
    start = (start_mask, n)
    target = (target_mask, n)
    if start == target:
        print(0)
        return
    # Quick feasibility check: counts of colours must match.
    if s.count('B') != t.count('B'):
        print(-1)
        return
    dist = {start: 0}
    dq = deque([start])
    while dq:
        mask, k = dq.popleft()
        d = dist[(mask, k)] + 1
        # choose pair (x, x+1) disjoint from empty pair (k, k+1)
        for x in range(0, n + 1):
            if x + 1 >= k and x <= k + 1:
                continue
            c1 = (mask >> x) & 1
            c2 = (mask >> (x + 1)) & 1
            nm = mask & ~(3 << x)
            nm |= (c1 << k) | (c2 << (k + 1))
            st = (nm, x)
            if st not in dist:
                if st == target:
                    print(d)
                    return
                dist[st] = d
                dq.append(st)
    print(-1)


main()
