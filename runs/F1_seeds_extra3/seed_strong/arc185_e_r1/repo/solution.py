import sys
from operator import itemgetter, mul, add
from itertools import repeat
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    MOD = 998244353
    V = max(A)

    # Euler phi sieve
    phi = list(range(V + 1))
    for p in range(2, V + 1):
        if phi[p] == p:  # p is prime
            for m in range(p, V + 1, p):
                phi[m] -= phi[m] // p

    # Divisor lists, only for values that occur in A
    present = [False] * (V + 1)
    for a in A:
        present[a] = True
    divs = [None] * (V + 1)
    for v in range(1, V + 1):
        if present[v]:
            divs[v] = []
    for d in range(1, V + 1):
        for m in range(d, V + 1, d):
            if present[m]:
                divs[m].append(d)

    # Per distinct value: (getter over T at divisors, phi of divisors, divisors)
    info = [None] * (V + 1)
    for v in range(1, V + 1):
        if present[v]:
            dv = divs[v]
            g = itemgetter(*dv) if len(dv) > 1 else (lambda T, _d=dv[0]: (T[_d],))
            info[v] = (g, [phi[d] for d in dv], dv)

    # T[d] = sum of 2^i over earlier indices i with d | A_i (unreduced ints)
    T = [0] * (V + 1)
    S = []
    push = S.append
    pw = 1
    upd = deque(maxlen=0).extend
    for v in A:
        g, ph, dv = info[v]
        old = g(T)                                   # T[d] for d | v
        push(sum(map(mul, ph, old)))                 # sum_d phi(d) T[d]
        upd(map(T.__setitem__, dv, map(add, old, repeat(pw))))  # T[d] += 2^k
        pw = pw * 2 % MOD

    out = []
    ans = 0
    for s in S:
        ans = (2 * ans + s) % MOD
        out.append(ans)
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
