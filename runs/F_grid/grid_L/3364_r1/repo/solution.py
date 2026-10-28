from typing import List


class Solution:
    def minimumValueSum(self, nums: List[int], andValues: List[int]) -> int:
        INF = float("inf")
        n, m = len(nums), len(andValues)
        # dp[j] = min cost of splitting the prefix processed so far into j subarrays
        # (the subarray count j is the index; dp[0] is only finite at position 0)
        dp = [INF] * (m + 1)
        dp[0] = 0
        # D[j]: dict AND-value -> min dp[start][j-1] over starts whose subarray
        # [start..current] has that AND value, for subarrays forming the j-th piece
        D = [dict() for _ in range(m + 1)]
        for x in nums:
            new_dp = [INF] * (m + 1)
            new_D = [dict() for _ in range(m + 1)]
            for j in range(1, m + 1):
                d = {}
                for v, c in D[j].items():
                    w = v & x
                    if c < d.get(w, INF):
                        d[w] = c
                # new subarray starting at current element
                c = dp[j - 1]
                if c < INF:
                    if c < d.get(x, INF):
                        d[x] = c
                new_D[j] = d
                target = andValues[j - 1]
                if target in d:
                    new_dp[j] = d[target] + x
            dp = new_dp
            D = new_D
        return dp[m] if dp[m] < INF else -1
