import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); W = int(data[pos + 1]); pos += 2
    N = H * W
    F = [int(x) for x in data[pos:pos + N]]
    pos += N
    Q = int(data[pos]); pos += 1

    # Activate cells in decreasing F. Union-find without path compression,
    # union by size; T[b] = activation index when b's root got linked under
    # its parent. Along any root path, T increases toward the root.
    order = sorted(range(N), key=lambda c: -F[c])
    INF = N + 5
    par = list(range(N))
    size = [1] * N
    T = [INF] * N
    active = [False] * N

    def find(x):
        while par[x] != x:
            x = par[x]
        return x

    for idx, c in enumerate(order):
        active[c] = True
        r, col = divmod(c, W)
        for nr, nc in ((r - 1, col), (r + 1, col), (r, col - 1), (r, col + 1)):
            if 0 <= nr < H and 0 <= nc < W:
                d = nr * W + nc
                if active[d]:
                    a = find(c)
                    b = find(d)
                    if a != b:
                        if size[a] < size[b]:
                            a, b = b, a
                        par[b] = a
                        size[a] += size[b]
                        T[b] = idx

    out = []
    for _ in range(Q):
        A = int(data[pos]) - 1; B = int(data[pos + 1]) - 1; Y = int(data[pos + 2])
        C = int(data[pos + 3]) - 1; D = int(data[pos + 4]) - 1; Z = int(data[pos + 5])
        pos += 6
        s = A * W + B
        t = C * W + D
        # Climb both nodes to their meeting point; the largest merge index
        # traversed gives the bottleneck (min F along the best path).
        u, v = s, t
        mx = -1
        while u != v:
            if T[u] < T[v]:
                if T[u] > mx:
                    mx = T[u]
                u = par[u]
            else:
                if T[v] > mx:
                    mx = T[v]
                v = par[v]
        xstar = F[s] if mx < 0 else F[order[mx]]
        d = abs(Y - Z)
        alt = Y + Z - 2 * xstar
        out.append(d if d >= alt else alt)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
