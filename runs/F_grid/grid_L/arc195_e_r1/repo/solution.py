import sys

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    A = [0, 0] + [int(x) for x in data[2:2 + n - 1]]  # A[i] for i in 2..n
    # modular inverses 1..n+1
    inv = [0, 1] + [0] * (n)
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    # factorial (n-1)!
    f = 1
    for i in range(2, n):
        f = f * i % MOD
    # S1[k] = sum_{i=2..k} A_i*(2i-2)/(i(i+1))
    # S2[k] = sum_{i=2..k} A_i/i
    S1 = [0] * (n + 1)
    S2 = [0] * (n + 1)
    s1 = 0
    s2 = 0
    for i in range(2, n + 1):
        a = A[i] % MOD
        s1 = (s1 + a * (2 * i - 2) % MOD * inv[i] % MOD * inv[i + 1]) % MOD
        s2 = (s2 + a * inv[i]) % MOD
        S1[i] = s1
        S2[i] = s2
    out = []
    idx = 2 + n - 1
    for _ in range(q):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        # i < u
        total = S1[u - 1] if u - 1 >= 0 else 0
        # i = u
        if u >= 2:
            total += A[u] % MOD * (u - 1) % MOD * inv[u]
        # u < i < v
        if v - 1 > u:
            total += S2[v - 1] - S2[u]
        # i = v
        total += A[v] % MOD
        total %= MOD
        out.append(total * f % MOD)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
