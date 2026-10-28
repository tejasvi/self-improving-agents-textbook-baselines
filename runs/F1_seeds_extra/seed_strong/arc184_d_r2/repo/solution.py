import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    X = [0] * n
    Y = [0] * n
    for i in range(n):
        X[i] = int(data[1 + 2 * i])
        Y[i] = int(data[2 + 2 * i])
    # Points indexed by x coordinate (X is a permutation of 1..n).
    # py[v] = Y of the point with X = v (1-based), and vice versa.
    byx = [0] * (n + 2)
    byy = [0] * (n + 2)
    for i in range(n):
        byx[X[i]] = i
        byy[Y[i]] = i
    # Bitmask helpers indexed by coordinate value.
    # xlt[v]: points with X < v ; xgt[v]: points with X > v
    # ylt[v]: points with Y < v ; ygt[v]: points with Y > v
    xlt = [0] * (n + 2)
    ylt = [0] * (n + 2)
    acc = 0
    for v in range(1, n + 2):
        xlt[v] = acc
        if v <= n:
            acc |= 1 << byx[v]
    acc = 0
    for v in range(1, n + 2):
        ylt[v] = acc
        if v <= n:
            acc |= 1 << byy[v]
    full = (1 << n) - 1
    xgt = [full & ~(xlt[v] | (1 << byx[v]) if 1 <= v <= n else xlt[v]) for v in range(n + 2)]
    ygt = [full & ~(ylt[v] | (1 << byy[v]) if 1 <= v <= n else ylt[v]) for v in range(n + 2)]
    # comparable partners: SW (X<,Y<) or NE (X>,Y>)
    comp = [0] * n
    for i in range(n):
        xi, yi = X[i], Y[i]
        sw = xlt[xi] & ylt[yi]
        ne = xgt[xi] & ygt[yi]
        comp[i] = sw | ne

    def valid(mask):
        m = mask
        while m:
            low = m & -m
            r = low.bit_length() - 1
            if not (comp[r] & mask):
                return False
            m ^= low
        return True

    # points sorted by X
    order = [byx[v] for v in range(1, n + 1)]
    f = [0] * n
    for b in order:  # increasing X
        xb, yb = X[b], Y[b]
        total = 0
        if valid(xlt[xb] & ygt[yb]):
            total = 1
        # predecessors a: X_a < X_b, Y_a > Y_b
        for a in order:
            if X[a] >= xb:
                break
            ya = Y[a]
            if ya <= yb or f[a] == 0:
                continue
            rect = xlt[xb] & xgt[X[a]] & ygt[yb] & ylt[ya]
            if valid(rect):
                total += f[a]
        f[b] = total % MOD
    ans = 1 if valid(full) else 0
    for b in order:
        if valid(xgt[X[b]] & ylt[Y[b]]):
            ans += f[b]
    print(ans % MOD)


main()
