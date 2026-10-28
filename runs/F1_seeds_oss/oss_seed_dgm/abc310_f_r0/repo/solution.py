# Write your solution here. Read from stdin, write to stdout.
import sys

MOD = 998244353
FULL_MASK = (1 << 11) - 1  # sums 0..10

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    dp = [0] * (1 << 11)
    dp[1] = 1  # only sum 0 achievable initially (bit 0)

    for a in A:
        inv = pow(a, MOD - 2, MOD)
        max_val = min(a, 10)
        prob_each = inv  # probability for each value 1..max_val (if within range)
        # probability for values >10 (or >a) that do nothing
        prob_other = (a - max_val) * inv % MOD
        ndp = [0] * (1 << 11)
        for mask in range(1 << 11):
            cur = dp[mask]
            if cur == 0:
                continue
            # values >10: mask unchanged
            ndp[mask] = (ndp[mask] + cur * prob_other) % MOD
            # values 1..max_val
            for v in range(1, max_val + 1):
                new_mask = mask | ((mask << v) & FULL_MASK)
                ndp[new_mask] = (ndp[new_mask] + cur * prob_each) % MOD
        dp = ndp
    # answer is sum of probabilities where bit 10 is set
    ans = 0
    for mask, prob in enumerate(dp):
        if mask & (1 << 10):
            ans = (ans + prob) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
