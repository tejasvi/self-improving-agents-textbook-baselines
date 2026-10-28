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
        vals = [deg[b] - 1 for b in adj[c]]
        vals.sort(reverse=True)
        for i, s in enumerate(vals, 1):
            if s < 1:
                break
            val = i * (1 + s)
            if val > best:
                best = val
    print(n - (1 + best))

main()
