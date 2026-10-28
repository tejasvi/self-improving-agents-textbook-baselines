import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for x in a:
        indeg[x] += 1

    # Kahn: peel off vertices with in-degree 0 (tree vertices).
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
    on_cycle = [indeg[i] > 0 for i in range(n)]

    # Cycle vertices: reach = cycle length.
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
            for c in cyc:
                reach[c] = L

    # Tree vertices in reverse peel order: parent resolved before child.
    for u in reversed(order):
        reach[u] = 1 + reach[a[u]]

    print(sum(reach))


main()
