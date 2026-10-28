import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); Q = int(data[1])
    A = [0, 0] + [int(x) % MOD for x in data[2:2 + N - 1]]  # A[i] for i in 2..N
    # modular inverses 1..N+1
    inv = [0, 1] + [0] * (N + 1)
    for i in range(2, N + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD  # (N-1)!
    # Prefix sums:
    # L[k] = sum_{i=2..k} A_i * 2(i-1)/(i(i+1))   (case i < u)
    # M[k] = sum_{i=2..k} A_i / i                 (case u < i < v)
    L = [0] * (N + 1)
    M = [0] * (N + 1)
    for i in range(2, N + 1):
        c = 2 * (i - 1) % MOD * inv[i] % MOD * inv[i + 1] % MOD
        L[i] = (L[i - 1] + A[i] * c) % MOD
        M[i] = (M[i - 1] + A[i] * inv[i]) % MOD
    out = []
    idx = 2 + N - 1
    for _ in range(Q):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        # i < u: L[u-1]
        s = L[u - 1]
        # i = u (u >= 2): A_u * (u-1)/u
        if u >= 2:
            s += A[u] * (u - 1) % MOD * inv[u]
        # u < i < v: M[v-1] - M[u]
        s += (M[v - 1] - M[u]) % MOD
        # i = v
        s += A[v]
        out.append(s % MOD * fact % MOD)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
