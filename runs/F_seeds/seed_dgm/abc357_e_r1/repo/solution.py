import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for x in a:
        indeg[x] += 1

    # Peel off tree nodes (Kahn's algorithm); remaining nodes lie on cycles.
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

    # Identify cycles and their lengths.
    on_cycle = [not r for r in removed]
    cyc_len = [0] * n  # cycle length for cycle nodes
    visited = [False] * n
    for s in range(n):
        if on_cycle[s] and not visited[s]:
            nodes = []
            u = s
            while not visited[u]:
                visited[u] = True
                nodes.append(u)
                u = a[u]
            c = len(nodes)
            for u in nodes:
                cyc_len[u] = c

    # Depth of tree nodes: process so that a[u] is handled before u.
    depth = [0] * n
    for u in reversed(order):
        depth[u] = depth[a[u]] + 1

    total = 0
    for u in range(n):
        if on_cycle[u]:
            total += cyc_len[u]
        else:
            # Need cycle length of the cycle this tree node flows into.
            pass

    # Cycle length for tree nodes: propagate from the cycle node reached.
    # Reverse order: a[u] is processed before u, so root[u] = root[a[u]].
    root_c = cyc_len[:]
    for u in reversed(order):
        root_c[u] = root_c[a[u]]
    for u in order:
        total += depth[u] + root_c[u]

    print(total)


main()
