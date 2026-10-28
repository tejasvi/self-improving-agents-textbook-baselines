from typing import List

class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # dp[v] = number of ways where arr1[i-1] = v
        # We'll transition from one position to the next
        
        # For position 0, arr1[0] can be from 0 to nums[0]
        # arr2[0] = nums[0] - arr1[0]
        dp = {}
        for v in range(nums[0] + 1):
            dp[v] = 1
        
        # Process each subsequent position
        for i in range(1, n):
            new_dp = {}
            
            # For position i, try all possible values of arr1[i]
            for arr1_i in range(nums[i] + 1):
                arr2_i = nums[i] - arr1_i
                if arr2_i < 0:
                    continue
                
                # Count ways to reach arr1_i at position i
                # We need arr1[i-1] <= arr1[i] and arr2[i] <= arr2[i-1]
                # which means arr2[i-1] >= arr2[i]
                # arr2[i-1] = nums[i-1] - arr1[i-1]
                # So: nums[i-1] - arr1[i-1] >= nums[i] - arr1[i]
                # arr1[i] - arr1[i-1] >= nums[i] - nums[i-1]
                
                count = 0
                for prev_arr1 in dp:
                    prev_arr2 = nums[i-1] - prev_arr1
                    
                    # Check constraints
                    # arr1 is non-decreasing: arr1[i] >= arr1[i-1]
                    if arr1_i < prev_arr1:
                        continue
                    
                    # arr2 is non-increasing: arr2[i] <= arr2[i-1]
                    if arr2_i > prev_arr2:
                        continue
                    
                    count = (count + dp[prev_arr1]) % MOD
                
                if count > 0:
                    new_dp[arr1_i] = count
            
            dp = new_dp
        
        # Sum all ways at the last position
        result = sum(dp.values()) % MOD
        return result
