import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]
    MOD = 998244353
    q = sum(1 for x in b if x == -1)

    # H_suf[k] (k=1..n-1): ways suffix k+1..n all <= v, for v in 0..m
    H_suf = [None] * (n + 1)
    cur = [1] * (m + 1)  # empty suffix: all <= v is 1 for every v
    for k in range(n - 1, 0, -1):
        x = b[k]  # element at 1-based index k+1 is b[k] (0-based)
        if x == -1:
            cur = [cur[v] * v % MOD for v in range(m + 1)]
        else:
            cur = [cur[v] if x <= v else 0 for v in range(m + 1)]
        H_suf[k] = cur

    ans = pow(m, q, MOD)
    # G[v] for v in 1..m+1: ways prefix 1..k all >= v
    G = [1] * (m + 2)
    G[0] = 0
    for k in range(1, n):
        x = b[k - 1]
        if x == -1:
            G = [G[v] * (m - v + 1) % MOD if 1 <= v <= m + 1 else G[v] for v in range(m + 2)]
        else:
            G = [G[v] if (v <= x) else 0 for v in range(m + 2)]
            # v in 0..m+1; for v<=x factor is 1 (x>=v), else 0
        H = H_suf[k]
        total = 0
        for y in range(1, m + 1):
            total += (H[y] - H[y - 1]) * G[y + 1]
        ans = (ans + total) % MOD
    print(ans % MOD)

main()
