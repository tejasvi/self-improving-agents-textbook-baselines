class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        """
        Minimize the bitwise OR of remaining elements after at most k operations.
        Each operation: pick index i, replace nums[i] and nums[i+1] with nums[i] & nums[i+1]
        
        DP approach:
        - dp(pos, ops_left) = minimum OR we can achieve starting from position pos with ops_left operations left
        - At each position, we decide how many consecutive elements to AND together
        - ANDing m consecutive elements uses m-1 operations
        """
        from functools import lru_cache
        
        @lru_cache(None)
        def dp(pos, ops_left):
            """
            Returns minimum OR we can achieve starting from position pos with ops_left operations left.
            """
            if pos >= len(nums):
                return 0
            
            best = float('inf')
            segment_and = nums[pos]
            
            # Try ANDing next 1, 2, 3, ... elements
            for count in range(1, len(nums) - pos + 1):
                # segment_and now contains AND of nums[pos:pos+count]
                # Update: add nums[pos+count-1] to the AND
                if count > 1:
                    segment_and &= nums[pos + count - 1]
                
                # Number of operations needed: count - 1
                ops_needed = count - 1
                
                if ops_needed <= ops_left:
                    # We can form this segment
                    next_pos = pos + count
                    future_or = dp(next_pos, ops_left - ops_needed)
                    current_or = segment_and | future_or
                    best = min(best, current_or)
            
            return best if best != float('inf') else 0
        
        result = dp(0, k)
        return result
