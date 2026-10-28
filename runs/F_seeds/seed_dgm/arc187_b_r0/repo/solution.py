import sys
from array import array

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

    # xs for prefix: G[x] = #ways prefix all >= x, x in 0..m+1
    # Forward pass: store G_k for k = 1..n-1 (prefix of length k).
    xs = range(0, m + 2)
    G = [1] * (m + 2)
    Gs = [None] * n
    for k in range(1, n):
        bk = b[k - 1]
        if bk == -1:
            G = [(g * (m - x + 1)) % MOD if x >= 1 else g for x, g in zip(xs, G)]
        else:
            G = [g if x <= bk else 0 for x, g in zip(xs, G)]
        Gs[k] = array('q', G)

    # Backward pass: H = #ways suffix (positions k+1..n) all <= y, y in 0..m
    ys = range(0, m + 1)
    H = [1] * (m + 1)
    for k in range(n - 1, 0, -1):
        # add position k+1 into the suffix
        bj = b[k]  # position k+1 (1-indexed) -> b[k]
        if bj == -1:
            H = [(h * y) % MOD for y, h in zip(ys, H)]
        else:
            H = [h if y >= bj else 0 for y, h in zip(ys, H)]
        Gk = Gs[k]
        # sum over x in 1..m of (G(x)-G(x+1)) * H(x-1)
        s = 0
        for x in range(1, m + 1):
            s += (Gk[x] - Gk[x + 1]) * H[x - 1]
        ans = (ans + s) % MOD
    print(ans % MOD)


main()
