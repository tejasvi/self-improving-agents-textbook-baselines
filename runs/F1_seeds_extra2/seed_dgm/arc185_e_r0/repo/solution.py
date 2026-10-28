import sys
from operator import mul


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    MOD = 998244353
    M = max(A)

    # Euler phi sieve
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if phi[p] == p:
            for k in range(p, M + 1, p):
                phi[k] -= phi[k] // p
    # divisors with phi values, only for values that occur
    needed = set(A)
    divs = {}
    phis = {}
    for v in needed:
        divs[v] = []
    # enumerate divisors of needed values via trial over d
    for d in range(1, M + 1):
        for mlt in range(d, M + 1, d):
            if mlt in needed:
                divs[mlt].append(d)
                phis.setdefault(mlt, []).append(phi[d])

    T = [0] * (M + 1)  # T[d] = sum of 2^{i-1} over earlier i with d | A_i (unreduced, < 2^50)
    out = []
    f = 0
    pw = 1  # 2^{j-1} mod MOD
    for j in range(n):
        a = A[j]
        ds = divs[a]
        S = sum(map(mul, phis[a], map(T.__getitem__, ds))) % MOD
        f = (2 * f + S) % MOD
        out.append(f)
        for d in ds:
            T[d] += pw
        pw = pw * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
