import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); W = int(data[pos + 1]); pos += 2
    N = H * W
    F = [int(x) for x in data[pos:pos + N]]
    pos += N

    # edges with weight = min(F_u, F_v)
    edges = []
    for i in range(H):
        base = i * W
        for j in range(W):
            u = base + j
            if j + 1 < W:
                v = u + 1
                edges.append((min(F[u], F[v]), u, v))
            if i + 1 < H:
                v = u + W
                edges.append((min(F[u], F[v]), u, v))
    edges.sort(reverse=True)

    parent = list(range(N))
    size = [1] * N
    tlink = [1 << 60] * N   # time of linking to parent (roots: inf)
    wlink = [0] * N         # weight of the link to parent
    t = 0

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        t += 1
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
        tlink[rv] = t
        wlink[rv] = w

    q = int(data[pos]); pos += 1
    out = []
    INF = 1 << 60
    for _ in range(q):
        a = int(data[pos]) - 1; b = int(data[pos + 1]) - 1
        y = int(data[pos + 2])
        c = int(data[pos + 3]) - 1; d = int(data[pos + 4]) - 1
        z = int(data[pos + 5])
        pos += 6
        s = a * W + b
        e = c * W + d
        best = INF
        u = s; v = e
        while u != v:
            if tlink[u] < tlink[v]:
                if wlink[u] < best:
                    best = wlink[u]
                u = parent[u]
            else:
                if wlink[v] < best:
                    best = wlink[v]
                v = parent[v]
        m = y if y < z else z
        if best < m:
            m = best
        out.append(y + z - 2 * m)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
