import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    A = [0, 0] + [int(x) % MOD for x in data[2:2 + n - 1]]  # A[i], i in 2..n
    inv = [0, 1] + [0] * n
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    # S1[k] = sum_{i=2}^{k} A_i * 2(i-1)/(i(i+1))   (edges i below both u,v)
    # PB[k] = sum_{i=2}^{k} A_i / i                  (edges strictly between u and v)
    S1 = [0] * (n + 1)
    PB = [0] * (n + 1)
    for i in range(2, n + 1):
        S1[i] = (S1[i - 1] + A[i] * (2 * (i - 1) % MOD) % MOD * inv[i] % MOD * inv[i + 1]) % MOD
        PB[i] = (PB[i - 1] + A[i] * inv[i]) % MOD
    f = 1
    for i in range(2, n):
        f = f * i % MOD
    out = []
    idx = 2 + n - 1
    for _ in range(q):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        total = S1[u - 1] if u >= 2 else 0
        if u >= 2:
            total += A[u] * ((1 - inv[u]) % MOD)
        total += PB[v - 1] - PB[u]
        total += A[v]
        total %= MOD
        out.append(total * f % MOD)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
