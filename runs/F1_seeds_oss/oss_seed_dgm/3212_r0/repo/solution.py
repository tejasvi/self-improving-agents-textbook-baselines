from typing import List

MOD = 10**9 + 7

class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        """Return number of good partitions modulo 1e9+7.
        A cut between i and i+1 is allowed if the set of numbers in the prefix
        nums[0..i] is disjoint from the set of numbers in the suffix nums[i+1..].
        The total number of good partitions equals 2^{k}, where k is the count
        of allowed cut positions.
        """
        n = len(nums)
        if n == 0:
            return 0
        # Build suffix frequency map
        suffix_cnt = {}
        for x in nums:
            suffix_cnt[x] = suffix_cnt.get(x, 0) + 1

        prefix_seen = set()
        bad = 0  # number of values present in both prefix and suffix
        allowed = 0

        # Iterate positions where a cut could be placed (0 .. n-2)
        for i in range(n - 1):
            x = nums[i]
            # move x from suffix to prefix
            suffix_cnt[x] -= 1
            if suffix_cnt[x] == 0:
                del suffix_cnt[x]

            if x in prefix_seen:
                # x already in prefix. It was possibly contributing to 'bad'
                # if it was also still in suffix before decrement.
                if x not in suffix_cnt:
                    # now x is only in prefix -> remove from bad if it was counted
                    bad -= 1
                # else still in suffix, bad unchanged
            else:
                # first time x appears in prefix
                prefix_seen.add(x)
                if x in suffix_cnt:
                    # now appears in both sides
                    bad += 1
                # else only in prefix, no effect

            # After processing position i, check if a cut after i is valid
            if bad == 0:
                allowed += 1

        # Number of partitions is 2^{allowed} modulo MOD
        return pow(2, allowed, MOD)
