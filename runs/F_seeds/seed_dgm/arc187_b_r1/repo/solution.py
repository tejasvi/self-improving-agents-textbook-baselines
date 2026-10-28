import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]
    q = sum(1 for x in b if x == -1)
    ans = pow(m, q, MOD)
    if n < 2:
        print(ans % MOD)
        return

    # suffix products: LE[k][t] for suffix positions k+1..n (0-indexed: i>=k)
    # LE_suf[k][t] = #ways suffix from index k (0-indexed) has all values <= t, t in 0..m
    suf = [None] * (n + 1)
    cur = [1] * (m + 1)  # empty suffix: all ways = 1 for any t
    suf[n] = cur
    for i in range(n - 1, 0, -1):
        x = b[i]
        if x == -1:
            new = [cur[t] * t % MOD for t in range(m + 1)]
        else:
            new = [cur[t] if x <= t else 0 for t in range(m + 1)]
            # value t>=x allowed only
        cur = new
        suf[i] = cur

    # prefix: pre_ge[t] for t in 1..m+1, prefix indices 0..k-1
    pre = [1] * (m + 2)  # empty prefix: index t in 1..m+1
    for k in range(1, n):
        i = k - 1
        x = b[i]
        if x == -1:
            # ways for position with value >= t : m - t + 1
            pre = [pre[t] * (m - t + 1) % MOD if t <= m else 0 for t in range(m + 2)]
        else:
            pre = [pre[t] if (t <= x) else 0 for t in range(m + 2)]
            # value x must be >= t  <=> t <= x
        # exact min distribution of prefix of length k
        # Epre(v) = GE(v) - GE(v+1), GE(v) = pre[v] for v in 1..m, GE(m+1)=0
        ge = pre[:]
        ge[m + 1] = 0
        # SP[w+1] = sum_{v>w} Epre(v) = GE(w+1) (telescoping)
        # so contribution = sum_w Esuf(w) * GE(w+1)
        s = suf[k]  # suffix indices k..n-1, LE[t] for t in 0..m
        total = 0
        for w in range(1, m + 1):
            esuf = (s[w] - s[w - 1]) % MOD
            if esuf:
                total += esuf * ge[w + 1]
        ans = (ans + total) % MOD
    print(ans % MOD)


main()
