from typing import List

class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        """Return the minimum absolute difference between k and the bitwise OR of any subarray.

        Approach:
        For each position i we maintain the set of distinct OR values of subarrays ending at i.
        When we extend to the next element nums[i], each previous OR value can be OR-ed with nums[i]
        and we also have the subarray consisting of only nums[i].
        Because OR can only add bits, the number of distinct values per position is bounded by the
        number of bits (≤ 31 for numbers up to 1e9). Thus the overall complexity is O(n * 31).
        While iterating we keep track of the minimal absolute difference to k.
        """
        # Set of OR values for subarrays ending at the previous index
        prev: set[int] = set()
        ans = float('inf')
        for x in nums:
            # Start new set with current element alone
            cur: set[int] = {x}
            # Extend previous subarrays by including current element
            for v in prev:
                cur.add(v | x)
            # Reduce the set to unique values (automatically by set)
            # Update answer with all values in cur
            for v in cur:
                diff = abs(k - v)
                if diff < ans:
                    ans = diff
                    # Early exit if we hit zero, cannot get better
                    if ans == 0:
                        return 0
            # Prepare for next iteration
            # To keep the set small, we can drop values that are supersets of others.
            # However the size is already bounded, so we just assign.
            prev = cur
        return ans if ans != float('inf') else 0
