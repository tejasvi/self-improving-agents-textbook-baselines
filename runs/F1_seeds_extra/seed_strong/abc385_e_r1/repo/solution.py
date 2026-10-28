import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    us = data[1:2 * n - 1:2]
    vs = data[2:2 * n:2]
    U = list(map(int, us))
    V = list(map(int, vs))
    deg = [0] * (n + 1)
    for u, v in zip(U, V):
        deg[u] += 1
        deg[v] += 1
    lists = [[] for _ in range(n + 1)]
    for u, v in zip(U, V):
        lists[u].append(deg[v] - 1)
        lists[v].append(deg[u] - 1)
    best = 0  # kept vertices excluding center count
    for c in range(1, n + 1):
        ts = lists[c]
        if not ts:
            continue
        ts.sort(reverse=True)
        for i, t in enumerate(ts, 1):
            if t < 1:
                break
            val = i * (1 + t)
            if val > best:
                best = val
    print(n - (1 + best))

main()
