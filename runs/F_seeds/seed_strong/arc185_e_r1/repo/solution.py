import sys
from operator import itemgetter, mul
from math import gcd
from itertools import repeat

MOD = 998244353
PEND_LIMIT = 32

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    MAX = max(A)

    # phi sieve
    phi = list(range(MAX + 1))
    for p in range(2, MAX + 1):
        if phi[p] == p:
            for q in range(p, MAX + 1, p):
                phi[q] -= phi[q] // p

    # smallest prime factor
    spf = [0] * (MAX + 1)
    for i in range(2, MAX + 1):
        if spf[i] == 0:
            for q in range(i, MAX + 1, i):
                if spf[q] == 0:
                    spf[q] = i

    cache = {}

    def info(a):
        divs = [1]
        x = a
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            new = []
            pk = 1
            for _ in range(e + 1):
                for d in divs:
                    new.append(d * pk)
                pk *= p
            divs = new
        ph = tuple(phi[d] for d in divs)
        dt = tuple(divs)
        if len(dt) > 1:
            g = itemgetter(*dt)
        else:
            d0 = dt[0]
            g = lambda C, _d=d0: (C[_d],)
        return (dt, ph, g)

    C = [0] * (MAX + 1)   # C[d] = sum of weights of flushed prior elements with d | A_i
    pend = {}             # value -> sum of weights of unflushed prior elements
    inv2 = (MOD + 1) // 2
    out = []
    S = 0
    pw2 = 1
    ipw = inv2
    for m in range(1, n + 1):
        a = A[m - 1]
        info_a = cache.get(a)
        if info_a is None:
            info_a = info(a)
            cache[a] = info_a
        dt, ph, g = info_a
        # Q = sum_{i<m} gcd(A_i, a) * 2^i
        Q = sum(map(mul, ph, g(C)))
        if pend:
            Q += sum(map(mul, map(gcd, repeat(a), pend.keys()), pend.values()))
        Q %= MOD
        pw2 = pw2 * 2 % MOD          # 2^m
        ipw = ipw * inv2 % MOD       # inv2^(m+1)
        S = (S + ipw * Q) % MOD
        out.append(S * pw2 % MOD)
        # add element m with weight 2^m
        pend[a] = pend.get(a, 0) + pw2
        if len(pend) > PEND_LIMIT:
            for v, w in pend.items():
                for d in cache[v][0] if v in cache else info(v)[0]:
                    C[d] += w
            pend = {}
    sys.stdout.write('\n'.join(map(str, out)) + '\n')

main()
