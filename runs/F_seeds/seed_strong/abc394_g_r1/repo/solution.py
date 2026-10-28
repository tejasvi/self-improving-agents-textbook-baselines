import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); W = int(data[pos + 1]); pos += 2
    N = H * W
    F = [int(x) for x in data[pos:pos + N]]
    pos += N
    Q = int(data[pos]); pos += 1

    # Activate cells in decreasing height; union-by-size without path compression.
    par = list(range(N))
    size = [1] * N
    val = [0] * N  # threshold at which node got attached to its parent (0 = root)
    active = [False] * N
    order = sorted(range(N), key=F.__getitem__, reverse=True)
    for v in order:
        fv = F[v]
        active[v] = True
        i, j = divmod(v, W)
        nbrs = []
        if i > 0:
            nbrs.append(v - W)
        if i < H - 1:
            nbrs.append(v + W)
        if j > 0:
            nbrs.append(v - 1)
        if j < W - 1:
            nbrs.append(v + 1)
        for u in nbrs:
            if not active[u]:
                continue
            ru = u
            while par[ru] != ru:
                ru = par[ru]
            rv = v
            while par[rv] != rv:
                rv = par[rv]
            if ru == rv:
                continue
            if size[ru] < size[rv]:
                ru, rv = rv, ru
            par[rv] = ru
            size[ru] += size[rv]
            val[rv] = fv

    out = []
    for _ in range(Q):
        A = int(data[pos]); B = int(data[pos + 1]); Y = int(data[pos + 2])
        C = int(data[pos + 3]); D = int(data[pos + 4]); Z = int(data[pos + 5])
        pos += 6
        s = (A - 1) * W + (B - 1)
        t = (C - 1) * W + (D - 1)
        res = F[s] if F[s] < F[t] else F[t]
        u = s
        v = t
        while u != v:
            if val[u] < val[v]:
                u, v = v, u
            if val[u] < res:
                res = val[u]
            u = par[u]
        lo = Y if Y < Z else Z
        hi = Y + Z - lo
        if res >= lo:
            out.append(hi - lo)
        else:
            T = res
            out.append(abs(Y - T) + abs(T - Z))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
