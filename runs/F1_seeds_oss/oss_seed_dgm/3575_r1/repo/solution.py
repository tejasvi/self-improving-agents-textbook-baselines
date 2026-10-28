from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # DP1[i][j] = set of possible OR results using j elements from first i elements (0..i-1)
        dp1 = [ [set() for _ in range(k+1)] for _ in range(n+1) ]
        dp1[0][0].add(0)
        for i in range(1, n+1):
            val = nums[i-1]
            for j in range(k+1):
                # not take element i-1
                dp1[i][j] = dp1[i-1][j].copy()
                if j>0:
                    for mask in dp1[i-1][j-1]:
                        dp1[i][j].add(mask | val)
        # DP2[i][j] = set of possible OR results using j elements from suffix starting at i (i..n-1)
        dp2 = [ [set() for _ in range(k+1)] for _ in range(n+1) ]
        dp2[n][0].add(0)
        for i in range(n-1, -1, -1):
            val = nums[i]
            for j in range(k+1):
                dp2[i][j] = dp2[i+1][j].copy()
                if j>0:
                    for mask in dp2[i+1][j-1]:
                        dp2[i][j].add(mask | val)
        ans = 0
        # split point i: first subsequence of size k from prefix [0,i), second of size k from suffix [i,n)
        for i in range(n+1):
            if not dp1[i][k] or not dp2[i][k]:
                continue
            for m1 in dp1[i][k]:
                for m2 in dp2[i][k]:
                    ans = max(ans, m1 ^ m2)
        return ans
