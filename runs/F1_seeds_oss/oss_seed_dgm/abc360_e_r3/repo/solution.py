# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    MOD = 998244353
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    K = int(data[1])
    inv2 = (MOD + 1) // 2  # modular inverse of 2
    if N == 1:
        print(1)
        return
    invN = pow(N, MOD - 2, MOD)
    a = (N - 2) * invN % MOD  # a = 1 - 2/N modulo MOD
    pow_a = pow(a, K, MOD)
    term1 = (N + 1) % MOD * inv2 % MOD
    term2 = (N - 1) % MOD * inv2 % MOD
    ans = (term1 - term2 * pow_a) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
