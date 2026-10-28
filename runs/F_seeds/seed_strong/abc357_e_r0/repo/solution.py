import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]
    indeg = [0] * n
    for x in a:
        indeg[x] += 1
    # Peel leaves (Kahn); removed vertices are the tree (non-cycle) vertices.
    order = [i for i in range(n) if indeg[i] == 0]
    idx = 0
    while idx < len(order):
        u = order[idx]
        idx += 1
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            order.append(v)
    on_cycle = [indeg[i] > 0 for i in range(n)]
    # cl[u]: length of cycle reached from u (for cycle vertices: own cycle)
    cl = [0] * n
    for i in range(n):
        if on_cycle[i] and cl[i] == 0:
            cyc = [i]
            j = a[i]
            while j != i:
                cyc.append(j)
                j = a[j]
            L = len(cyc)
            for c in cyc:
                cl[c] = L
    # depth[u]: number of tree vertices on path from u to cycle, including u
    # (cycle vertices have depth 0). a[u] is processed before u in reversed order.
    depth = [0] * n
    for u in reversed(order):
        v = a[u]
        depth[u] = depth[v] + 1
        cl[u] = cl[v]
    total = 0
    for i in range(n):
        total += depth[i] + cl[i]
    print(total)


main()
