import sys
from operator import mul

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    M = max(A)

    # Euler phi sieve
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if phi[p] == p:
            for k in range(p, M + 1, p):
                phi[k] -= phi[k] // p

    # Divisor lists for all values up to M (built via sieve)
    divs = [[] for _ in range(M + 1)]
    for d in range(1, M + 1):
        for k in range(d, M + 1, d):
            divs[k].append(d)

    # C[d] = sum over earlier i with d | A_i of 2^{i-1} (mod MOD)
    C = [0] * (M + 1)
    inv2 = (MOD + 1) // 2
    pow2 = 1      # 2^{j-1}
    inv2pow = 1   # 2^{-j}
    P = 0         # sum_{j<=m} 2^{-j} T_j
    out = []
    phi_get = phi.__getitem__
    C_get = C.__getitem__
    for j in range(1, n + 1):
        a = A[j - 1]
        ds = divs[a]
        # T_j = sum_{i<j} gcd(A_i, A_j) 2^{i-1}
        T = sum(map(mul, map(phi_get, ds), map(C_get, ds))) % MOD
        inv2pow = inv2pow * inv2 % MOD
        P = (P + inv2pow * T) % MOD
        out.append(pow(2, j, MOD) * P % MOD)
        for d in ds:
            C[d] += pow2
        pow2 = pow2 * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
