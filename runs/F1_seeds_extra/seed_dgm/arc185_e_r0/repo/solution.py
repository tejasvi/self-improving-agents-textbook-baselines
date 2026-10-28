import sys
from operator import mul


def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    M = max(A) if A else 1

    # Euler phi sieve
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if phi[p] == p:
            for m in range(p, M + 1, p):
                phi[m] -= phi[m] // p

    # divisor lists (only needed for values that appear)
    needed = set(A)
    divs = {}
    for x in needed:
        divs[x] = []
    # enumerate divisors of needed values via trial over d
    for d in range(1, M + 1):
        for m in range(d, M + 1, d):
            if m in needed:
                divs[m].append(d)
    dphi = {}
    for x in needed:
        ds = divs[x]
        dphi[x] = (ds, [phi[d] for d in ds])

    C = [0] * (M + 1)  # sum of 2^{i-1} (unreduced) over earlier i with d | A_i
    out = []
    S = 0
    pw = 1  # 2^{k}, k = 0-based index of current element
    # element 0
    ds0 = dphi[A[0]][0]
    for d in ds0:
        C[d] += 1
    out.append(0)
    pw = 2  # 2^{1}: weight for element index 1 (0-based) is 2^{1}
    for k in range(1, n):
        x = A[k]
        ds, ph = dphi[x]
        T = sum(map(mul, ph, map(C.__getitem__, ds)))
        S = (2 * S + T) % MOD
        out.append(S)
        for d in ds:
            C[d] += pw
        pw = pw * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
