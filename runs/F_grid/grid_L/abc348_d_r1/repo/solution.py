import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    idx = 0
    H = int(data[idx]); idx += 1
    W = int(data[idx]); idx += 1
    rows = []
    for _ in range(H):
        rows.append(data[idx]); idx += 1
    grid = "".join(rows)
    N = int(data[idx]); idx += 1
    med_at = {}
    meds = []
    for i in range(N):
        r = int(data[idx]) - 1
        c = int(data[idx + 1]) - 1
        e = int(data[idx + 2])
        idx += 3
        pos = r * W + c
        meds.append((pos, e))
        med_at[pos] = i

    start = grid.index('S')
    goal = grid.index('T')
    if start not in med_at:
        print("No")
        return

    # neighbors list for non-obstacle cells
    passable = [ch != '#' for ch in grid]
    nbrs = [None] * (H * W)
    for r in range(H):
        for c in range(W):
            p = r * W + c
            if not passable[p]:
                continue
            lst = []
            if r > 0 and passable[p - W]:
                lst.append(p - W)
            if r < H - 1 and passable[p + W]:
                lst.append(p + W)
            if c > 0 and passable[p - 1]:
                lst.append(p - 1)
            if c < W - 1 and passable[p + 1]:
                lst.append(p + 1)
            nbrs[p] = lst

    used = [False] * N
    used[med_at[start]] = True
    queue = deque([med_at[start]])
    stamp = [0] * (H * W)
    cur = 0
    while queue:
        mi = queue.popleft()
        pos, energy = meds[mi]
        cur += 1
        stamp[pos] = cur
        visited = [pos]
        frontier = [pos]
        d = 0
        while frontier and d < energy:
            d += 1
            nxt = []
            app = nxt.append
            for p in frontier:
                for q in nbrs[p]:
                    if stamp[q] != cur:
                        stamp[q] = cur
                        app(q)
            visited.extend(nxt)
            frontier = nxt
        if stamp[goal] == cur:
            print("Yes")
            return
        for q in visited:
            j = med_at.get(q)
            if j is not None and not used[j]:
                used[j] = True
                queue.append(j)
    print("No")


main()
