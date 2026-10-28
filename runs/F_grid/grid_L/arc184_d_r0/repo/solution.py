import sys

MOD = 998244353


def region_ok(vals):
    # vals: Y values of a region, listed in increasing X order.
    # Every point must be comparable (same direction) with another point of the region,
    # i.e. have a larger-X/larger-Y or smaller-X/smaller-Y partner inside the region.
    m = len(vals)
    if m == 0:
        return True
    if m == 1:
        return False
    suf_max = [-1] * (m + 1)
    for i in range(m - 1, -1, -1):
        suf_max[i] = max(suf_max[i + 1], vals[i])
    pre_min = 1 << 30
    for i in range(m):
        v = vals[i]
        if suf_max[i + 1] < v and pre_min > v:
            return False
        pre_min = min(pre_min, v)
    return True


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    Yx = [0] * n  # Yx[x] = y-coordinate of the ball with X = x (0-indexed)
    for i in range(n):
        x = int(data[1 + 2 * i]) - 1
        y = int(data[2 + 2 * i]) - 1
        Yx[x] = y

    # valid_start[c]: NW region of c is fine (c is the first chain element)
    # valid_end[c]: SE region of c is fine (c is the last chain element)
    valid_start = [False] * n
    valid_end = [False] * n
    for c in range(n):
        yc = Yx[c]
        nw = [Yx[t] for t in range(c) if Yx[t] > yc]
        se = [Yx[t] for t in range(c + 1, n) if Yx[t] < yc]
        valid_start[c] = region_ok(nw)
        valid_end[c] = region_ok(se)

    dp = [0] * n
    for b in range(n):
        yb = Yx[b]
        total = 1 if valid_start[b] else 0
        for a in range(b):
            ya = Yx[a]
            if ya <= yb or dp[a] == 0:
                continue
            vals = [Yx[t] for t in range(a + 1, b) if yb < Yx[t] < ya]
            if region_ok(vals):
                total += dp[a]
        dp[b] = total % MOD

    ans = 0
    for c in range(n):
        if valid_end[c]:
            ans += dp[c]
    ans %= MOD

    # The full set is reachable with zero operations. It is also the image of
    # some chain iff some ball is anti-comparable to all others.
    full_in_image = False
    for c in range(n):
        yc = Yx[c]
        if all((Yx[t] - yc) * (t - c) < 0 for t in range(n) if t != c):
            full_in_image = True
            break
    if not full_in_image:
        ans = (ans + 1) % MOD

    print(ans)


main()
