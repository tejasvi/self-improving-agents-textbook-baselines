import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    deg = [0] * (n + 1)
    us = data[1:2 * n - 1:2]
    vs = data[2:2 * n:2]
    eu = [int(x) for x in us]
    ev = [int(x) for x in vs]
    for a, b in zip(eu, ev):
        deg[a] += 1
        deg[b] += 1
    # For each center c, collect d(b) = deg(b)-1 over neighbors b with d>=1
    lists = [[] for _ in range(n + 1)]
    for a, b in zip(eu, ev):
        da = deg[a] - 1
        db = deg[b] - 1
        if db >= 1:
            lists[a].append(db)
        if da >= 1:
            lists[b].append(da)
    best = 0
    for c in range(1, n + 1):
        lst = lists[c]
        if not lst:
            continue
        lst.sort(reverse=True)
        for j, d in enumerate(lst, 1):
            val = 1 + j * (1 + d)
            if val > best:
                best = val
    print(n - best)


main()
