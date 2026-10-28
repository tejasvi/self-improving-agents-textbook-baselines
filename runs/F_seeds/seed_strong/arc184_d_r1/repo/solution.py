import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    X = [0] * (n + 1)
    Y = [0] * (n + 1)
    for i in range(n):
        X[i + 1] = int(data[1 + 2 * i])
        Y[i + 1] = int(data[2 + 2 * i])
    # Yof[x] = y-value of the point whose X equals x
    Yof = [0] * (n + 2)
    for i in range(1, n + 1):
        Yof[X[i]] = Y[i]

    def valid(xl, xr, yl, yh):
        # Points with X in [xl,xr] and Y in (yl,yh) must each have a
        # concordant partner (same strict direction) inside the region.
        if xl > xr:
            return True
        sel = [Yof[x] for x in range(xl, xr + 1) if yl < Yof[x] < yh]
        k = len(sel)
        if k == 0:
            return True
        if k == 1:
            return False
        # suffix max / prefix min
        sufmax = [0] * k
        m = -1
        for t in range(k - 1, -1, -1):
            if sel[t] > m:
                m = sel[t]
            sufmax[t] = m
        premin = [0] * k
        m = 10 ** 9
        for t in range(k):
            if sel[t] < m:
                m = sel[t]
            premin[t] = m
        for t in range(k):
            ok = False
            if t + 1 < k and sufmax[t + 1] > sel[t]:
                ok = True
            if t > 0 and premin[t - 1] < sel[t]:
                ok = True
            if not ok:
                return False
        return True

    ans = 1 if valid(1, n, 0, n + 1) else 0

    order = sorted(range(1, n + 1), key=lambda i: X[i])
    dp = [0] * (n + 1)
    for j in order:
        xj, yj = X[j], Y[j]
        val = 1 if valid(1, xj - 1, yj, n + 1) else 0
        for i in order:
            if X[i] >= xj:
                break
            if Y[i] > yj and dp[i]:
                if valid(X[i] + 1, xj - 1, yj, Y[i]):
                    val += dp[i]
        dp[j] = val % MOD

    for j in order:
        xj, yj = X[j], Y[j]
        if dp[j] and valid(xj + 1, n, 0, yj):
            ans += dp[j]
    print(ans % MOD)


main()
