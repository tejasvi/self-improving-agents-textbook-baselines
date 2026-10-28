import sys

def main():
    data = sys.stdin.read().split()
    MOD = 998244353
    n, m = int(data[0]), int(data[1])
    B = [int(x) for x in data[2:2 + n]]
    q = B.count(-1)
    # Prefix/suffix "all >= v" / "all <= w" counts.
    # pre[k][v] for v in 1..m+1: #fillings of B[0:k] with all values >= v
    # suf[k][w] for w in 0..m: #fillings of B[k:] with all values <= w
    total = pow(m, q, MOD)
    ans = total  # cut after position N (always a boundary)

    # Build suffix-of-values arrays incrementally, from the right.
    # suf_le[w] for current suffix starting at index k (w = 0..m)
    suf_le = [1] * (m + 1)  # empty suffix: all <= w -> 1 for every w (incl. w=0)
    # Precompute prefix arrays for each k in 1..n-1 as needed
    # We iterate k from n-1 down to 1, updating suffix B[k:], and prefix needs ge arrays.
    # Compute prefix arrays via forward pass storing them (n*m memory ~ 4e6 ints ok).
    pre_ge = []
    cur = [1] * (m + 2)  # empty prefix: all >= v -> 1
    pre_ge.append(cur)
    for i in range(n):
        b = B[i]
        new = [0] * (m + 2)
        if b == -1:
            for v in range(1, m + 2):
                new[v] = cur[v] * (m - v + 1) % MOD
        else:
            for v in range(1, m + 2):
                new[v] = cur[v] if b >= v else 0
        cur = new
        pre_ge.append(cur)
    # pre_ge[k] is prefix of length k
    for k in range(n - 1, 0, -1):
        # update suffix to B[k:]
        b = B[k]
        new = [0] * (m + 1)
        if b == -1:
            for w in range(m + 1):
                new[w] = suf_le[w] * w % MOD
        else:
            for w in range(m + 1):
                new[w] = suf_le[w] if b <= w else 0
        suf_le = new
        # exact max = w: E_suf[w] = suf_le[w] - suf_le[w-1] (w>=1); suf_le[0] for w=0 is empty-value case
        E_suf = [0] * (m + 1)
        for w in range(1, m + 1):
            E_suf[w] = (suf_le[w] - suf_le[w - 1]) % MOD
        pg = pre_ge[k]
        # E_pre[v] = pg[v] - pg[v+1], v in 1..m
        # sum over v > w of E_pre[v]*E_suf[w]
        # Iterate v from 1..m, maintain prefix sum of E_suf[w] for w < v
        acc = 0
        s = 0
        for v in range(1, m + 1):
            # add E_suf[v-1] to s when v-1 >= 1
            if v - 1 >= 1:
                s += E_suf[v - 1]
            e_pre = (pg[v] - pg[v + 1]) % MOD
            acc = (acc + e_pre * s) % MOD
        ans = (ans + acc) % MOD
    print(ans % MOD)

main()
