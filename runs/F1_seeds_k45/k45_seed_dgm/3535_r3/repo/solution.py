from typing import List

class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # dp[i][v] = number of ways to form monotonic pairs up to index i
        # where arr1[i] = v
        
        # For the first element
        dp = {}
        
        # arr1[0] can be from 0 to nums[0]
        # arr2[0] = nums[0] - arr1[0]
        for v in range(nums[0] + 1):
            dp[v] = 1
        
        # Process each subsequent element
        for i in range(1, n):
            new_dp = {}
            
            # Try all possible values for arr1[i]
            for curr_val in range(nums[i] + 1):
                count = 0
                
                # Try all previous values for arr1[i-1]
                for prev_val in dp:
                    # Constraint 1: arr1 is non-decreasing
                    if prev_val > curr_val:
                        continue
                    
                    # arr2[i-1] = nums[i-1] - prev_val
                    # arr2[i] = nums[i] - curr_val
                    # Constraint 2: arr2 is non-increasing
                    # So arr2[i] <= arr2[i-1]
                    # nums[i] - curr_val <= nums[i-1] - prev_val
                    # curr_val >= prev_val + nums[i] - nums[i-1]
                    
                    if curr_val >= prev_val + nums[i] - nums[i-1]:
                        count = (count + dp[prev_val]) % MOD
                
                if count > 0:
                    new_dp[curr_val] = count
            
            dp = new_dp
        
        # Sum all counts from the last position
        result = sum(dp.values()) % MOD
        return result
