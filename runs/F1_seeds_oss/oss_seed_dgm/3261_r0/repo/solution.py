from typing import List

class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        """Return the minimum possible bitwise OR after at most k merge operations.

        The operation merges two adjacent numbers into their bitwise AND. After a series of
        merges we end up with a partition of the original array into contiguous segments;
        each segment contributes a single number equal to the AND of all elements in the
        segment. The number of performed merges equals ``len(nums) - number_of_segments``.
        With at most ``k`` merges we must have at least ``n - k`` segments.

        For a candidate upper bound ``limit`` we ask whether we can create a partition where
        the AND of each segment is a subset of ``limit`` (i.e. ``segment_and | limit == limit``).
        If that is possible with at least ``n - k`` segments, then the final OR can be kept
        within ``limit``.  We can test this using a greedy scan that always creates the
        shortest possible valid segment, which maximises the number of segments.
        """
        n = len(nums)

        # Helper that checks if we can achieve final OR <= limit.
        def feasible(limit: int) -> bool:
            seg_cnt = 0
            i = 0
            while i < n:
                cur = nums[i]
                # If a single element already satisfies the limit, we can close a segment.
                if (cur | limit) == limit:
                    seg_cnt += 1
                    i += 1
                    continue
                # Otherwise we need to extend the segment.
                j = i + 1
                while j < n:
                    cur &= nums[j]
                    if (cur | limit) == limit:
                        break
                    j += 1
                # If we exited the loop without satisfying the limit, it's impossible.
                if j == n and (cur | limit) != limit:
                    return False
                # We have a valid segment from i..j inclusive.
                seg_cnt += 1
                i = j + 1
            # We need at least n - k segments (i.e., at most k merges).
            return seg_cnt >= n - k

        # Build answer bit by bit from high to low (numbers are < 2^30).
        answer = 0
        for bit in range(29, -1, -1):
            # Try to keep this bit 0.
            if feasible(answer):
                # current higher bits already allow a solution, keep this bit cleared.
                continue
            # Otherwise we must set this bit.
            answer |= (1 << bit)
        return answer
