import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:n]]
    m = n - 1
    LIM = 1001
    spf = list(range(LIM))
    for i in range(2, int(LIM ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, LIM, i):
                if spf[j] == j:
                    spf[j] = i
    occ = {}  # prime -> list of (k, exponent)
    for k, a in enumerate(A):
        x = a
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            occ.setdefault(p, []).append((k, e))

    def run(p, T, pw, exps, lo):
        # exps: list of exponent per position (0 if none); returns sum over valid e in [lo,T]
        # initial: e_1 any in [lo,T]
        dp = [pw[e] if e >= lo else 0 for e in range(T + 1)]
        for k in range(m):
            a = exps[k]
            if a == 0:
                nd = dp
            else:
                P = [0] * a + dp + [0] * a
                nd = [(u + v) % MOD for u, v in zip(P, P[2 * a:])]
            nd = [u * w % MOD for u, w in zip(nd, pw)]
            if lo > 0:
                nd[0] = 0
            dp = nd
        return sum(dp) % MOD

    ans = 1
    for p, lst in occ.items():
        exps = [0] * m
        T = 0
        for k, e in lst:
            exps[k] = e
            T += e
        pw = [1] * (T + 1)
        for d in range(1, T + 1):
            pw[d] = pw[d - 1] * p % MOD
        g = (run(p, T, pw, exps, 0) - run(p, T, pw, exps, 1)) % MOD
        ans = ans * g % MOD
    print(ans % MOD)


main()
