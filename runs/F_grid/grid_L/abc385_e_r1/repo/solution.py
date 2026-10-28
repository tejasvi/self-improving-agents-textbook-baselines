import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    deg = [0] * (n + 1)
    us = data[1:2 * n - 1:2]
    vs = data[2:2 * n:2]
    adj = [[] for _ in range(n + 1)]
    for a, b in zip(us, vs):
        u = int(a)
        v = int(b)
        adj[u].append(v)
        adj[v].append(u)
    for i in range(1, n + 1):
        deg[i] = len(adj[i])

    best = 0
    for c in range(1, n + 1):
        ws = [deg[v] - 1 for v in adj[c] if deg[v] - 1 >= 1]
        if not ws:
            continue
        ws.sort(reverse=True)
        for k, w in enumerate(ws, 1):
            val = 1 + k + k * w
            if val > best:
                best = val
    print(n - best)


main()
