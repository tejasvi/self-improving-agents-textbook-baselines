import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    idx = 0
    H = int(data[idx]); idx += 1
    W = int(data[idx]); idx += 1
    rows = data[idx:idx + H]
    idx += H
    N = int(data[idx]); idx += 1

    # padded grid of width W2 with a blocked border to avoid bounds checks
    W2 = W + 2
    size = (H + 2) * W2
    blocked = bytearray([1]) * size
    start = goal = -1
    for i in range(H):
        row = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            ch = row[j]
            k = base + j
            if ch != '#':
                blocked[k] = 0
            if ch == 'S':
                start = k
            elif ch == 'T':
                goal = k

    meds = []
    med_index = {}
    for _ in range(N):
        r = int(data[idx]); c = int(data[idx + 1]); e = int(data[idx + 2])
        idx += 3
        cell = r * W2 + c  # (r-1+1)*W2 + (c-1+1)
        med_index[cell] = len(meds)
        meds.append((cell, e))

    if start not in med_index:
        print("No")
        return

    used = [False] * N
    used[med_index[start]] = True
    queue = deque([med_index[start]])
    stamp = [0] * size
    cur = 0
    while queue:
        mi = queue.popleft()
        src, energy = meds[mi]
        cur += 1
        stamp[src] = cur
        frontier = [src]
        d = 0
        while frontier and d < energy:
            d += 1
            nxt = []
            app = nxt.append
            for u in frontier:
                for v in (u - W2, u + W2, u - 1, u + 1):
                    if stamp[v] == cur or blocked[v]:
                        continue
                    stamp[v] = cur
                    if v == goal:
                        print("Yes")
                        return
                    app(v)
                    j = med_index.get(v)
                    if j is not None and not used[j]:
                        used[j] = True
                        queue.append(j)
            frontier = nxt
    print("No")


main()
