import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]
    indeg = [0] * n
    for x in a:
        indeg[x] += 1
    # Peel vertices not on cycles (Kahn's algorithm); order = tree vertices.
    q = [i for i in range(n) if indeg[i] == 0]
    head = 0
    while head < len(q):
        u = q[head]
        head += 1
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
    on_cycle = [indeg[i] > 0 for i in range(n)]
    cl = [0] * n  # cycle length for each vertex's cycle
    seen = [False] * n
    for i in range(n):
        if on_cycle[i] and not seen[i]:
            cyc = []
            j = i
            while not seen[j]:
                seen[j] = True
                cyc.append(j)
                j = a[j]
            L = len(cyc)
            for c in cyc:
                cl[c] = L
    # Process tree vertices in reverse peel order: parent (a[u]) is finalized first.
    d = [0] * n
    for u in reversed(q):
        if not on_cycle[u]:
            v = a[u]
            d[u] = d[v] + 1
            cl[u] = cl[v]
    total = 0
    for i in range(n):
        total += cl[i] + d[i]
    print(total)


main()
