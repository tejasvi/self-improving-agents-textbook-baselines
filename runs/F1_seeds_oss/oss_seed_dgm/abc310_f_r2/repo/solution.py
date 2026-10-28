# Write your solution here. Read from stdin, write to stdout.
import sys

MOD = 998244353
FULL_MASK = (1 << 11) - 1  # we only care about sums 0..10


def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # dp[mask] = number of ways to obtain this set of achievable sums (0..10) after processing some dice
    dp = [0] * (1 << 11)
    dp[1] = 1  # only sum 0 is achievable initially (bit 0 set)
    total = 1  # total number of outcome tuples modulo MOD
    for a in A:
        total = (total * a) % MOD
        limit = min(a, 10)            # values that can affect sums up to 10
        big = (a - limit) % MOD       # number of values > 10, they do not change the mask
        ndp = [0] * (1 << 11)
        for mask, val in enumerate(dp):
            if val == 0:
                continue
            # outcomes larger than 10 keep the mask unchanged
            ndp[mask] = (ndp[mask] + val * big) % MOD
            # outcomes v = 1..limit
            for v in range(1, limit + 1):
                new_mask = mask | ((mask << v) & FULL_MASK)
                ndp[new_mask] = (ndp[new_mask] + val) % MOD
        dp = ndp

    # Count outcomes where sum 10 is NOT achievable
    notcnt = 0
    for mask, val in enumerate(dp):
        if (mask >> 10) & 1 == 0:
            notcnt = (notcnt + val) % MOD

    # Desired probability = (total - notcnt) / total
    prob = (total - notcnt) % MOD
    inv_total = pow(total, MOD - 2, MOD)
    ans = prob * inv_total % MOD
    print(ans)

if __name__ == "__main__":
    solve()
