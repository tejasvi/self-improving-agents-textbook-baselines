import sys
from array import array
from operator import mul

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    B = [int(x) for x in data[2:2 + n]]
    q = sum(1 for x in B if x == -1)
    ans = pow(m, q, MOD)
    if n < 2:
        print(ans % MOD)
        return

    # Suffix count arrays: S_k[u] = #ways suffix k..n-1 has all values <= u, u = 0..m
    # Stored for k = 1..n-1 as array('q').
    S_store = [None] * n
    S = [1] * (m + 1)
    for i in range(n - 1, 0, -1):
        x = B[i]
        if x == -1:
            S = [s * u % MOD for u, s in enumerate(S)]
        else:
            S[:x] = [0] * x  # need u >= x
        S_store[i] = array('q', S)

    # Prefix count arrays: P[i] = #ways prefix 0..k-1 has all values >= v, v = i+1 (index i = v-1)
    P = [1] * m
    base = [m - i for i in range(m)]  # M - v + 1 with v = i+1
    for k in range(1, n):
        x = B[k - 1]
        if x == -1:
            P = [p * b % MOD for p, b in zip(P, base)]
        else:
            # need v <= x, i.e. index i <= x-1 ; zero indices >= x
            P[x:] = [0] * (m - x)
        Sk = S_store[k]
        # cnt = sum_v (P(v) - P(v+1)) * S(v-1), v = i+1 -> S index i
        Sl = Sk[:m]
        t1 = sum(map(mul, P, Sl))
        t2 = sum(map(mul, P[1:], Sl[:m - 1]))  # P(v+1) for v=i+1, i in 0..m-2
        ans = (ans + t1 - t2) % MOD
    print(ans % MOD)

main()
