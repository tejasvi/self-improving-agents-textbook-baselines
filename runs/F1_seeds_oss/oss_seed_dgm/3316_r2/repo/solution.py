from typing import List
from bisect import bisect_right

MOD = 10**9 + 7

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        """Return the sum of powers of all subsequences of length ``k``.

        The *power* of a subsequence is the minimum absolute difference between any
        two elements of the subsequence.
        """
        n = len(nums)
        if k < 2:
            return 0  # By constraints k >= 2, but safety.

        a = sorted(nums)

        # All possible values the minimum gap can take – all pairwise absolute
        # differences. The number of distinct values is at most n*(n-1)/2 (<=1225).
        all_diffs = set()
        for i in range(n):
            for j in range(i + 1, n):
                all_diffs.add(abs(nums[i] - nums[j]))
        # Sort descending so we can apply inclusion‑exclusion later.
        diffs_desc = sorted(all_diffs, reverse=True)

        # DP helper: count of k‑subsets whose *minimum* gap is at least ``gap``.
        # In a sorted array this is equivalent to requiring that any two
        # consecutive selected elements differ by >= ``gap``.
        def count_ge(gap: int) -> int:
            # dp[c][i] – ways to pick c elements with the last chosen element at
            # position i (0‑based) and respecting the gap condition.
            dp = [[0] * n for _ in range(k + 1)]
            for i in range(n):
                dp[1][i] = 1
            # Build for larger subset sizes.
            for c in range(2, k + 1):
                # Prefix sums of dp[c-1] to obtain sums over valid previous indices
                # in O(1) per i.
                pref = [0] * n
                pref[0] = dp[c - 1][0]
                for i in range(1, n):
                    pref[i] = (pref[i - 1] + dp[c - 1][i]) % MOD
                for i in range(n):
                    # Find the rightmost index j < i such that a[i] - a[j] >= gap.
                    # All indices <= j are valid predecessors.
                    target = a[i] - gap
                    j = bisect_right(a, target) - 1
                    if j >= 0:
                        dp[c][i] = pref[j]
                    else:
                        dp[c][i] = 0
            # Total subsets of size k = sum over last index.
            return sum(dp[k][i] for i in range(n)) % MOD

        # Pre‑compute count_ge for each distinct gap.
        ge_counts = {g: count_ge(g) for g in diffs_desc}

        # Inclusion‑exclusion: for each gap (processed from largest to smallest)
        # the number of subsets whose *minimum* gap equals that gap is
        # count_ge(gap) minus the sum of already‑accounted subsets for larger gaps.
        ans = 0
        cumulative = 0  # subsets already counted for larger gaps
        for g in diffs_desc:
            exact = (ge_counts[g] - cumulative) % MOD
            ans = (ans + (g % MOD) * exact) % MOD
            cumulative = (cumulative + exact) % MOD
        return ans
