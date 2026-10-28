import sys


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    N = H * W
    F = [int(v) for v in data[2:2 + N]]
    p = 2 + N
    Q = int(data[p]); p += 1

    # Edge weight between adjacent blocks = min of their floors.
    # Bottleneck(u,v) = max over paths of min over edges = max over paths of min F on path.
    SH = 20
    MASK = (1 << SH) - 1
    edges = []
    ap = edges.append
    for i in range(H):
        base = i * W
        for j in range(W):
            u = base + j
            if j + 1 < W:
                ap((min(F[u], F[u + 1]) << 40) | (u << SH) | (u + 1))
            if i + 1 < H:
                ap((min(F[u], F[u + W]) << 40) | (u << SH) | (u + W))
    edges.sort(reverse=True)

    qa = [0] * Q; qb = [0] * Q; qy = [0] * Q; qz = [0] * Q
    lists = [[] for _ in range(N)]
    L = [-1] * Q  # bottleneck value; -1 = unknown yet
    for q in range(Q):
        a = int(data[p]); b = int(data[p + 1]); y = int(data[p + 2])
        c = int(data[p + 3]); d = int(data[p + 4]); z = int(data[p + 5]); p += 6
        u = (a - 1) * W + (b - 1)
        v = (c - 1) * W + (d - 1)
        qa[q] = u; qb[q] = v; qy[q] = y; qz[q] = z
        if u == v:
            L[q] = F[u]
        else:
            lists[u].append(q)
            lists[v].append(q)

    parent = list(range(N))
    size = [1] * N

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for e in edges:
        w = e >> 40; u = (e >> SH) & MASK; v = e & MASK
        ru = find(u); rv = find(v)
        if ru == rv:
            continue
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        # merge rv (small) into ru (big)
        parent[rv] = ru
        size[ru] += size[rv]
        small = lists[rv]
        lists[rv] = None
        big = lists[ru]
        for q in small:
            if L[q] >= 0:
                continue
            ra = find(qa[q]); rb = find(qb[q])
            if ra == rb:
                L[q] = w
            else:
                big.append(q)
        lists[ru] = big

    out = []
    for q in range(Q):
        y = qy[q]; z = qz[q]
        l = L[q]
        if l >= min(y, z):
            out.append(abs(y - z))
        else:
            out.append(y + z - 2 * l)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
