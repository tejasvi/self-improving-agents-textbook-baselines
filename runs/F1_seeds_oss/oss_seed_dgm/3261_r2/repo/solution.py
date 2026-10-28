from typing import List

class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # Number of groups after exactly k merges
        groups_needed = n - k
        # Maximum possible value (since nums[i] < 2^30)
        MAX_BIT = 30
        ALL_ONES = (1 << MAX_BIT) - 1

        def feasible(limit: int) -> bool:
            """Return True if we can partition nums into at least groups_needed
            contiguous segments such that the AND of each segment has no bits
            outside 'limit' (i.e., segment_and & ~limit == 0)."""
            cnt = 0
            cur = ALL_ONES
            mask_out = ~limit  # bits that must not appear
            for val in nums:
                cur &= val
                if cur & mask_out == 0:
                    cnt += 1
                    cur = ALL_ONES
            return cnt >= groups_needed

        # Greedy bit construction: try to keep bits 0 from high to low
        answer = 0
        for bit in reversed(range(MAX_BIT)):
            # try without setting this bit
            candidate = answer  # current bits already decided, higher bits set as needed
            # we haven't decided lower bits yet, they are 0 for now
            if not feasible(candidate):
                # need this bit set
                answer |= (1 << bit)
        return answer
