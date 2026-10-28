import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); W = int(data[pos + 1]); pos += 2
    N = H * W
    F = [int(x) for x in data[pos:pos + N]]
    pos += N

    # edges with weight min(F_u, F_v)
    edges = []
    for i in range(H):
        base = i * W
        for j in range(W):
            u = base + j
            fu = F[u]
            if j + 1 < W:
                v = u + 1
                edges.append((min(fu, F[v]), u, v))
            if i + 1 < H:
                v = u + W
                edges.append((min(fu, F[v]), u, v))
    edges.sort(key=lambda e: -e[0])

    # DSU without path compression, union by size; record link time and weight
    parent = list(range(N))
    size = [1] * N
    INF = float('inf')
    tm = [INF] * N   # time (edge index) when node got linked to its parent
    wt = [0] * N     # weight of that link

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for t, (w, u, v) in enumerate(edges):
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
        tm[rv] = t
        wt[rv] = w

    def bottleneck(a, c):
        # maximin path value between a and c in the max spanning forest
        if a == c:
            return INF
        res = INF
        while a != c:
            if tm[a] < tm[c]:
                if wt[a] < res:
                    res = wt[a]
                a = parent[a]
            else:
                if wt[c] < res:
                    res = wt[c]
                c = parent[c]
        return res

    Q = int(data[pos]); pos += 1
    out = []
    for _ in range(Q):
        A = int(data[pos]) - 1
        B = int(data[pos + 1]) - 1
        Y = int(data[pos + 2])
        C = int(data[pos + 3]) - 1
        D = int(data[pos + 4]) - 1
        Z = int(data[pos + 5])
        pos += 6
        a = A * W + B
        c = C * W + D
        base = abs(Y - Z)
        m = Y if Y < Z else Z
        bn = bottleneck(a, c)
        if bn < m:
            base += 2 * (m - int(bn))
        out.append(base)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
