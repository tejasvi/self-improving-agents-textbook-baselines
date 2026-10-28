import sys
from operator import mul, itemgetter

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    MAXV = max(A)

    # Euler phi
    phi = list(range(MAXV + 1))
    for p in range(2, MAXV + 1):
        if phi[p] == p:
            for m in range(p, MAXV + 1, p):
                phi[m] -= phi[m] // p

    present = bytearray(MAXV + 1)
    for a in A:
        present[a] = 1

    # divisors only for present values
    divs = [None] * (MAXV + 1)
    for v in range(1, MAXV + 1):
        if present[v]:
            divs[v] = []
    for d in range(1, MAXV + 1):
        for m in range(d, MAXV + 1, d):
            if present[m]:
                divs[m].append(d)
    phis = [None] * (MAXV + 1)
    getters = [None] * (MAXV + 1)
    for v in range(1, MAXV + 1):
        if present[v]:
            phis[v] = [phi[d] for d in divs[v]]
            getters[v] = itemgetter(*divs[v]) if len(divs[v]) > 1 else (lambda S, d=divs[v][0]: (S[d],))

    # pow2[k] = 2^k mod MOD
    pow2 = [1] * (n + 1)
    for k in range(1, n + 1):
        pow2[k] = pow2[k - 1] * 2 % MOD

    S = [0] * (MAXV + 1)  # unreduced sums of pow2 values (kept small enough)
    T = [0] * n
    i = 0
    while i < n:
        v = A[i]
        j = i
        while j < n and A[j] == v:
            j += 1
        dv = divs[v]
        pv = phis[v]
        base = sum(map(mul, pv, getters[v](S))) % MOD
        # within-run contributions: gcd(v,v)=v times earlier same-run weights
        acc = 0
        for k in range(i, j):
            T[k] = (base + v * acc) % MOD
            acc += pow2[k]
        W = acc % MOD
        for d in dv:
            S[d] += W
        i = j

    out = []
    ans = 0
    for j in range(n):
        ans = (2 * ans + T[j]) % MOD
        out.append(ans)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
