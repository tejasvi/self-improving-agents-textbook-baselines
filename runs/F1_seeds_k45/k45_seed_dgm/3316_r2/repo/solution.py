from typing import List
from itertools import combinations

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        
        # Sort the array
        nums.sort()
        n = len(nums)
        
        total_sum = 0
        
        # Generate all combinations of k elements
        for combo in combinations(range(n), k):
            # Get the elements at these indices
            subsequence = [nums[i] for i in combo]
            
            # Find the minimum absolute difference between consecutive elements
            # Since the array is sorted, we only need to check consecutive elements
            min_diff = float('inf')
            for i in range(k - 1):
                diff = subsequence[i + 1] - subsequence[i]
                min_diff = min(min_diff, diff)
            
            total_sum = (total_sum + min_diff) % MOD
        
        return total_sum
