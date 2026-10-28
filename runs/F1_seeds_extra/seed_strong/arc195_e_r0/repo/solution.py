import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0]); q = int(data[1])
    A = [0] * (n + 2)
    for i in range(2, n + 1):
        A[i] = int(data[i])  # data[2..n] correspond to A_2..A_n
    # inverses up to n+1
    M = n + 2
    inv = [0, 1] + [0] * (M - 1)
    for i in range(2, M + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    # F[x] = sum_{j=2}^{x-1} A_j/j ; G[x] = sum_{j=2}^{x-1} 2A_j/(j(j+1))
    F = [0] * (n + 2)
    G = [0] * (n + 2)
    for x in range(2, n + 2):
        j = x - 1
        if j >= 2:
            F[x] = (F[x - 1] + A[j] * inv[j]) % MOD
            G[x] = (G[x - 1] + 2 * A[j] % MOD * inv[j] % MOD * inv[j + 1]) % MOD
        else:
            F[x] = 0
            G[x] = 0
    fact = 1
    for i in range(2, n):
        fact = fact * i % MOD  # (n-1)!
    out = []
    pos = n + 1  # index into data after A values
    # data layout: N Q A_2..A_N => A_i at data[2 + (i-2)] = data[i]
    for _ in range(q):
        u = int(data[pos]); v = int(data[pos + 1]); pos += 2
        def part(x):
            # sum_j A_j a_x(j), j>=2
            if x == 1:
                return 0
            return (F[x] + A[x]) % MOD
        def qpart(x):
            # sum_j A_j q(j) with q(j) for j<x, and q(x)=1/x
            if x == 1:
                return 0
            return (G[x] + A[x] * inv[x]) % MOD
        # sum over j with exactly-one: a_u + a_v - 2 q
        # q for pair (u,v) with u<v is qpart(u)
        total = (part(u) + part(v) - 2 * qpart(u)) % MOD
        out.append(total * fact % MOD)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
