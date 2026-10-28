class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # dp[i][j] = number of ways to have arr1[i] = j
        # We process from left to right
        # For position i, we need:
        # - arr1[i-1] <= arr1[i] (arr1 is non-decreasing)
        # - arr2[i-1] >= arr2[i] which means nums[i-1] - arr1[i-1] >= nums[i] - arr1[i]
        #   This gives us: arr1[i] >= arr1[i-1] + nums[i] - nums[i-1]
        
        # Maximum possible value for arr1[i] is nums[i] (when arr2[i] = 0)
        max_val = max(nums)
        
        # Initialize: for position 0, arr1[0] can be any value from 0 to nums[0]
        dp = {}
        for j in range(nums[0] + 1):
            dp[j] = 1
        
        # Process each position
        for i in range(1, n):
            new_dp = {}
            
            for prev_val in dp:
                # arr1[i] must satisfy:
                # 1. arr1[i] >= prev_val (non-decreasing)
                # 2. arr1[i] >= prev_val + nums[i] - nums[i-1] (from non-increasing arr2)
                # 3. arr1[i] <= nums[i] (since arr2[i] >= 0)
                
                min_val = max(prev_val, prev_val + nums[i] - nums[i-1])
                max_val = nums[i]
                
                for curr_val in range(min_val, max_val + 1):
                    if curr_val not in new_dp:
                        new_dp[curr_val] = 0
                    new_dp[curr_val] = (new_dp[curr_val] + dp[prev_val]) % MOD
            
            dp = new_dp
        
        # Sum up all valid configurations
        result = 0
        for count in dp.values():
            result = (result + count) % MOD
        
        return result
