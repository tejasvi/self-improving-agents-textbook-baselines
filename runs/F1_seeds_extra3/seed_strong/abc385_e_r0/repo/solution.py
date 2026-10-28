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
    adj = [[] for _ in range(n + 1)]
    for a, b in zip(eu, ev):
        adj[a].append(b)
        adj[b].append(a)
    best = 0
    for c in range(1, n + 1):
        nb = adj[c]
        if not nb:
            continue
        vals = sorted((deg[u] - 1 for u in nb), reverse=True)
        for k in range(1, len(vals) + 1):
            y = vals[k - 1]
            if y < 1:
                break
            kept = 1 + k * (1 + y)
            if kept > best:
                best = kept
    print(n - best)

main()
