from typing import List

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        nums.sort()
        n = len(nums)
        
        total_sum = 0
        
        # dp[i][j][p] = number of subsequences of length j using elements from nums[0:i]
        # where the last selected element is at index p
        # We'll track this to enforce the gap constraint
        
        # Better: for each gap value that appears between consecutive sorted elements,
        # count how many subsequences have that as their minimum gap
        
        # The minimum gap in a subsequence is determined by the minimum difference
        # between any two consecutive elements in the sorted subsequence
        
        # Approach:
        # 1. For each possible gap value g (which is a difference in the sorted array)
        # 2. Count subsequences where all gaps are >= g, minus subsequences where all gaps are > g
        
        # Collect all possible gap values
        gaps = set()
        for i in range(n - 1):
            gaps.add(nums[i + 1] - nums[i])
        
        gaps = sorted(gaps)
        
        # For each gap value, count subsequences with that minimum gap
        for gap_val in gaps:
            count_geq = self._count_subsequences_with_min_gap(nums, k, gap_val)
            count_gt = self._count_subsequences_with_min_gap(nums, k, gap_val + 1)
            count_eq = (count_geq - count_gt) % MOD
            total_sum = (total_sum + gap_val * count_eq) % MOD
        
        return total_sum
    
    def _count_subsequences_with_min_gap(self, nums, k, min_gap):
        """
        Count subsequences of length k where all consecutive elements
        (in sorted order) differ by at least min_gap
        """
        MOD = 10**9 + 7
        n = len(nums)
        
        # dp[i][j][last_idx] = number of ways to select j elements from first i elements,
        # where the last selected element is at index last_idx,
        # and all consecutive selected elements differ by at least min_gap
        
        # This would be O(n^3 * k) which might be too slow
        # Let's use: dp[i][j] = number of ways to select j elements from first i elements
        # But we need to track what the last selected element was
        
        # dp[i][j][p] where p is the index of the last selected element
        # This is O(n^3 * k) for all pairs, but we need a better approach
        
        # Actually, we can use:
        # dp[i][j] where we process elements in order
        # and for each element, we track which previous element it was added after
        
        # Simpler: dp[i][j] = list/dict of (count, last_index)
        # But let's use a direct approach with memoization
        
        memo = {}
        
        def dp(idx, count, last_idx):
            # Count ways to select 'count' more elements from nums[idx:],
            # where the last selected element was at last_idx
            if count == 0:
                return 1
            if idx >= len(nums):
                return 0
            
            if (idx, count, last_idx) in memo:
                return memo[(idx, count, last_idx)]
            
            result = 0
            
            # Skip current element
            result += dp(idx + 1, count, last_idx)
            
            # Take current element if it satisfies the gap constraint
            if last_idx == -1:  # First element
                result += dp(idx + 1, count - 1, idx)
            elif nums[idx] - nums[last_idx] >= min_gap:
                result += dp(idx + 1, count - 1, idx)
            
            result %= MOD
            memo[(idx, count, last_idx)] = result
            return result
        
        return dp(0, k, -1)
