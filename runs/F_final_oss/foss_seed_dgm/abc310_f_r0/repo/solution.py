# Solution for "Make 10 Again"
# We need the probability that, after throwing N dice with faces 1..A_i,
# there exists a subset of dice whose results sum to exactly 10.
# The answer must be given modulo MOD = 998244353 as described in the statement.

import sys
MOD = 998244353

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # DP over reachable subset sums up to 10.
    # State is a bitmask of length 11 (bits 0..10). Bit s set means sum s is achievable.
    # dp[mask] = number of assignments for processed dice that result in this reachable set.
    SZ = 1 << 11  # 2048
    dp = [0] * SZ
    dp[1] = 1  # only sum 0 reachable initially (bit 0)

    for a in A:
        ndp = [0] * SZ
        small = min(a, 10)
        large = a - small  # values >10, they do not change reachable sums
        for mask in range(SZ):
            cur = dp[mask]
            if cur == 0:
                continue
            # values >10 keep mask unchanged
            if large:
                ndp[mask] = (ndp[mask] + cur * large) % MOD
            # values 1..small
            for v in range(1, small + 1):
                shifted = (mask << v) & ((1 << 11) - 1)
                new_mask = mask | shifted
                ndp[new_mask] = (ndp[new_mask] + cur) % MOD
        dp = ndp

    # Count favorable assignments where sum 10 is reachable (bit 10 set)
    favorable = 0
    bit10 = 1 << 10
    for mask, cnt in enumerate(dp):
        if mask & bit10:
            favorable = (favorable + cnt) % MOD

    # Total number of possible outcomes = product of A_i
    total = 1
    for a in A:
        total = (total * a) % MOD

    # Probability = favorable / total modulo MOD
    inv_total = pow(total, MOD - 2, MOD)
    ans = favorable * inv_total % MOD
    print(ans)

if __name__ == "__main__":
    solve()
