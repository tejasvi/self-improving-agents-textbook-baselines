import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]
    q = sum(1 for x in b if x == -1)

    # f = number of positions k (1..n) with min(prefix[1..k]) > max(suffix[k+1..n]).
    # k = n always qualifies -> contributes m^q total over all fillings.
    # For 1 <= k < n: sum over a of
    #   (#prefix fillings with min exactly a) * (#suffix fillings with max <= a-1).

    # suf_le[k][t] = #fillings of b[k..n-1] with all values <= t, t in 0..m
    suf_le = [None] * (n + 1)
    cur = [1] * (m + 1)
    suf_le[n] = cur
    for i in range(n - 1, 0, -1):
        x = b[i]
        if x == -1:
            cur = [cur[t] * t % MOD for t in range(m + 1)]
        else:
            cur = [cur[t] if t >= x else 0 for t in range(m + 1)]
        suf_le[i] = cur

    # gp[a] = #fillings of prefix b[0..k-1] with all values >= a, a in 1..m+1
    gp = [1] * (m + 2)
    total = pow(m, q, MOD)
    for k in range(1, n):
        x = b[k - 1]
        if x == -1:
            gp = [gp[a] * (m - a + 1) % MOD if a <= m else 0 for a in range(m + 2)]
        else:
            gp = [gp[a] if (a <= x) else 0 for a in range(m + 2)]
        sl = suf_le[k]
        s = 0
        for a in range(1, m + 1):
            ex = (gp[a] - gp[a + 1]) % MOD
            if ex:
                s += ex * sl[a - 1]
        total = (total + s) % MOD

    print(total % MOD)


main()
