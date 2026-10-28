import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); W = int(data[pos + 1]); pos += 2
    N = H * W
    F = [0] * N
    for i in range(N):
        F[i] = int(data[pos + i])
    pos += N
    # Kruskal-style union-find (union by size, no path compression).
    # Cells activated in decreasing height; link value = height at link time.
    parent = list(range(N))
    size = [1] * N
    wlink = [0] * N  # value of the link from node to its parent
    active = [False] * N
    order = sorted(range(N), key=lambda x: -F[x])

    def find_root(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for c in order:
        v = F[c]
        active[c] = True
        r, col = divmod(c, W)
        for nb in ((r - 1, col), (r + 1, col), (r, col - 1), (r, col + 1)):
            nr, nc = nb
            if 0 <= nr < H and 0 <= nc < W:
                d = nr * W + nc
                if not active[d]:
                    continue
                ra = find_root(c)
                rb = find_root(d)
                if ra == rb:
                    continue
                if size[ra] > size[rb]:
                    ra, rb = rb, ra
                parent[ra] = rb
                wlink[ra] = v
                size[rb] += size[ra]

    def bottleneck(s, t):
        # min link value along path from s and t to their LCA
        if s == t:
            return None
        # ancestors of s: map node -> min value from s up to that node (exclusive of link beyond)
        anc = {}
        x = s
        cur = None
        while True:
            anc[x] = cur  # min over links from s to x (None if x == s)
            if parent[x] == x:
                break
            w = wlink[x]
            cur = w if cur is None or w < cur else cur
            x = parent[x]
        x = t
        cur = None
        while True:
            if x in anc:
                a = anc[x]
                if cur is None:
                    return a
                if a is None:
                    return cur
                return min(a, cur)
            if parent[x] == x:
                break
            w = wlink[x]
            cur = w if cur is None or w < cur else cur
            x = parent[x]
        return None

    Q = int(data[pos]); pos += 1
    out = []
    for _ in range(Q):
        A = int(data[pos]) - 1; B = int(data[pos + 1]) - 1; Y = int(data[pos + 2])
        C = int(data[pos + 3]) - 1; D = int(data[pos + 4]) - 1; Z = int(data[pos + 5])
        pos += 6
        s = A * W + B
        t = C * W + D
        L = min(Y, Z)
        if s != t:
            b = bottleneck(s, t)
            if b is not None and b < L:
                L = b
        out.append(Y + Z - 2 * L)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
