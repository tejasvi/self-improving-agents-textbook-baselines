import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    inv2 = pow(2, MOD - 2, MOD)
    # E_{t+1} = (1 - 2/N) E_t + (N+1)/N, E_0 = 1
    # Fixed point (N+1)/2  =>  E_K = (N+1)/2 + (1 - 2/N)^K * (1 - (N+1)/2)
    inv_n = pow(n % MOD, MOD - 2, MOD)
    c = (1 - 2 * inv_n) % MOD
    half = (n + 1) * inv2 % MOD
    ans = (half + pow(c, k, MOD) * ((1 - half) % MOD)) % MOD
    print(ans)


if __name__ == "__main__":
    main()
