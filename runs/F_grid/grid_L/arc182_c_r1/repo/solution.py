import sys

MOD = 998244353
PRIMES = [2, 3, 5, 7, 11, 13]
NP = len(PRIMES)
FULL = 1 << NP


def mul(a, b):
    # a, b: lists of length FULL indexed by bitmask; t_S * t_T = t_{S|T} if disjoint else 0
    res = [0] * FULL
    for i in range(FULL):
        ai = a[i]
        if ai == 0:
            continue
        for j in range(FULL):
            if i & j:
                continue
            bj = b[j]
            if bj:
                res[i | j] = (res[i | j] + ai * bj) % MOD
    return res


def add(a, b):
    return [(x + y) % MOD for x, y in zip(a, b)]


def exponent(v, p):
    c = 0
    while v % p == 0:
        v //= p
        c += 1
    return c


def main():
    N, M = map(int, sys.stdin.read().split())
    # B = sum_{v=1}^{M} g_v, g_v = prod_p (1 + v_p t_p)
    B = [0] * FULL
    for v in range(1, M + 1):
        g = [0] * FULL
        g[0] = 1
        for idx, p in enumerate(PRIMES):
            e = exponent(v, p)
            if e:
                # multiply g by (1 + e t_idx)
                bit = 1 << idx
                new = g[:]
                for m in range(FULL):
                    if g[m] and not (m & bit):
                        new[m | bit] = (new[m | bit] + e * g[m]) % MOD
                g = new
        B = add(B, g)

    one = [0] * FULL
    one[0] = 1
    # Process bits of N from most significant: maintain S = sum_{k=1}^n B^k, P = B^n
    S = [0] * FULL
    P = one[:]
    n = 0
    for bit in bin(N)[2:]:
        # n -> 2n
        if n > 0:
            S = add(S, mul(P, S))
            P = mul(P, P)
        n *= 2
        if bit == '1':
            P = mul(P, B)
            S = add(S, P)
            n += 1
    print(sum(S) % MOD)


main()
