import sys
from operator import mul


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    MOD = 998244353
    M = max(A)

    # Euler phi sieve
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if phi[p] == p:
            for k in range(p, M + 1, p):
                phi[k] -= phi[k] // p

    # Divisor lists only for values that actually occur.
    present = set(A)
    divs = {}
    needed = [False] * (M + 1)
    for a in present:
        needed[a] = True
    for d in range(1, M + 1):
        for k in range(d, M + 1, d):
            if needed[k]:
                divs.setdefault(k, []).append(d)
    phis = {}
    for a, ds in divs.items():
        phis[a] = [phi[d] for d in ds]

    # gcd(a, b) = sum_{d | gcd(a,b)} phi(d).
    # For prefix position m with value a:
    #   ans_m = 2*ans_{m-1} + sum_{i<m} gcd(A_i, A_m) * 2^{i-1}
    #         = 2*ans_{m-1} + sum_{d | A_m} phi(d) * W[d]
    # where W[d] = sum_{i<m, d | A_i} 2^{i-1} (mod MOD).
    W = [0] * (M + 1)
    pw = 1  # 2^{i-1} for the current 1-indexed position i
    ans = 0
    out = []
    getW = W.__getitem__
    for a in A:
        ds = divs[a]
        t = sum(map(mul, phis[a], map(getW, ds)))
        ans = (2 * ans + t) % MOD
        out.append(ans)
        for d in ds:
            W[d] = (W[d] + pw) % MOD
        pw = pw * 2 % MOD

    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
