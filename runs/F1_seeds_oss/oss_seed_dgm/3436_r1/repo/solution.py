from typing import List

class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        """Return the minimum absolute difference between k and the bitwise OR of any subarray.

        The algorithm maintains, for each position i, the set of distinct OR values of subarrays
        ending at i. When we move to the next element, we can obtain the new set by OR-ing the
        current element with each value from the previous set and also starting a new subarray
        at the current element. Because a bit can be set only once, the size of this set is bounded
        by the number of bits (≤ 31 for the constraint limits), giving an overall O(n·bits) time
        complexity.
        """
        # Early exit if any element matches k exactly (difference zero)
        # This also handles the case of a single-element array.
        for x in nums:
            if x == k:
                return 0

        ans = float('inf')
        cur: List[int] = []  # OR values of subarrays ending at the previous index

        for num in nums:
            # Build the list of OR values for subarrays ending at the current index.
            nxt: List[int] = [num]
            for v in cur:
                nxt.append(v | num)

            # Deduplicate while preserving order (order is not important for correctness,
            # but keeping it small helps performance).
            seen = set()
            cur = []
            for val in nxt:
                if val not in seen:
                    seen.add(val)
                    cur.append(val)

            # Update the answer with all OR values that end at this position.
            for val in cur:
                diff = abs(k - val)
                if diff < ans:
                    ans = diff
                    if ans == 0:
                        return 0

        return ans
