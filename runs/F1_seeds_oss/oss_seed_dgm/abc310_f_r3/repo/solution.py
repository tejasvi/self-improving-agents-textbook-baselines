# Write your solution here. Read from stdin, write to stdout.
import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # We only care about sums up to 10. Represent the set of reachable sums as a bitmask of 11 bits (0..10).
    M = 11
    MASK_LIMIT = (1 << M) - 1  # keep only bits 0..10
    dp = [0] * (1 << M)
    dp[1] = 1  # only sum 0 is reachable initially (bit 0 set)

    for Ai in A:
        inv = pow(Ai, MOD - 2, MOD)  # modular inverse of Ai
        maxx = min(10, Ai)           # outcomes that can affect sums <=10
        # probability of an outcome > 10 (does not change the reachable set)
        p0 = (Ai - maxx) * inv % MOD
        ndp = [0] * (1 << M)
        for mask, prob in enumerate(dp):
            if prob == 0:
                continue
            # outcomes larger than 10 keep the mask unchanged
            ndp[mask] = (ndp[mask] + prob * p0) % MOD
            # outcomes 1..maxx each have probability 1/Ai (i.e., inv)
            add = prob * inv % MOD
            for x in range(1, maxx + 1):
                new_mask = mask | ((mask << x) & MASK_LIMIT)
                ndp[new_mask] = (ndp[new_mask] + add) % MOD
        dp = ndp

    # Sum probabilities of states where sum 10 is reachable (bit 10 set)
    ans = 0
    for mask, prob in enumerate(dp):
        if (mask >> 10) & 1:
            ans = (ans + prob) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
