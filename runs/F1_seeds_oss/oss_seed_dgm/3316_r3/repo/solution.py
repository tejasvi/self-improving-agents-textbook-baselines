from typing import List
MOD = 10**9 + 7

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        # Sort the numbers to work with ordered subsequences
        a = sorted(nums)
        n = len(a)
        if k == 1:
            # Subsequence of length 1 has no pair, define power as 0 (though k>=2 per constraints)
            return 0
        # Compute gaps between consecutive sorted elements
        gaps = [a[i+1] - a[i] for i in range(n-1)]
        # All possible threshold values (distinct gaps). Include 0 to handle the base case.
        thresholds = sorted(set(gaps))
        if 0 not in thresholds:
            thresholds = [0] + thresholds
        else:
            # ensure 0 is the first element
            thresholds = [0] + [t for t in thresholds if t != 0]

        # Function to count subsets of size k where every adjacent selected gap >= t
        def count_subsets(t: int) -> int:
            # dp[pos][cnt] = number of ways where the last selected element is at index pos and we have selected cnt elements
            dp = [[0] * (k+1) for _ in range(n)]
            for i in range(n):
                dp[i][1] = 1  # single element subsequence ending at i
            for cnt in range(2, k+1):
                for pos in range(n):
                    total = 0
                    # look back for previous positions that satisfy gap condition
                    for prev in range(pos):
                        if a[pos] - a[prev] >= t:
                            total += dp[prev][cnt-1]
                    dp[pos][cnt] = total % MOD
            # total subsets of size k is sum over last positions
            return sum(dp[pos][k] for pos in range(n)) % MOD

        # Precompute C[t] for each threshold
        C = {}
        for t in thresholds:
            C[t] = count_subsets(t)

        # Compute the answer using the formula:
        # sum = Σ (t_i - t_{i-1}) * C[t_i]
        ans = 0
        prev = 0
        for t in thresholds:
            diff = t - prev
            ans = (ans + diff * C[t]) % MOD
            prev = t
        return ans
