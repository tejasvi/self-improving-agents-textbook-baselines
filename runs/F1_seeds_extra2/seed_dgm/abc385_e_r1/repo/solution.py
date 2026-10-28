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
        ks = [deg[b] - 1 for b in adj[c] if deg[b] - 1 >= 1]
        if not ks:
            continue
        ks.sort(reverse=True)
        for i, k in enumerate(ks, 1):
            val = i * (k + 1)
            if val > best:
                best = val
    kept = best + 1
    print(n - kept)

main()
