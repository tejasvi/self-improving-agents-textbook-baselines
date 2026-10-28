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
    # activate cells by decreasing F; time = rank in this order
    order = sorted(range(n), key=lambda c: -F[c])
    rank = [0] * n
    for t, c in enumerate(order):
        rank[c] = t
    INF = 1 << 60
    par = list(range(n))
    size = [1] * n
    T = [INF] * n  # link time of node to its parent
    active = [False] * n
    for t, c in enumerate(order):
        active[c] = True
        r, col = divmod(c, W)
        for nr, nc in ((r - 1, col), (r + 1, col), (r, col - 1), (r, col + 1)):
            if 0 <= nr < H and 0 <= nc < W:
                d = nr * W + nc
                if not active[d]:
                    continue
                # find roots without path compression
                a = c
                while par[a] != a:
                    a = par[a]
                b = d
                while par[b] != b:
                    b = par[b]
                if a == b:
                    continue
                if size[a] < size[b]:
                    a, b = b, a
                par[b] = a
                size[a] += size[b]
                T[b] = t
    Q = int(data[pos]); pos += 1
    out = []
    for _ in range(Q):
        A = int(data[pos]) - 1; B = int(data[pos + 1]) - 1; Y = int(data[pos + 2])
        C = int(data[pos + 3]) - 1; D = int(data[pos + 4]) - 1; Z = int(data[pos + 5])
        pos += 6
        u = A * W + B
        v = C * W + D
        res = 0
        while u != v:
            if T[u] < T[v]:
                res = T[u] if T[u] > res else res
                u = par[u]
            else:
                res = T[v] if T[v] > res else res
                v = par[v]
        # res is the time at which they become connected (max link time on path)
        bott = F[u] if A * W + B == C * W + D else F[order[res]]
        m = bott
        if Y < m: m = Y
        if Z < m: m = Z
        out.append(Y + Z - 2 * m)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
