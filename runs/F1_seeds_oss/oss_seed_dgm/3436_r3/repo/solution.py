from typing import List

class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        # We keep a set of possible OR values for subarrays ending at the previous index.
        # For each new element, we combine it with each previous OR (by OR-ing) and also start a new subarray.
        # The number of distinct OR values for subarrays ending at a position is bounded by the number of bits (<=31)
        # because each OR can only add new bits, never remove them.
        # We compute the minimum absolute difference to k over all encountered OR values.
        ans = abs(k - nums[0])  # initialize with first element subarray
        prev = set()
        for x in nums:
            # generate new set of ORs for subarrays ending at current position
            cur = {x}
            for v in prev:
                cur.add(v | x)
            # update answer using all values in cur
            for v in cur:
                diff = k - v
                if diff < 0:
                    diff = -diff
                if diff < ans:
                    ans = diff
                # early exit if exact match
                if ans == 0:
                    return 0
            prev = cur
        return ans
