import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    MOD = 998244353
    M = max(A)

    # Euler's totient for 1..M
    phi = list(range(M + 1))
    for p in range(2, M + 1):
        if phi[p] == p:  # p is prime
            for k in range(p, M + 1, p):
                phi[k] -= phi[k] // p

    # Divisor lists only for values that occur
    present = set(A)
    divs = {x: [] for x in present}
    for d in range(1, M + 1):
        for x in range(d, M + 1, d):
            if x in divs:
                divs[x].append(d)
    pdivs = {x: (dl, [phi[d] for d in dl]) for x, dl in divs.items()}

    # C[d] = sum over earlier i with d | A_i of 2^(i-1)
    C = [0] * (M + 1)
    inv2 = (MOD + 1) // 2
    out = []
    S = 0      # sum_{j<=m} 2^{-j} G_j
    pow2 = 1   # 2^(j-1)
    vm = 1     # 2^{-m}
    pw_m = 1   # 2^m
    for m in range(1, n + 1):
        x = A[m - 1]
        dl, pl = pdivs[x]
        vm = vm * inv2 % MOD
        pw_m = pw_m * 2 % MOD
        G = sum([p * C[d] for p, d in zip(pl, dl)]) % MOD
        S = (S + vm * G) % MOD
        out.append(pw_m * S % MOD)
        for d in dl:
            C[d] += pow2
        pow2 = pow2 * 2 % MOD
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
