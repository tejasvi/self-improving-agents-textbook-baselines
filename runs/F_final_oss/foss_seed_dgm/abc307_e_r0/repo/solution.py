# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    MOD = 998244353
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    base = (M - 1) % MOD
    pow_val = pow(base, N, MOD)
    sign = 1 if N % 2 == 0 else -1
    ans = (pow_val + sign * base) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
