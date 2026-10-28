from typing import List

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Sort the array
        nums.sort()
        
        # Get all unique differences that could be minimum differences
        # These are differences between elements in the sorted array
        diffs = set()
        for i in range(n):
            for j in range(i + 1, n):
                diffs.add(nums[j] - nums[i])
        
        diffs = sorted(diffs)
        
        total = 0
        
        # For each possible minimum difference, count subsequences with exactly that minimum
        for target_diff in diffs:
            # dp[i][j] = number of subsequences of length i ending at position j
            # such that all consecutive elements (in the subsequence) have difference >= target_diff
            # and no two elements have difference < target_diff
            
            # We need to count subsequences where:
            # 1. Length is k
            # 2. All consecutive elements have diff >= target_diff
            # 3. At least one pair has diff == target_diff (to be the minimum)
            
            # First, count all subsequences where all consecutive elements have diff >= target_diff
            dp_all = [[0] * n for _ in range(k + 1)]
            
            for i in range(n):
                dp_all[1][i] = 1
            
            for length in range(1, k):
                for j in range(n):
                    if dp_all[length][j] == 0:
                        continue
                    # Try to extend from position j
                    for next_j in range(j + 1, n):
                        if nums[next_j] - nums[j] >= target_diff:
                            dp_all[length + 1][next_j] = (dp_all[length + 1][next_j] + dp_all[length][j]) % MOD
            
            count_geq = sum(dp_all[k]) % MOD
            
            # Count subsequences where all consecutive elements have diff > target_diff
            dp_strict = [[0] * n for _ in range(k + 1)]
            
            for i in range(n):
                dp_strict[1][i] = 1
            
            for length in range(1, k):
                for j in range(n):
                    if dp_strict[length][j] == 0:
                        continue
                    # Try to extend from position j
                    for next_j in range(j + 1, n):
                        if nums[next_j] - nums[j] > target_diff:
                            dp_strict[length + 1][next_j] = (dp_strict[length + 1][next_j] + dp_strict[length][j]) % MOD
            
            count_gt = sum(dp_strict[k]) % MOD
            
            # Subsequences with min diff exactly equal to target_diff
            count_eq = (count_geq - count_gt + MOD) % MOD
            
            total = (total + count_eq * target_diff) % MOD
        
        return total
