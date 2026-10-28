import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for v in a:
        indeg[v] += 1

    # Peel off tail vertices (indegree 0 repeatedly).
    order = [i for i in range(n) if indeg[i] == 0]
    idx = 0
    while idx < len(order):
        u = order[idx]
        idx += 1
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            order.append(v)

    reach = [0] * n
    on_cycle = [d > 0 for d in indeg]
    visited = [False] * n
    for i in range(n):
        if on_cycle[i] and not visited[i]:
            cyc = []
            j = i
            while not visited[j]:
                visited[j] = True
                cyc.append(j)
                j = a[j]
            L = len(cyc)
            for j in cyc:
                reach[j] = L

    # Tail vertices: reverse peel order guarantees a[u] is computed first.
    for u in reversed(order):
        reach[u] = reach[a[u]] + 1

    print(sum(reach))


main()
