import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); W = int(data[pos + 1]); pos += 2
    n = H * W
    F = [0] * n
    for i in range(n):
        F[i] = int(data[pos + i])
    pos += n

    order = sorted(range(n), key=lambda c: -F[c])
    vals = [F[c] for c in order]  # value at activation time k
    par = list(range(n))
    size = [1] * n
    INF = n
    t = [INF] * n  # time index at which node got attached to its parent
    active = [False] * n

    def find(x):
        while par[x] != x:
            x = par[x]
        return x

    for k in range(n):
        c = order[k]
        active[c] = True
        r, col = divmod(c, W)
        nbs = []
        if r > 0:
            nbs.append(c - W)
        if r < H - 1:
            nbs.append(c + W)
        if col > 0:
            nbs.append(c - 1)
        if col < W - 1:
            nbs.append(c + 1)
        for nb in nbs:
            if not active[nb]:
                continue
            ra = find(c)
            rb = find(nb)
            if ra == rb:
                continue
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            par[rb] = ra
            size[ra] += size[rb]
            t[rb] = k

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
        if a == c:
            T = F[a]
        else:
            mx = -1
            while a != c:
                if t[a] < t[c]:
                    if t[a] > mx:
                        mx = t[a]
                    a = par[a]
                else:
                    if t[c] > mx:
                        mx = t[c]
                    c = par[c]
            T = vals[mx]
        lo = Y if Y < Z else Z
        if T >= lo:
            out.append(abs(Y - Z))
        else:
            out.append(Y + Z - 2 * T)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
