import sys


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    N = H * W
    F = list(map(int, data[2:2 + N]))
    pos = 2 + N
    Q = int(data[pos]); pos += 1
    vals = list(map(int, data[pos:pos + 6 * Q]))

    qs = [0] * Q
    qt = [0] * Q
    qy = [0] * Q
    qz = [0] * Q
    ans = [-1] * Q
    M = [0] * Q
    lists = [[] for _ in range(N)]
    for i in range(Q):
        k = 6 * i
        s = (vals[k] - 1) * W + vals[k + 1] - 1
        y = vals[k + 2]
        t = (vals[k + 3] - 1) * W + vals[k + 4] - 1
        z = vals[k + 5]
        qs[i] = s; qt[i] = t; qy[i] = y; qz[i] = z
        if s == t:
            ans[i] = abs(y - z)
        else:
            lists[s].append(i)
            lists[t].append(i)

    parent = list(range(N))

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    active = [False] * N
    order = sorted(range(N), key=F.__getitem__, reverse=True)
    for c in order:
        v = F[c]
        active[c] = True
        r, col = divmod(c, W)
        nbs = []
        if r > 0: nbs.append(c - W)
        if r < H - 1: nbs.append(c + W)
        if col > 0: nbs.append(c - 1)
        if col < W - 1: nbs.append(c + 1)
        for nb in nbs:
            if not active[nb]:
                continue
            ra = c
            while parent[ra] != ra:
                parent[ra] = parent[parent[ra]]
                ra = parent[ra]
            rb = nb
            while parent[rb] != rb:
                parent[rb] = parent[parent[rb]]
                rb = parent[rb]
            if ra == rb:
                continue
            if len(lists[ra]) > len(lists[rb]):
                ra, rb = rb, ra
            parent[ra] = rb
            la = lists[ra]
            lists[ra] = None
            lb = lists[rb]
            for q in la:
                if ans[q] >= 0:
                    continue
                x = qs[q]
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                y = qt[q]
                while parent[y] != y:
                    parent[y] = parent[parent[y]]
                    y = parent[y]
                if x == y:
                    M[q] = v
                    ans[q] = 0
                else:
                    lb.append(q)

    out = []
    for i in range(Q):
        if ans[i] >= 0 and qs[i] == qt[i]:
            out.append(ans[i])
            continue
        y = qy[i]; z = qz[i]
        m = M[i]
        mn = y if y < z else z
        if m >= mn:
            out.append(abs(y - z))
        else:
            out.append(y + z - 2 * m)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
