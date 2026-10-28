from typing import List

class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # dp[i][v] = count of valid configurations where arr1[i] = v
        # v is the value in arr1 at position i
        # We need arr1 to be non-decreasing and arr2 to be non-increasing
        # where arr2[i] = nums[i] - arr1[i]
        
        # Initialize dp for position 0
        # arr1[0] can be any value from 0 to nums[0]
        dp = {}
        for v in range(nums[0] + 1):
            dp[v] = 1
        
        # Process each position from 1 to n-1
        for i in range(1, n):
            new_dp = {}
            
            # For each value v that arr1[i] can take
            for v in range(nums[i] + 1):
                # arr2[i] = nums[i] - v
                arr2_i = nums[i] - v
                
                # Count valid configurations from previous position
                count = 0
                
                # We need to check all possible values at position i-1
                for prev_v in dp:
                    # arr2[i-1] = nums[i-1] - prev_v
                    arr2_prev = nums[i-1] - prev_v
                    
                    # Check constraints:
                    # 1. arr1[i-1] <= arr1[i]: prev_v <= v
                    # 2. arr2[i] <= arr2[i-1]: arr2_i <= arr2_prev
                    # 3. arr2[i] >= 0: arr2_i >= 0 (already ensured by v <= nums[i])
                    
                    if prev_v <= v and arr2_i <= arr2_prev:
                        count = (count + dp[prev_v]) % MOD
                
                if count > 0:
                    new_dp[v] = count
            
            dp = new_dp
        
        # Sum all counts at the last position
        result = sum(dp.values()) % MOD
        return result
