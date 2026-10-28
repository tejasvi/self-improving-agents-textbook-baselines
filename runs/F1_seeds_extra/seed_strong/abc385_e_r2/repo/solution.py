import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    deg = [0] * (n + 1)
    us = data[1:2 * n - 1:2]
    vs = data[2:2 * n:2]
    adj = [[] for _ in range(n + 1)]
    for a, b in zip(us, vs):
        a = int(a)
        b = int(b)
        adj[a].append(b)
        adj[b].append(a)
        deg[a] += 1
        deg[b] += 1
    best = 0
    for c in range(1, n + 1):
        ds = [deg[b] - 1 for b in adj[c] if deg[b] >= 2]
        if not ds:
            continue
        ds.sort(reverse=True)
        for k, d in enumerate(ds, 1):
            val = 1 + k * (d + 1)
            if val > best:
                best = val
    print(n - best)


main()
