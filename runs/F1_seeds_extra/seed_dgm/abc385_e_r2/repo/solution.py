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
        ds = sorted((deg[b] - 1 for b in adj[c]), reverse=True)
        for i, d in enumerate(ds, 1):
            if d < 1:
                break
            val = 1 + i + i * d
            if val > best:
                best = val
    print(n - best)

main()
