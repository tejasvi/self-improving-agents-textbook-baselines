import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    Y = [0] * (n + 2)  # Y[x] for X coordinate x in 1..n
    for i in range(n):
        x = int(data[1 + 2 * i])
        y = int(data[2 + 2 * i])
        Y[x] = y
    # sentinels: A at X=0, Y=n+1 ; B at X=n+1, Y=0
    Y[0] = n + 1
    Y[n + 1] = 0

    # adj[x]: bitmask of real points comparable to x (over X coordinates)
    adj = [0] * (n + 2)
    for x in range(1, n + 1):
        m = 0
        for z in range(1, n + 1):
            if (z - x) * (Y[z] - Y[x]) > 0:
                m |= 1 << z
        adj[x] = m

    # maskYlt[v] = bits z (real) with Y[z] < v
    maskYlt = [0] * (n + 3)
    inv = [0] * (n + 2)  # inv[y] = X coordinate with that Y
    for z in range(1, n + 1):
        inv[Y[z]] = z
    cur = 0
    for v in range(0, n + 2):
        maskYlt[v] = cur  # bits z (real) with Y[z] < v
        if 1 <= v <= n:
            cur |= 1 << inv[v]

    def valid_box(a, b):
        # points with a<x<b and Yb<Y<Ya must each have comparable partner inside
        lo = (1 << (a + 1)) - 1  # bits 0..a
        hi = (1 << b) - 1        # bits 0..b-1
        S = (hi ^ lo) & (maskYlt[Y[a]] & ~maskYlt[Y[b] + 1])
        T = S
        while T:
            low = T & -T
            x = low.bit_length() - 1
            if not (adj[x] & S):
                return False
            T ^= low
        return True

    # DP over nodes in X order: 0 = A, 1..n real, n+1 = B
    dp = [0] * (n + 2)
    dp[0] = 1
    for b in range(1, n + 2):
        s = 0
        for a in range(0, b):
            if dp[a] and Y[a] > Y[b] and valid_box(a, b):
                s += dp[a]
        dp[b] = s % MOD
    print(dp[n + 1] % MOD)


main()
