import sys
from itertools import product


def main():
    N = int(sys.stdin.read().split()[0])

    # Divisors of N
    def factorize(n):
        f = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                f[d] = f.get(d, 0) + 1
                n //= d
            d += 1 if d == 2 else 2
        if n > 1:
            f[n] = f.get(n, 0) + 1
        return f

    fac = factorize(N)
    divs = [1]
    for p, e in fac.items():
        nd = []
        for d in divs:
            x = d
            for _ in range(e + 1):
                nd.append(x)
                x *= p
        divs = nd
    divs.sort()

    # Pair values: a * rev(a) dividing N, keep shortest a per value
    pair_best = {}  # value -> a string
    for L in range(1, 7):
        for tup in product('123456789', repeat=L):
            s = ''.join(tup)
            a = int(s)
            v = a * int(s[::-1])
            if N % v == 0:
                cur = pair_best.get(v)
                if cur is None or len(s) < len(cur):
                    pair_best[v] = s
    pairs = sorted(pair_best.items())

    INF = float('inf')
    idx = {d: i for i, d in enumerate(divs)}
    # cost of pair = 2*len(a) + 2 (two runs plus two stars)
    dp = [INF] * len(divs)
    back = [None] * len(divs)  # (prev index, pair value)
    dp[idx[1]] = 0
    for v, s in pairs:
        c = 2 * len(s) + 2
        for i, d in enumerate(divs):
            if d % v == 0:
                j = idx[d // v]
                if dp[j] + c < dp[i]:
                    dp[i] = dp[j] + c
                    back[i] = (j, v)

    # Middle palindromic divisors (digits 1-9)
    best = None  # (total cost, middle string or None, index of rest)
    for d in divs:
        s = str(d)
        if '0' in s or s != s[::-1]:
            continue
        rest = N // d
        j = idx[rest]
        if dp[j] == INF:
            continue
        cost = dp[j] + len(s) + (1 if rest != 1 or dp[j] > 0 else 0)
        if best is None or cost < best[0]:
            best = (cost, s, j)

    if best is None:
        print(-1)
        return

    _, mid, j = best
    left = []
    cur = j
    while divs[cur] != 1:
        prev, v = back[cur]
        left.append(pair_best[v])
        cur = prev
    # left holds runs for pairs (any order is fine)
    runs = left + [mid] + [s[::-1] for s in reversed(left)]
    print('*'.join(runs))


main()
