import sys
from math import isqrt

MOD = 998244353


def main():
    N, M = map(int, sys.stdin.read().split())
    r = isqrt(N)

    def chi_sum(v):  # sum_{2<=i<=v} chi(i), chi(i) = 1 if i%3==1, -1 if i%3==2, 0 otherwise
        if v < 2:
            return 0
        return (1 if v % 3 == 1 else 0) - 1

    # Lucy DP: g0(v) = #primes <= v, g1(v) = sum_{p<=v} chi(p)
    # hi[i] <-> v = N//i (i in 1..r); lo[v] <-> v (v in 0..r)
    hi0 = [0] * (r + 1)
    hi1 = [0] * (r + 1)
    lo0 = [0] * (r + 1)
    lo1 = [0] * (r + 1)
    for i in range(1, r + 1):
        v = N // i
        hi0[i] = v - 1
        hi1[i] = chi_sum(v)
    for v in range(0, r + 1):
        lo0[v] = max(v - 1, 0)
        lo1[v] = chi_sum(v)

    sieve = bytearray([1]) * (r + 1)
    primes = []
    for p in range(2, r + 1):
        if sieve[p]:
            primes.append(p)
            for q in range(p * p, r + 1, p):
                sieve[q] = 0

    for p in primes:
        p2 = p * p
        pc = lo0[p - 1]
        sc = lo1[p - 1]
        c = 1 if p % 3 == 1 else (-1 if p % 3 == 2 else 0)
        lim = min(r, N // p2)
        for i in range(1, lim + 1):
            ip = i * p
            if ip <= r:
                a0 = hi0[ip]
                a1 = hi1[ip]
            else:
                w = N // ip
                a0 = lo0[w]
                a1 = lo1[w]
            hi0[i] -= a0 - pc
            if c:
                hi1[i] -= c * (a1 - sc)
        for v in range(r, p2 - 1, -1):
            w = v // p
            lo0[v] -= lo0[w] - pc
            if c:
                lo1[v] -= c * (lo1[w] - sc)

    # Prime counts for the "bad" mode: primes p with h(p)=M are p=3 and p≡1 (mod 3).
    # #allowed(<=v) = (#primes≡1 + #primes≡2 ... ) -> A = (pi_no3 + S_chi)/2 + [v>=3]
    def cb_from(g0, g1, v):
        if v < 2:
            return 0
        pi_no3 = g0 - (1 if v >= 3 else 0)
        A = (pi_no3 + g1) // 2
        return A + (1 if v >= 3 else 0)

    CT_lo = lo0
    CT_hi = hi0
    CB_lo = [cb_from(lo0[v], lo1[v], v) for v in range(r + 1)]
    CB_hi = [0] * (r + 1)
    for i in range(1, r + 1):
        CB_hi[i] = cb_from(hi0[i], hi1[i], N // i)

    # g[e] = C(e+M-1, e) mod MOD
    gmax = 80
    g = [1] * (gmax + 1)
    for e in range(1, gmax + 1):
        g[e] = g[e - 1] * ((M - 1 + e) % MOD) % MOD * pow(e, MOD - 2, MOD) % MOD

    np_ = len(primes)

    def run(mode):
        if mode == 0:
            Clo, Chi = CT_lo, CT_hi
        else:
            Clo, Chi = CB_lo, CB_hi

        def C(x):
            if x <= r:
                return Clo[x]
            return Chi[N // x]

        def allowed(p, e):
            if mode == 0:
                return True
            if p == 3:
                return True
            if p % 3 == 1:
                return e % 3 != 2
            return e % 2 == 0

        # S(x, j): sum of h(n) over 2<=n<=x with lpf(n) >= primes[j]
        # base = C(primes[j]-1) = number of (allowed) primes below primes[j]
        def S(x, j, base):
            res = M * (C(x) - base) % MOD
            for k in range(j, np_):
                p = primes[k]
                if p * p > x:
                    break
                pe = p
                e = 1
                nxt_base = C(p)
                while pe * p <= x:
                    if allowed(p, e):
                        res += g[e] * S(x // pe, k + 1, nxt_base)
                    if allowed(p, e + 1):
                        res += g[e + 1]
                    pe *= p
                    e += 1
                res %= MOD
            return res % MOD

        return S(N, 0, 0)

    total = run(0)
    bad = run(1)
    print((total - bad) % MOD)


main()
