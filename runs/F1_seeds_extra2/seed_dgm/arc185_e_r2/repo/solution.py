import sys
from operator import mul


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    MOD = 998244353
    M = max(A) if A else 1

    # smallest prime factor and phi
    spf = list(range(M + 1))
    i = 2
    while i * i <= M:
        if spf[i] == i:
            for j in range(i * i, M + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if spf[p] == p:
            for j in range(p, M + 1, p):
                phi[j] -= phi[j] // p

    cache = {}

    def divs_phis(v):
        r = cache.get(v)
        if r is not None:
            return r
        # factorize
        fac = []
        x = v
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            fac.append((p, e))
        ds = [1]
        for p, e in fac:
            new = []
            for d in ds:
                m = d
                for _ in range(e + 1):
                    new.append(m)
                    m *= p
            ds = new
        ps = [phi[d] for d in ds]
        r = (ds, ps)
        cache[v] = r
        return r

    W = [0] * (M + 1)
    out = []
    ans = 0
    pw = 1  # 2^{j-1}
    for j in range(n):
        a = A[j]
        ds, ps = divs_phis(a)
        s = sum(map(mul, ps, map(W.__getitem__, ds))) % MOD
        ans = (2 * ans + s) % MOD
        out.append(ans)
        for d in ds:
            W[d] += pw
        pw = pw * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
