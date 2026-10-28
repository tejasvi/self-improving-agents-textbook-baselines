import sys
from math import isqrt

MOD = 998244353


def main():
    N, M = map(int, sys.stdin.read().split())
    r = isqrt(N)

    # weights w(e) = C(e+M-1, M-1) mod MOD for e = 0..70
    maxe = 70
    w = [1] * (maxe + 1)
    for e in range(1, maxe + 1):
        w[e] = w[e - 1] * ((M - 1 + e) % MOD) % MOD * pow(e, MOD - 2, MOD) % MOD

    # ---- Lucy sieve: pi_all(v) and chi-sum(v) over primes <= v ----
    # chi(n) = 1 if n%3==1, -1 if n%3==2, 0 if n%3==0
    def chi_prefix_minus1(v):
        # sum_{2<=n<=v} chi(n)
        return (1 if v % 3 == 1 else 0) - 1

    cs_small = [0] * (r + 1)
    cs_large = [0] * (r + 1)
    ct_small = [0] * (r + 1)
    ct_large = [0] * (r + 1)
    for v in range(1, r + 1):
        ct_small[v] = v - 1
        cs_small[v] = chi_prefix_minus1(v)
    for i in range(1, r + 1):
        v = N // i
        ct_large[i] = v - 1
        cs_large[i] = chi_prefix_minus1(v)
    ct_small[0] = cs_small[0] = 0

    for p in range(2, r + 1):
        if ct_small[p] == ct_small[p - 1]:
            continue
        cp = ct_small[p - 1]
        sp = cs_small[p - 1]
        chp = 1 if p % 3 == 1 else (-1 if p % 3 == 2 else 0)
        p2 = p * p
        lim = min(r, N // p2)
        for i in range(1, lim + 1):
            d = i * p
            if d <= r:
                vc = ct_large[d]
                vs = cs_large[d]
            else:
                q = N // d
                vc = ct_small[q]
                vs = cs_small[q]
            ct_large[i] -= vc - cp
            if chp:
                cs_large[i] -= chp * (vs - sp)
        for v in range(r, p2 - 1, -1):
            q = v // p
            ct_small[v] -= ct_small[q] - cp
            if chp:
                cs_small[v] -= chp * (cs_small[q] - sp)

    def get_pi(x):
        if x <= r:
            return ct_small[x]
        return ct_large[N // x]

    def get_chi(x):
        if x <= r:
            return cs_small[x]
        return cs_large[N // x]

    # primes up to r
    sieve = bytearray([1]) * (r + 1)
    primes = []
    for i in range(2, r + 1):
        if sieve[i]:
            primes.append(i)
            for j in range(i * i, r + 1, i):
                sieve[j] = 0
    K = len(primes)

    # prefix prime weights for f and g over primes[0..j-1]
    PF = [0] * (K + 1)
    PG = [0] * (K + 1)
    for j, p in enumerate(primes):
        PF[j + 1] = (PF[j] + M) % MOD
        PG[j + 1] = (PG[j] + (M if p % 3 != 2 else 0)) % MOD

    def prime_sums(x):
        # returns (sum over primes <= x of f(p), sum over primes <= x of g(p))
        pa = get_pi(x)
        ch = get_chi(x)
        ge3 = 1 if x >= 3 else 0
        pi1 = (pa - ge3 + ch) // 2
        sf = M * pa % MOD
        sg = M * (pi1 + ge3) % MOD
        return sf, sg

    # class: 0 for p=3, 1 for p%3==1, 2 for p%3==2
    def hf(e):
        return w[e]

    def hg(cls, e):
        if cls == 0:
            return w[e]
        if cls == 1:
            return w[e] if e % 3 != 2 else 0
        return w[e] if e % 2 == 0 else 0

    cls_of = [0] * K
    for idx, p in enumerate(primes):
        cls_of[idx] = 0 if p == 3 else (1 if p % 3 == 1 else 2)

    sys.setrecursionlimit(10000)

    def S(x, j):
        # sum over n in [2, x] with lpf(n) >= primes[j] of (f(n), g(n))
        if j < K:
            if x < primes[j]:
                return 0, 0
        pf, pg = prime_sums(x)
        rf = (pf - PF[j]) % MOD
        rg = (pg - PG[j]) % MOD
        i = j
        while i < K and primes[i] * primes[i] <= x:
            p = primes[i]
            cls = cls_of[i]
            pe = p
            e = 1
            while pe * p <= x:
                y = x // pe
                lo = primes[i + 1] if i + 1 < K else r + 1
                if y >= lo:
                    sf, sg = S(y, i + 1)
                else:
                    sf, sg = 0, 0
                rf += w[e] * sf + w[e + 1]
                rg += hg(cls, e) * sg + hg(cls, e + 1)
                rf %= MOD
                rg %= MOD
                pe *= p
                e += 1
            i += 1
        return rf % MOD, rg % MOD

    sf, sg = S(N, 0)
    print((sf - sg) % MOD)


main()
