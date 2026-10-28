import sys
from operator import itemgetter


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    MOD = 998244353
    M = max(max(A), 2)

    # Euler phi
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if phi[p] == p:  # p is prime
            for k in range(p, M + 1, p):
                phi[k] -= phi[k] // p

    # Divisors lists computed lazily per distinct value, with phi folded in.
    # For value a: ds[a] = tuple of divisors d of a; ph[a] = tuple of phi(d).
    cache = {}

    W = [0] * (M + 1)
    out = []
    ans = 0
    w = 1  # 2^{m-1} mod MOD for 0-indexed m
    for a in A:
        entry = cache.get(a)
        if entry is None:
            # build divisors via trial division up to sqrt
            small = []
            large = []
            i = 1
            while i * i <= a:
                if a % i == 0:
                    small.append(i)
                    if i * i != a:
                        large.append(a // i)
                i += 1
            ds = small + large[::-1]
            getter = itemgetter(*ds)
            phs = [phi[d] for d in ds]
            entry = (ds, getter, phs)
            cache[a] = entry
        ds, getter, phs = entry
        if len(ds) == 1:
            G = phs[0] * W[ds[0]]
        else:
            G = sum(map(int.__mul__, phs, getter(W)))
        G %= MOD
        ans = (2 * ans + G) % MOD
        out.append(ans)
        for d in ds:
            W[d] = (W[d] + w) % MOD
        w = w * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
