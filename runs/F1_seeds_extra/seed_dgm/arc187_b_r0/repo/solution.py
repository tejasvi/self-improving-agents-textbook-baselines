import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]
    q = sum(1 for x in b if x == -1)

    # S_suf[k][x] = #fillings of positions k..n-1 (0-indexed) with all values <= x, x in 0..m
    # Suffix arrays computed from the right; we store only what is needed.
    suf = [None] * (n + 1)
    cur = [1] * (m + 1)
    cur[0] = 0  # nonempty suffix cannot have all values <= 0
    suf[n] = None
    for k in range(n - 1, -1, -1):
        bk = b[k]
        new = [0] * (m + 1)
        if bk == -1:
            for x in range(m + 1):
                new[x] = cur[x] * (x) % MOD
        else:
            for x in range(bk, m + 1):
                new[x] = cur[x]
        # new[x] for suffix starting at k: element k <= x
        # cur was for suffix k+1; if suffix k+1 empty, cur should be all ones (handled by init)
        suf[k] = new
        cur = new

    total = pow(m, q, MOD)
    # prefix: P(v) = #fillings of positions 0..k-1 with all values >= v, v in 1..m+1
    P = [1] * (m + 2)  # empty prefix: all ones (for v in 1..m+1)
    P[0] = 0
    ans = total  # the +1 per fillings
    for k in range(1, n):  # prefix = positions 0..k-1, suffix = k..n-1
        bk = b[k - 1]
        newP = [0] * (m + 2)
        if bk == -1:
            for v in range(1, m + 2):
                newP[v] = P[v] * (m - v + 1) % MOD
        else:
            for v in range(1, bk + 1):
                newP[v] = P[v]
        P = newP
        S = suf[k]
        s = 0
        for v in range(1, m + 1):
            e = (P[v] - P[v + 1]) % MOD
            if e:
                s += e * S[v - 1]
        ans = (ans + s) % MOD
    print(ans % MOD)

main()
