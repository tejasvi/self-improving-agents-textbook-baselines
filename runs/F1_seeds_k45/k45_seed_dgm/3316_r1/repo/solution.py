from typing import List

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Sort the array
        nums.sort()
        
        total = 0
        
        # For each pair of indices (i, j) with i < j,
        # Count subsequences of length k where both i and j are included
        # and the minimum difference is exactly nums[j] - nums[i]
        
        for j in range(n):
            for i in range(j):
                min_diff = nums[j] - nums[i]
                
                # Count k-length subsequences containing both nums[i] and nums[j]
                # where the minimum pairwise difference is exactly min_diff
                
                # Count those with min_diff >= min_diff
                count = self._count_with_constraint(nums, i, j, k, min_diff)
                
                # Subtract those with minimum > min_diff
                # (we want exactly min_diff as the minimum)
                count -= self._count_with_constraint(nums, i, j, k, min_diff + 1)
                
                total = (total + count * min_diff) % MOD
        
        return total % MOD
    
    def _count_with_constraint(self, nums: List[int], must_i: int, must_j: int, k: int, min_diff: int) -> int:
        """
        Count subsequences of length k containing both must_i and must_j
        where all consecutive selected elements (when sorted) have difference >= min_diff
        """
        MOD = 10**9 + 7
        n = len(nums)
        
        # DP with memoization
        memo = {}
        
        def dp(idx, cnt, has_i, has_j, last_val):
            """
            idx: current position in nums
            cnt: number of elements selected
            has_i: whether nums[must_i] is selected
            has_j: whether nums[must_j] is selected
            last_val: value of last selected element
            """
            if cnt == k:
                return 1 if (has_i and has_j) else 0
            
            if idx == n or n - idx + cnt < k:  # Not enough elements left
                return 0
            
            state = (idx, cnt, has_i, has_j, last_val)
            if state in memo:
                return memo[state]
            
            result = 0
            
            # Don't select nums[idx]
            result += dp(idx + 1, cnt, has_i, has_j, last_val)
            
            # Select nums[idx]
            if last_val is None or nums[idx] - last_val >= min_diff:
                new_has_i = has_i or (idx == must_i)
                new_has_j = has_j or (idx == must_j)
                result += dp(idx + 1, cnt + 1, new_has_i, new_has_j, nums[idx])
            
            result %= MOD
            memo[state] = result
            return result
        
        return dp(0, 0, False, False, None)
