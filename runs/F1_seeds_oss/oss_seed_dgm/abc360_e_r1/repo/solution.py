# Write your solution here. Read from stdin, write to stdout.
import sys
MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    K = int(data[1])
    inv2 = (MOD + 1) // 2  # modular inverse of 2 since MOD is prime
    # compute r = (N-2)/N mod MOD
    if N % MOD == 0:
        # N == MOD, but constraints guarantee N < MOD, so this won't happen
        r = 0
    else:
        r = (N - 2) % MOD * modinv(N) % MOD
    pow_r = pow(r, K, MOD)
    term1 = (N + 1) % MOD * inv2 % MOD
    term2 = (N - 1) % MOD * inv2 % MOD * pow_r % MOD
    ans = (term1 - term2) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
