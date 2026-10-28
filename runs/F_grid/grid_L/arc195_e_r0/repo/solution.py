import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    A = [0, 0] + [int(x) % MOD for x in data[2:2 + n - 1]]  # A[i] for i in 2..n
    # modular inverses up to n+1
    inv = [0, 1] + [0] * n
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    # PA[x] = sum_{i=2}^{x} A_i / i ; PB[x] = sum_{i=2}^{x} 2 A_i / (i(i+1))
    PA = [0] * (n + 1)
    PB = [0] * (n + 1)
    fact = 1
    for i in range(2, n + 1):
        fact = fact * (i - 1) % MOD
        PA[i] = (PA[i - 1] + A[i] * inv[i]) % MOD
        PB[i] = (PB[i - 1] + 2 * A[i] % MOD * inv[i] % MOD * inv[i + 1]) % MOD
    # fact = (n-1)!
    out = []
    idx = 2 + n - 1
    for _ in range(q):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        # E = sum_i A_i * (P(i anc u) + P(i anc v) - 2 P(i anc both)), i >= 2
        t1 = PA[u - 1]
        t2 = (A[v] + PA[v - 1]) % MOD
        t3 = 0
        if u >= 2:
            t1 += A[u]
            t3 = 2 * (A[u] * inv[u] % MOD + PB[u - 1]) % MOD
        e = (t1 + t2 - t3) % MOD
        out.append(e * fact % MOD)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
