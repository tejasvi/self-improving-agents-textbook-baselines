import sys

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

    # divisors of every value up to M (only needed for values present)
    present = [False] * (M + 1)
    for a in A:
        present[a] = True
    divs = [None] * (M + 1)
    for v in range(1, M + 1):
        if present[v]:
            divs[v] = []
    for d in range(1, M + 1):
        for k in range(d, M + 1, d):
            if present[k]:
                divs[k].append(d)

    C = [0] * (M + 1)
    out = []
    ans = 0
    w = 1  # 2^(j) mod p, weight of earlier index j (0-based)
    for a in A:
        ds = divs[a]
        U = 0
        for d in ds:
            U += phi[d] * C[d]
        U %= MOD
        ans = (2 * ans + U) % MOD
        out.append(ans)
        for d in ds:
            C[d] += w
        w = w * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
