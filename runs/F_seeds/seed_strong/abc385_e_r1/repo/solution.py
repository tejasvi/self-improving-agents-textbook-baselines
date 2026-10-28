import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    deg = [0] * (n + 1)
    us = data[1:2 * n - 1:2]
    vs = data[2:2 * n:2]
    adj = [[] for _ in range(n + 1)]
    for a, b in zip(us, vs):
        a = int(a); b = int(b)
        adj[a].append(b)
        adj[b].append(a)
    for v in range(1, n + 1):
        deg[v] = len(adj[v])
    best = 0
    for c in range(1, n + 1):
        ds = [deg[b] - 1 for b in adj[c] if deg[b] - 1 >= 1]
        if not ds:
            continue
        ds.sort(reverse=True)
        m = 0
        for i, d in enumerate(ds, 1):
            val = i * (1 + d)
            if val > m:
                m = val
        if 1 + m > best:
            best = 1 + m
    print(n - best)

main()
