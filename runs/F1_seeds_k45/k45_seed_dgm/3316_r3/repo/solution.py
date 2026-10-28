from typing import List

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Sort the array
        nums.sort()
        
        # Total sum of powers
        total = 0
        
        # For each possible pair (i, j) where i < j, we'll consider this pair
        # as having the minimum difference in some subsequences
        # We need to count how many subsequences of length k have (i,j) as
        # the pair with minimum difference
        
        # Key insight: for each difference value, count how many subsequences
        # of length k have this as their minimum difference
        
        # Collect all differences
        differences = []
        for i in range(n):
            for j in range(i + 1, n):
                differences.append(nums[j] - nums[i])
        
        # For each possible pair, calculate contribution
        for i in range(n):
            for j in range(i + 1, n):
                # Current pair difference
                diff = nums[j] - nums[i]
                
                # Count subsequences of length k where:
                # 1. Both i and j are included
                # 2. This pair (i,j) has the minimum difference
                
                # Use DP to count:
                # - Subsequences of length k with all pairs having diff >= current diff
                # - Subtract subsequences of length k with all pairs having diff > current diff
                
                count_geq = self._countSubsequences(nums, k, i, j, diff, False)
                count_gt = self._countSubsequences(nums, k, i, j, diff, True)
                
                contribution = (count_geq - count_gt) % MOD
                if contribution > 0:
                    total = (total + diff * contribution) % MOD
        
        return total
    
    def _countSubsequences(self, nums, k, must_i, must_j, min_diff, strict):
        """
        Count subsequences of length k that:
        - Include indices must_i and must_j
        - Have all consecutive pair differences >= min_diff (or > if strict=True)
        
        We process in sorted order, so consecutive pairs in the subsequence
        are consecutive in the sorted array.
        """
        MOD = 10**9 + 7
        n = len(nums)
        
        # dp[idx][count][last_idx] = number of subsequences using 'count' elements
        # from nums[0:idx], with last element at 'last_idx'
        # where all consecutive differences are >= min_diff (or > if strict)
        
        # Use memoization
        memo = {}
        
        def dp(idx, count, last_idx, has_i, has_j):
            # idx: current position in array
            # count: how many elements we've selected
            # last_idx: index of last selected element (-1 if none)
            # has_i: whether we've selected must_i
            # has_j: whether we've selected must_j
            
            if count == k:
                # We have k elements, check if we have both must_i and must_j
                return 1 if (has_i and has_j) else 0
            
            if idx == n or n - idx < k - count:
                # Not enough elements left
                return 0
            
            key = (idx, count, last_idx, has_i, has_j)
            if key in memo:
                return memo[key]
            
            result = 0
            
            # Option 1: Skip current element
            result += dp(idx + 1, count, last_idx, has_i, has_j)
            
            # Option 2: Include current element
            can_include = True
            if last_idx != -1:
                diff_val = nums[idx] - nums[last_idx]
                if strict:
                    can_include = diff_val > min_diff
                else:
                    can_include = diff_val >= min_diff
            
            if can_include:
                new_has_i = has_i or (idx == must_i)
                new_has_j = has_j or (idx == must_j)
                result += dp(idx + 1, count + 1, idx, new_has_i, new_has_j)
            
            result %= MOD
            memo[key] = result
            return result
        
        return dp(0, 0, -1, False, False)
