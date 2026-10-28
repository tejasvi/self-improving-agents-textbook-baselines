import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); W = int(data[pos + 1]); pos += 2
    N = H * W
    F = [int(x) for x in data[pos:pos + N]]
    pos += N
    order = sorted(range(N), key=lambda c: -F[c])
    active = [False] * N
    par = list(range(N))
    size = [1] * N
    INF = 1 << 60
    idx = [INF] * N
    wt = []  # wt[k] = F value at the k-th union
    for c in order:
        active[c] = True
        i, j = divmod(c, W)
        nbrs = []
        if i > 0:
            nbrs.append(c - W)
        if i < H - 1:
            nbrs.append(c + W)
        if j > 0:
            nbrs.append(c - 1)
        if j < W - 1:
            nbrs.append(c + 1)
        for n in nbrs:
            if not active[n]:
                continue
            ra = c
            while par[ra] != ra:
                ra = par[ra]
            rb = n
            while par[rb] != rb:
                rb = par[rb]
            if ra == rb:
                continue
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            # attach rb under ra
            k = len(wt)
            wt.append(F[c])
            par[rb] = ra
            idx[rb] = k
            size[ra] += size[rb]

    Q = int(data[pos]); pos += 1
    out = []
    for _ in range(Q):
        A = int(data[pos]) - 1; B = int(data[pos + 1]) - 1; Y = int(data[pos + 2])
        C = int(data[pos + 3]) - 1; D = int(data[pos + 4]) - 1; Z = int(data[pos + 5])
        pos += 6
        P = A * W + B
        R = C * W + D
        if P == R:
            M = F[P]
        else:
            x, y = P, R
            mx = -1
            while x != y:
                if idx[x] > idx[y]:
                    x, y = y, x
                if idx[x] == INF:
                    break
                if idx[x] > mx:
                    mx = idx[x]
                x = par[x]
            M = wt[mx] if mx >= 0 else 1
        lo = min(Y, Z)
        if M >= lo:
            out.append(abs(Y - Z))
        else:
            out.append(Y + Z - 2 * M)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
