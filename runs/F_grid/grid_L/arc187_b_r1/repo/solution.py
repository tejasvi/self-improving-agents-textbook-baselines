import sys
from array import array

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]
    q = sum(1 for x in b if x == -1)

    # H[k] (k=1..n-1): suffix positions k+1..n (1-indexed), array over u=0..m:
    # number of fillings where all values <= u.
    W = m + 1  # u in 0..m
    H = [None] * (n + 1)
    cur = [1] * W
    for k in range(n, 1, -1):
        # add position k (1-indexed) -> b[k-1]; suffix becomes k..n, store for cut k-1
        x = b[k - 1]
        if x == -1:
            cur = [cur[u] * u % MOD for u in range(W)]
        else:
            cur = [cur[u] if u >= x else 0 for u in range(W)]
        H[k - 1] = array('q', cur)

    # Forward: G over v=1..m+1, G[v] = #prefix fillings with all values >= v
    G = [1] * (m + 2)  # index v, v in 0..m+1
    total = pow(m, q, MOD)
    for k in range(1, n):
        x = b[k - 1]
        if x == -1:
            # factor (m - v + 1) for v in 1..m+1
            G = [G[v] * (m - v + 1) % MOD if v >= 1 else 0 for v in range(m + 2)]
        else:
            G = [G[v] if (v >= 1 and v <= x) else 0 for v in range(m + 2)]
        Hk = H[k]
        s = 0
        # exact min v in 1..m: G[v]-G[v+1]; pairs with H[v-1]
        for v in range(1, m + 1):
            e = G[v] - G[v + 1]
            if e:
                s += e * Hk[v - 1]
        total = (total + s) % MOD
    print(total % MOD)


main()
