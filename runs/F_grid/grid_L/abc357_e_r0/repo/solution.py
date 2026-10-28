import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for v in a:
        indeg[v] += 1

    # Peel off tail vertices (in-degree 0) in topological order.
    order = [i for i in range(n) if indeg[i] == 0]
    head = 0
    while head < len(order):
        u = order[head]
        head += 1
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            order.append(v)

    reach = [0] * n
    on_cycle = [indeg[i] > 0 for i in range(n)]
    visited = [False] * n
    for s in range(n):
        if on_cycle[s] and not visited[s]:
            # Walk the cycle containing s.
            cyc = []
            u = s
            while not visited[u]:
                visited[u] = True
                cyc.append(u)
                u = a[u]
            L = len(cyc)
            for c in cyc:
                reach[c] = L

    # Tail vertices: process in reverse peel order so a[u] is already set.
    for u in reversed(order):
        reach[u] = reach[a[u]] + 1

    print(sum(reach))


main()
