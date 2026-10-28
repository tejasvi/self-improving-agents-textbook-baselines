import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]

    indeg = [0] * n
    for v in a:
        indeg[v] += 1
    # Peel vertices with in-degree 0 (tree vertices); remaining are cycle vertices.
    order = [i for i in range(n) if indeg[i] == 0]
    idx = 0
    while idx < len(order):
        u = order[idx]
        idx += 1
        w = a[u]
        indeg[w] -= 1
        if indeg[w] == 0:
            order.append(w)

    on_cycle = [indeg[i] > 0 for i in range(n)]
    cyc_len = [0] * n
    seen = [False] * n
    for s in range(n):
        if on_cycle[s] and not seen[s]:
            cyc = []
            v = s
            while not seen[v]:
                seen[v] = True
                cyc.append(v)
                v = a[v]
            L = len(cyc)
            for v in cyc:
                cyc_len[v] = L

    depth = [0] * n
    # Reverse peel order: a[u] is processed before u (a[u] is either on cycle or peeled later).
    for u in reversed(order):
        depth[u] = depth[a[u]] + 1

    # Total: sum over u of depth[u] + cycle length of the cycle u enters.
    total = 0
    for u in range(n):
        total += depth[u]
    # cycle length for each vertex: propagate from cycle; tree vertices take cycle len of target.
    clen = cyc_len[:]
    for u in reversed(order):
        clen[u] = clen[a[u]]
    for u in range(n):
        total += clen[u]
    print(total)


main()
