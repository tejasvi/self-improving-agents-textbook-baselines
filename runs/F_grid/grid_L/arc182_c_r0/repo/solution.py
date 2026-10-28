import sys

MOD = 998244353
PRIMES = [2, 3, 5, 7, 11, 13]
K = len(PRIMES)
D = 1 << K


def mul(a, b):
    # multiplication in Z_MOD[u_1..u_K] / (u_i^2)
    c = [0] * D
    for i in range(D):
        ai = a[i]
        if ai == 0:
            continue
        for j in range(D):
            if (i & j) == 0 and b[j]:
                c[i | j] = (c[i | j] + ai * b[j]) % MOD
    return c


def add(a, b):
    return [(x + y) % MOD for x, y in zip(a, b)]


def geo(A, n):
    """Return (A^n, sum_{k=1}^n A^k)."""
    if n == 0:
        one = [0] * D
        one[0] = 1
        return one, [0] * D
    if n % 2 == 0:
        p, s = geo(A, n // 2)
        # S_n = S_{n/2} + A^{n/2} * S_{n/2}
        return mul(p, p), add(s, mul(p, s))
    p, s = geo(A, n - 1)
    pn = mul(p, A)
    return pn, add(s, pn)


def main():
    N, M = map(int, sys.stdin.read().split())
    # Element m contributes prod_p t_p^{v_p} with t_p = 1 + u_p, u_p^2 = 0,
    # so t_p^{v} = 1 + v*u_p.
    S = [0] * D
    for m in range(1, M + 1):
        x = m
        elem = [0] * D
        elem[0] = 1
        for idx, p in enumerate(PRIMES):
            v = 0
            while x % p == 0:
                x //= p
                v += 1
            if v:
                f = [0] * D
                f[0] = 1
                f[1 << idx] = v
                elem = mul(elem, f)
        S = add(S, elem)
    # Score = prod_p (e_p + 1) = coefficient of u_1...u_K in prod_p t_p^{e_p+1}
    P = [0] * D
    P[0] = 1
    for idx in range(K):
        f = [0] * D
        f[0] = 1
        f[1 << idx] = 1
        P = mul(P, f)
    _, G = geo(S, N)
    R = mul(P, G)
    print(R[D - 1] % MOD)


main()
