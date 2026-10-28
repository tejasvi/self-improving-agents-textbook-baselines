# Write your solution here. Read from stdin, write to stdout.
import sys
MOD = 998244353

def modinv(x):
    return pow(x, MOD-2, MOD)

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    mask = (1 << 11) - 1  # keep bits 0..10
    dp = [0] * (1 << 11)
    dp[1] = 1  # only sum 0 achievable
    for ai in A:
        inv = modinv(ai)
        limit = min(10, ai)
        prob_rest = (ai - limit) * inv % MOD  # probability of values >10 (state unchanged)
        new_dp = [0] * (1 << 11)
        for state, prob in enumerate(dp):
            if prob == 0:
                continue
            # handle values >10 (no change)
            new_dp[state] = (new_dp[state] + prob * prob_rest) % MOD
            # handle each value v from 1..limit
            for v in range(1, limit + 1):
                new_state = state | ((state << v) & mask)
                new_dp[new_state] = (new_dp[new_state] + prob * inv) % MOD
        dp = new_dp
    ans = 0
    target_bit = 1 << 10
    for state, prob in enumerate(dp):
        if state & target_bit:
            ans = (ans + prob) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
