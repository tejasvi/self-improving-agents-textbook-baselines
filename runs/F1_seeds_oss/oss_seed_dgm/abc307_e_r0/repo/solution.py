# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    MOD = 998244353
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    m1 = (M - 1) % MOD
    # Compute (M-1)^N mod MOD
    pow_term = pow(m1, N, MOD)
    # Compute (-1)^N * (M-1) mod MOD
    if N % 2 == 0:
        sign_term = m1
    else:
        sign_term = (-m1) % MOD
    ans = (pow_term + sign_term) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
