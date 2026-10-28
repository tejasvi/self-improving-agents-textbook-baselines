import sys
from operator import itemgetter, add, mul
from itertools import repeat
from collections import deque

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    M = max(A)

    # Euler phi via sieve
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if phi[p] == p:
            for k in range(p, M + 1, p):
                phi[k] -= phi[k] // p

    # divisors of all values up to M
    divs = [[] for _ in range(M + 1)]
    for d in range(1, M + 1):
        for k in range(d, M + 1, d):
            divs[k].append(d)

    try:
        from math import sumprod
    except ImportError:  # pragma: no cover
        def sumprod(x, y):
            return sum(map(mul, x, y))

    # per distinct value: (divisor tuple, phi-of-divisor tuple, getter)
    info = {}
    S = [0] * (M + 1)

    out = []
    ans = 0
    w = 1  # 2^{i-1}
    for a in A:
        ent = info.get(a)
        if ent is None:
            dt = tuple(divs[a])
            pt = tuple(phi[d] for d in dt)
            if len(dt) == 1:
                d0 = dt[0]
                getter = lambda S, d0=d0: (S[d0],)
            else:
                getter = itemgetter(*dt)
            ent = (dt, pt, getter)
            info[a] = ent
        dt, pt, getter = ent
        vals = getter(S)
        T = sumprod(pt, vals) % MOD
        ans = (2 * ans + T) % MOD
        out.append(ans)
        # update S[d] += w for d | a
        newv = map(add, vals, repeat(w))
        deque(map(S.__setitem__, dt, newv), maxlen=0)
        w = w * 2 % MOD

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
