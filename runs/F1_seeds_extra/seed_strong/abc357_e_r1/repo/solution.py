import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [0] * n
    indeg = [0] * n
    for i in range(n):
        x = int(data[1 + i]) - 1
        a[i] = x
        indeg[x] += 1

    # Peel off tree vertices (in-degree zero), recording peel order.
    order = []
    stack = [i for i in range(n) if indeg[i] == 0]
    removed = [False] * n
    while stack:
        u = stack.pop()
        removed[u] = True
        order.append(u)
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            stack.append(v)

    # Cycle vertices: each reaches its whole cycle.
    reach = [0] * n
    visited = [False] * n
    for i in range(n):
        if not removed[i] and not visited[i]:
            cyc = []
            j = i
            while not visited[j]:
                visited[j] = True
                cyc.append(j)
                j = a[j]
            L = len(cyc)
            for c in cyc:
                reach[c] = L

    # Tree vertices: reach(u) = 1 + reach(a[u]); peel order reversed
    # guarantees a[u] is computed first.
    for u in reversed(order):
        reach[u] = reach[a[u]] + 1

    print(sum(reach))


main()
