# Solution for "Many LCS" problem
# N <= 10, so we can represent the LCS DP row as a bitmask of which positions of S are matched.
# For a mask, dp[i] = number of set bits among first i characters of S.
# Adding a character c updates the DP row using the classic recurrence:
#   new[0] = 0
#   for i=1..N:
#       if S[i-1] == c: new[i] = prev[i-1] + 1
#       else: new[i] = max(prev[i], new[i-1])
# The resulting new row is again a monotone sequence with increments of at most 1,
# therefore it corresponds to another mask (positions where new[i] = new[i-1] + 1).
# The number of possible masks is at most 2^N (1024), allowing an efficient DP.

import sys
MOD = 998244353

def mask_to_prefix_counts(mask, N):
    """Return a list prev where prev[i] = popcount of mask in first i bits (i from 0..N)."""
    # we can compute iteratively
    prev = [0] * (N + 1)
    cnt = 0
    for i in range(1, N + 1):
        if mask & (1 << (i - 1)):
            cnt += 1
        prev[i] = cnt
    return prev

def prefix_counts_to_mask(prefix):
    """Convert a prefix sum list (length N+1) with increments 0/1 to a mask.
    prefix[0] should be 0, and for i>=1, prefix[i] - prefix[i-1] is 0 or 1.
    """
    N = len(prefix) - 1
    mask = 0
    for i in range(1, N + 1):
        if prefix[i] - prefix[i - 1] == 1:
            mask |= 1 << (i - 1)
    return mask

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    S = next(it).strip()

    letters = [chr(ord('a') + i) for i in range(26)]

    dp = {0: 1}  # mask -> count, start with empty mask
    for _ in range(M):
        ndp = {}
        for mask, cnt in dp.items():
            prev = mask_to_prefix_counts(mask, N)
            for c in letters:
                # compute new prefix counts
                new = [0] * (N + 1)
                for i in range(1, N + 1):
                    if S[i - 1] == c:
                        new[i] = prev[i - 1] + 1
                    else:
                        a = prev[i]
                        b = new[i - 1]
                        new[i] = a if a >= b else b
                new_mask = prefix_counts_to_mask(new)
                ndp[new_mask] = (ndp.get(new_mask, 0) + cnt) % MOD
        dp = ndp

    # accumulate answers by popcount(mask) which equals LCS length
    ans = [0] * (N + 1)
    for mask, cnt in dp.items():
        k = mask.bit_count()
        ans[k] = (ans[k] + cnt) % MOD
    print(' '.join(str(x) for x in ans))

if __name__ == "__main__":
    solve()
