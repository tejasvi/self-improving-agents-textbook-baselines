from typing import List

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        nums.sort()
        n = len(nums)
        result = 0
        
        # For each consecutive pair in sorted array
        for i in range(n - 1):
            min_diff = nums[i + 1] - nums[i]
            
            # Count k-length subsequences where:
            # 1. Elements at positions i and i+1 are both included and are consecutive in the subsequence
            # 2. All gaps between consecutive elements in subsequence are >= min_diff
            
            # DP:
            # left[j][c] = ways to pick c elements from [0..j] ending at j, with all gaps >= min_diff
            # right[j][c] = ways to pick c elements from [j..n-1] starting at j, with all gaps >= min_diff
            
            left = [[0] * (k + 1) for _ in range(n)]
            right = [[0] * (k + 1) for _ in range(n)]
            
            # Fill left DP
            for j in range(n):
                left[j][1] = 1
                for c in range(2, k + 1):
                    for prev in range(j):
                        if nums[j] - nums[prev] >= min_diff:
                            left[j][c] = (left[j][c] + left[prev][c - 1]) % MOD
            
            # Fill right DP
            for j in range(n - 1, -1, -1):
                right[j][1] = 1
                for c in range(2, k + 1):
                    for nxt in range(j + 1, n):
                        if nums[nxt] - nums[j] >= min_diff:
                            right[j][c] = (right[j][c] + right[nxt][c - 1]) % MOD
            
            # Combine: pick left_cnt from left side, right_cnt from right side
            for left_cnt in range(1, k):
                right_cnt = k - left_cnt
                if right_cnt >= 1:
                    count = (left[i][left_cnt] * right[i + 1][right_cnt]) % MOD
                    contribution = (min_diff * count) % MOD
                    result = (result + contribution) % MOD
        
        return result
