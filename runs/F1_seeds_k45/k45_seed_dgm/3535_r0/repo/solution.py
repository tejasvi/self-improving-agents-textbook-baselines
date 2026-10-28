class Solution:
    def countOfPairs(self, nums: list[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # dp[i][v] = number of ways to choose arr1[0..i] such that arr1[i] = v
        # We use a dictionary to store only non-zero values
        dp = [{} for _ in range(n)]
        
        # Base case: first position
        # arr1[0] can be any value from 0 to nums[0]
        # arr2[0] = nums[0] - arr1[0]
        for v in range(nums[0] + 1):
            dp[0][v] = 1
        
        # Fill the DP table
        for i in range(1, n):
            # For each possible value at position i-1
            for prev_v in dp[i-1]:
                prev_arr2 = nums[i-1] - prev_v
                
                # For each possible value at position i
                # Constraints:
                # 1. arr1[i] >= arr1[i-1], so arr1[i] >= prev_v
                # 2. arr2[i] <= arr2[i-1], so nums[i] - arr1[i] <= prev_arr2
                #    which means arr1[i] >= nums[i] - prev_arr2
                # 3. arr1[i] >= 0 and arr1[i] <= nums[i]
                
                min_v = max(prev_v, nums[i] - prev_arr2)
                max_v = nums[i]
                
                for v in range(min_v, max_v + 1):
                    if v not in dp[i]:
                        dp[i][v] = 0
                    dp[i][v] = (dp[i][v] + dp[i-1][prev_v]) % MOD
        
        # Sum all the ways at the last position
        result = sum(dp[n-1].values()) % MOD
        return result
