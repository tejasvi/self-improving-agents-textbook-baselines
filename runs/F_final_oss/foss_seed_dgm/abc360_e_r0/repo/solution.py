# Write your solution here. Read from stdin, write to stdout.
import sys
MOD = 998244353

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    K = int(data[1])
    inv2 = (MOD + 1) // 2  # modular inverse of 2 since MOD is prime
    # term1 = (N + 1) / 2 mod MOD
    term1 = (N + 1) % MOD * inv2 % MOD
    if N == 1:
        # Only one ball, position always 1
        print(1)
        return
    invN = pow(N, MOD - 2, MOD)
    a = (N - 2) % MOD * invN % MOD  # ((N-2)/N) modulo MOD
    pow_a = pow(a, K, MOD)
    term2 = (N - 1) % MOD * inv2 % MOD * pow_a % MOD
    ans = (term1 - term2) % MOD
    print(ans)

if __name__ == "__main__":
    main()
