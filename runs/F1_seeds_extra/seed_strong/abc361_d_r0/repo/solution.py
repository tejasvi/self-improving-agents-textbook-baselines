import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    S = data[1]
    T = data[2]

    def enc(s):
        v = 0
        for i, c in enumerate(s):
            if c == 'B':
                v |= 1 << i
        return v

    # State: (b, g): b = bits of stones in list order (bit i = 1 if black),
    # g = 0-indexed left cell of the empty pair (cells g, g+1 empty).
    # Stone at list index i sits in cell i if i < g, else cell i+2.
    src = enc(S)
    dst = enc(T)
    if src == dst:
        print(0)
        return
    full = 1 << n
    total = (n + 1) * full
    dist = [-1] * total
    start = n * full + src
    goal = n * full + dst
    dist[start] = 0
    dq = deque([start])
    while dq:
        st = dq.popleft()
        d = dist[st] + 1
        g, b = divmod(st, full)
        # Pair entirely to the left of the gap: list indices x, x+1 with x+1 <= g-1.
        # Moves to new gap at x.
        for x in range(g - 1):
            pair = (b >> x) & 3
            low = b & ((1 << x) - 1)
            mid = (b >> (x + 2)) & ((1 << (g - x - 2)) - 1)
            high = b >> g
            nb = low | (mid << x) | (pair << (g - 2)) | (high << g)
            ns = x * full + nb
            if dist[ns] < 0:
                dist[ns] = d
                if ns == goal:
                    print(d)
                    return
                dq.append(ns)
        # Pair entirely to the right of the gap: list indices j, j+1 with j >= g.
        # Moves to new gap at j+2.
        for j in range(g, n - 1):
            pair = (b >> j) & 3
            low = b & ((1 << g) - 1)
            mid = (b >> g) & ((1 << (j - g)) - 1)
            high = b >> (j + 2)
            nb = low | (pair << g) | (mid << (g + 2)) | (high << (j + 2))
            ns = (j + 2) * full + nb
            if dist[ns] < 0:
                dist[ns] = d
                if ns == goal:
                    print(d)
                    return
                dq.append(ns)
    print(-1)

main()
