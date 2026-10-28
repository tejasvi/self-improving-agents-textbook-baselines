import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    A = [0, 0] + [int(x) for x in data[2:2 + n - 1]]  # A[i] for i in 2..n
    inv = [0, 1] + [0] * (n + 1)
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    fact = 1
    for i in range(2, n):
        fact = fact * i % MOD
    # PF[k] = sum_{i=2}^{k} A_i*(2i-2)/(i(i+1)); PG[k] = sum_{i=2}^{k} A_i/i
    PF = [0] * (n + 1)
    PG = [0] * (n + 1)
    for i in range(2, n + 1):
        a = A[i] % MOD
        PF[i] = (PF[i - 1] + a * (2 * i - 2) % MOD * inv[i] % MOD * inv[i + 1]) % MOD
        PG[i] = (PG[i - 1] + a * inv[i]) % MOD
    out = []
    idx = 2 + n - 1
    for _ in range(q):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        # i < u (i>=2)
        s = PF[u - 1] if u - 1 >= 2 else 0
        # i == u
        if u >= 2:
            s += A[u] % MOD * (u - 1) % MOD * inv[u]
        # u < i < v
        if v - 1 > u:
            s += PG[v - 1] - PG[u]
        # i == v
        s += A[v] % MOD
        out.append(s % MOD * fact % MOD)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
