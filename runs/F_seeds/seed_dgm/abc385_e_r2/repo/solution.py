import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    deg = [0] * (n + 1)
    us = data[1:2 * n - 1:2]
    vs = data[2:2 * n:2]
    eu = [0] * (n - 1)
    ev = [0] * (n - 1)
    for i in range(n - 1):
        u = int(us[i])
        v = int(vs[i])
        eu[i] = u
        ev[i] = v
        deg[u] += 1
        deg[v] += 1
    adj = [[] for _ in range(n + 1)]
    for i in range(n - 1):
        u = eu[i]
        v = ev[i]
        adj[u].append(deg[v] - 1)
        adj[v].append(deg[u] - 1)
    best = 0
    for c in range(1, n + 1):
        vals = adj[c]
        if not vals:
            continue
        vals.sort(reverse=True)
        for k in range(1, len(vals) + 1):
            y = vals[k - 1]
            if y < 1:
                break
            kept = 1 + k * (1 + y)
            if kept > best:
                best = kept
    print(n - best)


main()
