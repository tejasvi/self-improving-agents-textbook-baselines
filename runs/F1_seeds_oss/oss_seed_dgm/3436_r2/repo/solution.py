from typing import List

class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        # We maintain a set of possible OR values for subarrays ending at the previous index.
        # For each new element, we create new ORs by OR-ing it with each value from previous set,
        # plus the element itself as a subarray of length 1.
        # The number of distinct OR values for subarrays ending at a position is bounded by
        # the number of bits (<= 30 for numbers up to 1e9), so the overall complexity is O(N * 30).
        best = abs(k - nums[0])  # initialize with first element subarray
        prev = set()
        for num in nums:
            # start new set for subarrays ending at current position
            cur = {num}
            # extend previous subarrays
            for val in prev:
                cur.add(val | num)
            # evaluate differences
            for val in cur:
                diff = k - val
                if diff < 0:
                    diff = -diff
                if diff < best:
                    best = diff
                    # early exit: if exact match found, cannot do better than 0
                    if best == 0:
                        return 0
            # keep only distinct values; also we can prune values that are already larger than best+ k?
            # However pruning is optional; we keep full set as it's already small.
            prev = cur
        return best
