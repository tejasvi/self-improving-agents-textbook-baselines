# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    MOD = 998244353
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    K = int(data[1])
    inv2 = (MOD + 1) // 2  # modular inverse of 2 since MOD is prime
    # Compute modular inverse of N
    invN = pow(N, MOD - 2, MOD)
    # a = (N-2)/N mod MOD
    a = (N - 2) % MOD
    a = a * invN % MOD
    aK = pow(a, K, MOD)
    term1 = (N + 1) % MOD * inv2 % MOD
    term2 = (N - 1) % MOD * inv2 % MOD * aK % MOD
    ans = (term1 - term2) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
