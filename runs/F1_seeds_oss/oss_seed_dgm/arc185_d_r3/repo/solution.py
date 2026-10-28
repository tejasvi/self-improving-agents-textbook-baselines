# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    MOD = 998244353
    N_str, M_str = sys.stdin.read().strip().split()
    N = int(N_str)
    M = int(M_str)
    inv2 = (MOD + 1) // 2  # modular inverse of 2 modulo MOD (since MOD is prime)
    inv6 = pow(6, MOD-2, MOD)  # modular inverse of 6
    n = (N * M + 1) % MOD
    M_mod = M % MOD
    term1 = n * M_mod % MOD * ((M + 1) % MOD) % MOD * inv2 % MOD
    term2 = M_mod * M_mod % MOD
    term3 = ((M - 1) % MOD) * M_mod % MOD * ((2 * M - 1) % MOD) % MOD * inv6 % MOD
    inner = (term1 - term2 - term3) % MOD
    ans = N % MOD * inner % MOD
    print(ans)

if __name__ == "__main__":
    solve()
