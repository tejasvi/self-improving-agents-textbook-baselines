from typing import List

class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # dp[i][v] = number of ways to fill arr1[0...i] such that arr1[i] = v
        # We process position by position and track valid values for arr1[i]
        
        # For position 0, arr1[0] can be any value from 0 to nums[0]
        # dp[0] is a dictionary mapping value -> count
        dp = {}
        for v in range(nums[0] + 1):
            dp[v] = 1
        
        # For each subsequent position
        for i in range(1, n):
            new_dp = {}
            
            # For each previous value
            for prev_val, count in dp.items():
                # arr1[i] must satisfy:
                # 1. arr1[i] >= prev_val (non-decreasing)
                # 2. arr1[i] >= prev_val + (nums[i] - nums[i-1]) (arr2 non-increasing)
                # 3. arr1[i] <= nums[i] (so arr2[i] >= 0)
                
                min_val = max(prev_val, prev_val + (nums[i] - nums[i-1]))
                max_val = nums[i]
                
                # Add all valid values in this range
                for v in range(min_val, max_val + 1):
                    if v not in new_dp:
                        new_dp[v] = 0
                    new_dp[v] = (new_dp[v] + count) % MOD
            
            dp = new_dp
        
        # Sum all the ways
        result = sum(dp.values()) % MOD
        return result
