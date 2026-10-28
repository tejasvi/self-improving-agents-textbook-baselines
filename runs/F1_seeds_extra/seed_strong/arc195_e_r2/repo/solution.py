import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    A = [0, 0] + [int(x) for x in data[2:2 + n - 1]]  # A[i] for i in 2..n
    # modular inverses 1..n+1
    inv = [0, 1] + [0] * n
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    # P1[k] = sum_{i=2}^k A_i * 2(i-1)/(i(i+1)); P2[k] = sum_{i=2}^k A_i / i
    P1 = [0] * (n + 1)
    P2 = [0] * (n + 1)
    s1 = 0; s2 = 0
    for i in range(2, n + 1):
        a = A[i] % MOD
        s1 = (s1 + a * 2 * (i - 1) % MOD * inv[i] % MOD * inv[i + 1]) % MOD
        s2 = (s2 + a * inv[i]) % MOD
        P1[i] = s1
        P2[i] = s2
    fact = 1
    for i in range(2, n):
        fact = fact * i % MOD
    out = []
    idx = 2 + n - 1
    for _ in range(q):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        # i < u
        t = P1[u - 1] if u - 1 >= 0 else 0
        # i = u
        t += A[u] % MOD * (u - 1) % MOD * inv[u] if u >= 2 else 0
        # u < i < v
        t += P2[v - 1] - P2[u]
        # i = v
        t += A[v]
        out.append(t % MOD * fact % MOD)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
