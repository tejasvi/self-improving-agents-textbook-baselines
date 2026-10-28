from typing import List

MOD = 10**9 + 7

class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        """Return number of ways to partition nums into contiguous subarrays such that
        no integer appears in more than one subarray.
        The answer is 2^{k-1} where k is the number of positions i (0-indexed) that can be
        the end of a subarray, i.e., all occurrences of numbers seen so far end at or before i.
        """
        n = len(nums)
        # Record last occurrence of each value
        last = {}
        for idx, val in enumerate(nums):
            last[val] = idx
        # Scan to find valid cut positions
        cut_cnt = 0
        cur_max = -1
        for i, val in enumerate(nums):
            cur_max = max(cur_max, last[val])
            if cur_max == i:
                cut_cnt += 1
        # There is always at least one cut (the end of array)
        # Number of partitions is 2^{cut_cnt-1}
        return pow(2, cut_cnt - 1, MOD)
