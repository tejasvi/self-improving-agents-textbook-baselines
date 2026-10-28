import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    deg = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    idx = 1
    for _ in range(n - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1
    best = 0
    for c in range(1, n + 1):
        vals = [deg[b] - 1 for b in adj[c] if deg[b] - 1 >= 1]
        if not vals:
            continue
        vals.sort(reverse=True)
        for i, a in enumerate(vals, 1):
            kept = 1 + i * (1 + a)
            if kept > best:
                best = kept
    print(n - best)

main()
