import sys

MOD = 998244353

def mod_pow(a, n, mod=MOD):
    res = 1
    a %= mod
    while n:
        if n & 1:
            res = res * a % mod
        a = a * a % mod
        n >>= 1
    return res

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    # Using formula: (M-1)^N + (-1)^N * (M-1)
    base = (M - 1) % MOD
    term1 = mod_pow(base, N)
    term2 = base if N % 2 == 0 else (-base)
    ans = (term1 + term2) % MOD
    print(ans)

if __name__ == "__main__":
    main()
