import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]
    q = sum(1 for v in b if v == -1)
    total = pow(m, q, MOD)
    if n == 1:
        print(total)
        return
    # Components are contiguous blocks; boundary after k is a cut iff
    # min(prefix) > max(suffix). f = 1 + number of cuts.
    # Count over fills: sum_y (#suffix with max == y) * (#prefix with min >= y+1).
    # H[k][y] = #suffix fills (positions k..n-1, 0-indexed) with all values <= y, y in 0..m
    # G[k][x] = #prefix fills (positions 0..k-1) with all values >= x, x in 1..m+1
    ys = list(range(m + 1))
    H = [None] * (n + 1)
    ok = [1] * (m + 1)   # ok[y]: fixed values in suffix all <= y
    cur = [1] * (m + 1)  # y^(#(-1) in suffix)
    for k in range(n - 1, -1, -1):
        v = b[k]
        if v == -1:
            cur = [c * y % MOD for c, y in zip(cur, ys)]
        else:
            ok = [o if y >= v else 0 for o, y in zip(ok, ys)]
        H[k] = [o * c % MOD for o, c in zip(ok, cur)]
    # prefix side: G over x = 1..m+1, stored indexed by x (index 0..m+1)
    xs = list(range(m + 2))
    okp = [1] * (m + 2)   # okp[x]: fixed values in prefix all >= x
    curp = [1] * (m + 2)  # (m-x+1)^(#(-1) in prefix)
    base = [(m + 1 - x) if x >= 1 else 0 for x in xs]
    base = [max(0, t) for t in base]
    ans = total
    for k in range(1, n):
        # prefix = positions 0..k-1 ; suffix = k..n-1
        v = b[k - 1]
        if v == -1:
            curp = [c * t % MOD for c, t in zip(curp, base)]
        else:
            okp = [o if x <= v else 0 for o, x in zip(okp, xs)]
        G = [o * c % MOD for o, c in zip(okp, curp)]
        Hk = H[k]
        s = 0
        # sum over y in 0..m of (H[y]-H[y-1]) * G[y+1]
        prev = 0
        for y in range(m + 1):
            h = Hk[y]
            s += (h - prev) * G[y + 1]
            prev = h
        ans = (ans + s) % MOD
    print(ans % MOD)

main()
