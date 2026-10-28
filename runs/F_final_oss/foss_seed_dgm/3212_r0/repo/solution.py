from typing import List

MOD = 10**9 + 7

class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        """Return the number of good partitions of the array.

        A partition is good if no integer appears in more than one subarray.
        This is equivalent to counting the positions where we can cut the
        array so that the left part and the right part share no common values.
        The total number of good partitions is 2^{k}, where *k* is the number
        of such cut positions (each allowed cut can be either taken or not).
        """
        n = len(nums)
        if n == 0:
            return 0
        # Frequency of each value in the whole array (remaining to the right)
        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1

        seen = set()          # values that have appeared in the prefix
        shared = 0           # count of values that appear both in prefix and suffix
        allowed_cuts = 0

        # Iterate over possible cut positions after index i (i from 0 to n-2)
        for i in range(n - 1):
            v = nums[i]
            # Move this occurrence from suffix to prefix
            freq[v] -= 1

            if v not in seen:
                # First time we see this value in the prefix
                seen.add(v)
                if freq[v] > 0:
                    # Still appears later, so it is shared between sides
                    shared += 1
            else:
                # Value already in prefix; check if this was the last occurrence on the right
                if freq[v] == 0:
                    # It was contributing to shared before, now it doesn't
                    shared -= 1

            # If after processing position i there is no shared value, we can cut here
            if shared == 0:
                allowed_cuts += 1

        # Number of good partitions is 2^{allowed_cuts} modulo MOD
        return pow(2, allowed_cuts, MOD)
