from typing import List


class Solution:
    def _max_contrib(self, nums: List[int], k: int) -> int:
        """Sum of max over all subarrays of length <= k."""
        n = len(nums)
        # left[i]: first index of range where nums[i] is max (prev strictly greater)
        left = [0] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            left[i] = stack[-1] + 1 if stack else 0
            stack.append(i)
        # right[i]: last index of range (next greater or equal, tie-break)
        right = [0] * n
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] < nums[i]:
                stack.pop()
            right[i] = stack[-1] - 1 if stack else n - 1
            stack.append(i)

        total = 0
        for i in range(n):
            a, b = left[i], right[i]
            lo = max(a, i - k + 1)
            hi = i
            if lo > hi:
                continue
            # count = sum_{l=lo}^{hi} (min(b, l+k-1) - i + 1)
            m = b - k + 1  # for l <= m: l+k-1 <= b
            cnt = 0
            # part 1: l in [lo, min(hi, m)] -> term = l + k - i
            p1_hi = min(hi, m)
            if lo <= p1_hi:
                c = p1_hi - lo + 1
                s = (lo + p1_hi) * c // 2
                cnt += s + c * (k - i)
            # part 2: l in [max(lo, m+1), hi] -> term = b - i + 1
            p2_lo = max(lo, m + 1)
            if p2_lo <= hi:
                cnt += (hi - p2_lo + 1) * (b - i + 1)
            total += nums[i] * cnt
        return total

    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        mx = self._max_contrib(nums, k)
        mn = -self._max_contrib([-x for x in nums], k)
        return mx + mn
