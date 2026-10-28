import sys
from operator import mul


def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    M = max(A) + 1

    # phi via sieve
    phi = list(range(M))
    for p in range(2, M):
        if phi[p] == p:  # p is prime
            for k in range(p, M, p):
                phi[k] -= phi[k] // p

    # divisors and phi(d) for each divisor, for every value < M
    divs = [[] for _ in range(M)]
    phs = [[] for _ in range(M)]
    for d in range(1, M):
        ph = phi[d]
        for m in range(d, M, d):
            divs[m].append(d)
            phs[m].append(ph)

    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = pow2[i - 1] * 2 % MOD
    inv2 = (MOD + 1) // 2
    ipow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        ipow2[i] = ipow2[i - 1] * inv2 % MOD

    # C[d] = sum of 2^{i-1} over earlier i with d | A_i (kept reduced mod)
    C = [0] * M
    S = 0
    out = []
    app = out.append
    for j in range(1, n + 1):
        a = A[j - 1]
        dl = divs[a]
        # T_j = sum_{i<j} 2^{i-1} gcd(A_i, A_j)
        T = sum(map(mul, phs[a], map(C.__getitem__, dl)))
        S = (S + ipow2[j] * (T % MOD)) % MOD
        app(pow2[j] * S % MOD)
        w = pow2[j - 1]
        for d in dl:
            C[d] += w
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
