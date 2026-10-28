import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]
    idx = 1
    for _ in range(n - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
    deg = [len(a) for a in adj]
    best = 0
    for c in range(1, n + 1):
        ds = [deg[b] - 1 for b in adj[c]]
        if not ds:
            continue
        ds.sort(reverse=True)
        for i, d in enumerate(ds, 1):
            if d < 1:
                break
            val = 1 + i * (1 + d)
            if val > best:
                best = val
    print(n - best)

main()
