import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    us = data[1:2 * n - 1:2]
    vs = data[2:2 * n:2]
    deg = [0] * (n + 1)
    U = [0] * (n - 1)
    V = [0] * (n - 1)
    for i in range(n - 1):
        u = int(us[i]); v = int(vs[i])
        U[i] = u; V[i] = v
        deg[u] += 1
        deg[v] += 1
    cand = [[] for _ in range(n + 1)]
    for i in range(n - 1):
        u = U[i]; v = V[i]
        cand[u].append(deg[v] - 1)
        cand[v].append(deg[u] - 1)
    best = 0
    for c in range(1, n + 1):
        lst = cand[c]
        if not lst:
            continue
        lst.sort(reverse=True)
        for i, d in enumerate(lst, 1):
            if d < 1:
                break
            val = i * (d + 1) + 1
            if val > best:
                best = val
    print(n - best)

main()
