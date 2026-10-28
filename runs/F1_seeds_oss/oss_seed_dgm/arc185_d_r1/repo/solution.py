# Write your solution here. Read from stdin, write to stdout.
import sys
MOD = 998244353

def solve():
    import sys
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    V = N * M + 1
    # compute terms modulo MOD
    inv2 = (MOD + 1) // 2  # modular inverse of 2 under MOD (since MOD is prime)
    inv6 = pow(6, MOD - 2, MOD)
    m = M % MOD
    m1 = (M + 1) % MOD
    # sum_k = M(M+1)/2 mod
    sum_k = m * m1 % MOD * inv2 % MOD
    # sum_k2 = M(M+1)(2M+1)/6 mod
    two_m_plus1 = (2 * m + 1) % MOD
    sum_k2 = m * m1 % MOD * two_m_plus1 % MOD * inv6 % MOD
    term = (V % MOD) * sum_k % MOD
    term = (term - sum_k2) % MOD
    ans = (N % MOD) * term % MOD
    print(ans)

if __name__ == "__main__":
    solve()
