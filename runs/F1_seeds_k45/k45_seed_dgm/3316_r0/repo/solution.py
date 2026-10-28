from typing import List

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        
        # Sort the array
        nums.sort()
        n = len(nums)
        
        result = 0
        
        def backtrack(idx, current_subseq):
            nonlocal result
            
            if len(current_subseq) == k:
                # Calculate minimum difference in current subsequence
                min_diff = float('inf')
                for i in range(len(current_subseq) - 1):
                    diff = current_subseq[i + 1] - current_subseq[i]  # Already sorted
                    min_diff = min(min_diff, diff)
                result = (result + min_diff) % MOD
                return
            
            if idx == n:
                return
            
            # Include current element
            backtrack(idx + 1, current_subseq + [nums[idx]])
            
            # Exclude current element
            backtrack(idx + 1, current_subseq)
        
        backtrack(0, [])
        
        return result
