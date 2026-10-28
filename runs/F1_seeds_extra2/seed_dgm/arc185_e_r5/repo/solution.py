import sys
from operator import mul


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    MOD = 998244353
    M = max(A) if A else 1

    # Euler phi sieve
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if phi[p] == p:
            for k in range(p, M + 1, p):
                phi[k] -= phi[k] // p

    # divisor lists, only for values that appear
    present = [False] * (M + 1)
    for a in A:
        present[a] = True
    divs = [None] * (M + 1)
    for v in range(1, M + 1):
        if present[v]:
            divs[v] = []
    for d in range(1, M + 1):
        for m in range(d, M + 1, d):
            if present[m]:
                divs[m].append(d)
    # phi values aligned with divisor lists
    phis = [None] * (M + 1)
    for v in range(1, M + 1):
        if present[v]:
            phis[v] = [phi[d] for d in divs[v]]

    T = [0] * (M + 1)
    out = []
    ans = 0
    pw = 1  # 2^{j-1} mod MOD
    for j in range(n):
        a = A[j]
        dl = divs[a]
        pl = phis[a]
        S = sum(map(mul, pl, [T[d] for d in dl])) % MOD
        ans = (2 * ans + S) % MOD
        out.append(ans)
        for d in dl:
            T[d] += pw
        # keep T bounded
        for d in dl:
            if T[d] >= MOD:
                T[d] %= MOD
        pw = pw * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
