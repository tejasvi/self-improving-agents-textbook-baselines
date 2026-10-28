"""Solution for minimizing OR after at most k adjacent AND merge operations.

The key observation is that merging a contiguous subarray into a single element results in the
bitwise AND of all numbers in that subarray, regardless of the order of merges.  Therefore the
process can be viewed as partitioning the original array into some number of contiguous segments.
If a segment has length `s`, it needs `s-1` operations to collapse it into one element.  With at most
`k` operations we must end up with at least `n - k` segments.

For a candidate answer `X` we ask: can we partition the array into at least `n-k` segments such that
the AND of each segment has no bits outside `X`?  If this is possible then the overall OR of the
remaining elements will be a subset of `X`, i.e., ≤ `X`.

Feasibility can be checked greedily: walk through the array while maintaining the running AND of the
current segment.  As soon as the running AND becomes a subset of `X` we cut a segment (count it) and
restart the running AND.  This yields the maximum possible number of segments for the given `X`.
If the maximum count is at least `n‑k` the answer `X` is achievable.

Feasibility is monotone in `X` (allowing more bits never makes it harder), so we binary‑search the
smallest feasible `X` in the range `[0, 2^30‑1]`.
"""

from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # Minimum number of segments we need to keep after at most k merges.
        need_segments = n - k
        # Upper bound for values (nums[i] < 2^30).
        MAX_VAL = (1 << 30) - 1

        def feasible(limit: int) -> bool:
            """Return True if we can obtain OR <= limit using at most k operations.

            We greedily form as many segments as possible whose AND does not contain bits
            outside `limit`.  The number of segments we can obtain is the maximum achievable.
            """
            seg_cnt = 0
            cur_and = MAX_VAL
            # bits that are NOT allowed in any segment AND (masked to 30 bits)
            mask_out = (~limit) & MAX_VAL
            for v in nums:
                cur_and &= v
                # If cur_and has no disallowed bits, we can close this segment.
                if cur_and & mask_out == 0:
                    seg_cnt += 1
                    cur_and = MAX_VAL
            return seg_cnt >= need_segments

        lo, hi = 0, MAX_VAL
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
