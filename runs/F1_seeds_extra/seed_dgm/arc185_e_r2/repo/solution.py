import sys

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    M = max(A)

    # smallest prime factor sieve
    spf = list(range(M + 1))
    i = 2
    while i * i <= M:
        if spf[i] == i:
            for k in range(i * i, M + 1, i):
                if spf[k] == k:
                    spf[k] = i
        i += 1

    # Euler phi sieve
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if spf[p] == p:
            for k in range(p, M + 1, p):
                phi[k] -= phi[k] // p

    div_cache = {}

    def divisors_with_phi(v):
        # gcd(a,b) = sum_{d | a, d | b} phi(d)
        r = div_cache.get(v)
        if r is not None:
            return r
        divs = [1]
        dphi = [1]
        x = v
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            nd = []
            nph = []
            for d, f in zip(divs, dphi):
                nd.append(d)
                nph.append(f)
                pk = 1
                for k in range(1, e + 1):
                    pk *= p
                    nd.append(d * pk)
                    # phi(p^k) = p^(k-1) * (p-1)
                    nph.append(f * (pk // p) * (p - 1))
            divs = nd
            dphi = nph
        r = (divs, dphi)
        div_cache[v] = r
        return r

    # T[d] = sum over earlier i with d | A_i of 2^(i-1) mod MOD
    T = [0] * (M + 1)
    out = []
    ans = 0
    pw = 1  # 2^(j-1) mod MOD for 0-indexed j
    for j in range(n):
        v = A[j]
        divs, dphi = divisors_with_phi(v)
        s = 0
        for d, f in zip(divs, dphi):
            t = T[d]
            if t:
                s += f * t
        S = s % MOD
        ans = (2 * ans + S) % MOD
        out.append(ans)
        for d in divs:
            T[d] = (T[d] + pw) % MOD
        pw = pw * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
