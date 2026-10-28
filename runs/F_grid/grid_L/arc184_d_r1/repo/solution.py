import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    # yAt[x] = Y coordinate of the ball whose X coordinate is x (1-indexed)
    yAt = [0] * (n + 2)
    for i in range(n):
        x = int(data[1 + 2 * i])
        y = int(data[2 + 2 * i])
        yAt[x] = y

    def valid(xlo, xhi, ylo, yhi):
        # Points with xlo < x < xhi and ylo < y < yhi (x enumerated in order).
        # Valid iff every such point has a comparable partner inside the set.
        ys = []
        for x in range(xlo + 1, xhi):
            y = yAt[x]
            if ylo < y < yhi:
                ys.append(y)
        m = len(ys)
        if m == 0:
            return True
        if m == 1:
            return False
        # prefix min and suffix max
        pmin = [0] * m
        cur = ys[0]
        for i in range(m):
            if ys[i] < cur:
                cur = ys[i]
            pmin[i] = cur
        smax = [0] * m
        cur = ys[m - 1]
        for i in range(m - 1, -1, -1):
            if ys[i] > cur:
                cur = ys[i]
            smax[i] = cur
        for i in range(m):
            y = ys[i]
            ok = False
            if i + 1 < m and smax[i + 1] > y:
                ok = True
            elif i > 0 and pmin[i - 1] < y:
                ok = True
            if not ok:
                return False
        return True

    total_full = valid(0, n + 1, 0, n + 1)  # empty antichain: whole set has no isolated ball
    ans = 1 if total_full else 0

    # Chain DP over decreasing pairs (x increasing, y decreasing).
    # dp[d] = number of valid chains ending at d (with cell0 and all inner cells valid).
    dp = [0] * (n + 2)
    for d in range(1, n + 1):
        yd = yAt[d]
        # Note: the cell0 region for chain start at d: x < d, y > yd
        dp[d] = 1 if valid(0, d, yd, n + 1) else 0

    # process in increasing x
    for d in range(1, n + 1):
        yd = yAt[d]
        acc = dp[d]
        for c in range(1, d):
            yc = yAt[c]
            if yc > yd and dp[c]:
                if valid(c, d, yd, yc):
                    acc += dp[c]
        dp[d] = acc % MOD

    for c in range(1, n + 1):
        if dp[c] and valid(c, n + 1, 0, yAt[c]):
            ans += dp[c]
    print(ans % MOD)


main()
