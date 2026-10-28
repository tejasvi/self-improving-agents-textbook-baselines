import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    A = [0, 0] + [int(x) % MOD for x in data[2:2 + n - 1]]  # A[i] for i in 2..n
    # inverses up to n+1
    inv = [0, 1] + [0] * n
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    # S1[k] = sum_{i=2}^{k} A_i * 2(i-1)/(i(i+1))
    # S2[k] = sum_{i=2}^{k} A_i / i
    S1 = [0] * (n + 1)
    S2 = [0] * (n + 1)
    for i in range(2, n + 1):
        a = A[i]
        S1[i] = (S1[i - 1] + a * 2 * (i - 1) % MOD * inv[i] % MOD * inv[i + 1]) % MOD
        S2[i] = (S2[i - 1] + a * inv[i]) % MOD
    fact = 1
    for i in range(2, n):
        fact = fact * i % MOD  # (n-1)!
    out = []
    pos = 2 + n - 1
    for _ in range(q):
        u = int(data[pos]); v = int(data[pos + 1]); pos += 2
        e = S1[u - 1]
        if u >= 2:
            e += A[u] * ((1 - inv[u]) % MOD)
        if v - 1 > u:
            e += S2[v - 1] - S2[u]
        e += A[v]
        out.append(e % MOD * fact % MOD)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
