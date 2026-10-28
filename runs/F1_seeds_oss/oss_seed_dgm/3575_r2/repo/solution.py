from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # prefix_dp[t] = set of possible OR values using exactly t elements from processed prefix
        prefix_dp = [set() for _ in range(k+1)]
        prefix_dp[0].add(0)
        # store for each index i the set of OR values for exactly k elements using indices <= i
        prefix_or = [set() for _ in range(n)]
        for i, val in enumerate(nums):
            # update dp in reverse order of t to avoid reuse of current element multiple times
            upper = min(k, i+1)
            for t in range(upper, 0, -1):
                for prev in list(prefix_dp[t-1]):
                    prefix_dp[t].add(prev | val)
            if k <= i+1:
                prefix_or[i] = set(prefix_dp[k])
        # suffix processing
        suffix_dp = [set() for _ in range(k+1)]
        suffix_dp[0].add(0)
        suffix_or = [set() for _ in range(n)]
        for i in range(n-1, -1, -1):
            val = nums[i]
            upper = min(k, n - i)
            for t in range(upper, 0, -1):
                for prev in list(suffix_dp[t-1]):
                    suffix_dp[t].add(prev | val)
            if n - i >= k:
                suffix_or[i] = set(suffix_dp[k])
        # combine results: split after i (first group ends at i, second starts at i+1)
        best = 0
        for i in range(n-1):
            left_set = prefix_or[i]
            right_set = suffix_or[i+1]
            if not left_set or not right_set:
                continue
            # brute force all pairs (max 128*128=16384)
            for a in left_set:
                for b in right_set:
                    val = a ^ b
                    if val > best:
                        best = val
        return best
