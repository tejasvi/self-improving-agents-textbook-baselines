from typing import List

class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        """Return the minimum absolute difference between k and the bitwise OR of any subarray.
        
        The approach maintains the set of distinct OR results for subarrays ending at the current index.
        For each new element we combine it with previous ORs, producing at most ~log(MAX) distinct values.
        This yields an O(n * log MAX) solution suitable for n up to 1e5.
        """
        # Initialize answer with a large value.
        INF = 2 * 10**9  # larger than any possible difference (k up to 1e9, OR up to ~2^30)
        ans = INF
        # Set of OR values for subarrays ending at the previous position.
        prev_or_set = set()
        for x in nums:
            # Start new subarrays with the current element.
            cur_set = {x}
            # Extend previous subarrays by including current element.
            for val in prev_or_set:
                cur_set.add(val | x)
            # Update answer using all ORs that end at this index.
            for val in cur_set:
                diff = k - val
                if diff < 0:
                    diff = -diff
                if diff < ans:
                    ans = diff
                    if ans == 0:
                        return 0
            # Prepare for next iteration.
            prev_or_set = cur_set
        return ans
