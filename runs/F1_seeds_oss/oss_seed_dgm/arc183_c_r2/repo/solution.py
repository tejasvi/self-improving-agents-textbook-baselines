import sys

MOD = 998244353

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    # For each interval (L,R) keep a set of positions X that are forbidden to be the maximum.
    forbidden = {}
    for _ in range(M):
        L = int(next(it))
        R = int(next(it))
        X = int(next(it))
        forbidden.setdefault((L, R), set()).add(X)

    # Pre‑compute factorials and inverse factorials for binomial coefficients.
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def comb(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD

    # dp[l][r] = number of valid permutations of the positions l..r (1‑indexed).
    # We use an (N+2) sized table so that dp[i][i-1] = 1 (empty interval).
    dp = [[0] * (N + 2) for _ in range(N + 2)]
    for i in range(1, N + 2):
        dp[i][i - 1] = 1

    # Process intervals by increasing length.
    for length in range(1, N + 1):
        for l in range(1, N - length + 2):
            r = l + length - 1
            forb_set = forbidden.get((l, r))
            total = 0
            for k in range(l, r + 1):
                if forb_set is not None and k in forb_set:
                    continue  # k cannot be the position of the maximum in this interval
                left = dp[l][k - 1]
                right = dp[k + 1][r]
                ways = left * right % MOD * comb(length - 1, k - l) % MOD
                total += ways
                if total >= MOD:
                    total -= MOD
            dp[l][r] = total

    print(dp[1][N] % MOD)

if __name__ == "__main__":
    main()
