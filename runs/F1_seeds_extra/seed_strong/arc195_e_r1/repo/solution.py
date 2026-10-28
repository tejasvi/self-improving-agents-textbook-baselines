import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    A = [0, 0] + [int(x) for x in data[2:2 + n - 1]]  # A[i] for i in 2..n
    # modular inverses 1..n+1
    M = n + 2
    inv = [0, 1] + [0] * (M - 1)
    for i in range(2, M + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    # F1[k] = sum_{i=2}^{k} A_i * 2(i-1)/(i(i+1)); F2[k] = sum_{i=2}^{k} A_i / i
    F1 = [0] * (n + 1)
    F2 = [0] * (n + 1)
    s1 = 0
    s2 = 0
    for i in range(2, n + 1):
        a = A[i] % MOD
        s1 = (s1 + a * (2 * (i - 1) % MOD) % MOD * inv[i] % MOD * inv[i + 1]) % MOD
        s2 = (s2 + a * inv[i]) % MOD
        F1[i] = s1
        F2[i] = s2
    fact = 1
    for i in range(2, n):
        fact = fact * i % MOD  # (n-1)!
    out = []
    idx = 2 + n - 1
    for _ in range(q):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        total = F1[u - 1] if u >= 2 else 0
        if u >= 2:
            total += A[u] % MOD * ((1 - inv[u]) % MOD)
        total += F2[v - 1] - F2[u]
        total += A[v]
        out.append(total % MOD * fact % MOD)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
