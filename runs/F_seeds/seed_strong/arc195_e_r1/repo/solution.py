import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    A = [0, 0] + [int(x) for x in data[2:2 + n - 1]]  # A[i] for i in 2..n
    # inverses up to n+1
    M = n + 2
    inv = [0, 1] + [0] * (M - 1)
    for i in range(2, M + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    PB = [0] * (n + 1)  # PB[k] = sum_{i=2}^k 2(i-1)/(i(i+1)) * A_i
    PC = [0] * (n + 1)  # PC[k] = sum_{i=2}^k A_i / i
    fb = 0; fc = 0
    for i in range(2, n + 1):
        a = A[i]
        fb = (fb + 2 * (i - 1) % MOD * inv[i] % MOD * inv[i + 1] % MOD * a) % MOD
        fc = (fc + a * inv[i]) % MOD
        PB[i] = fb
        PC[i] = fc
    F = 1
    for i in range(2, n):
        F = F * i % MOD
    # F = (n-1)!
    out = []
    idx = 2 + n - 1
    for _ in range(q):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        s = PB[u - 1]
        if u >= 2:
            s += A[u] * (u - 1) % MOD * inv[u]
        s += PC[v - 1] - PC[u]
        s += A[v]
        out.append(s % MOD * F % MOD)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
