from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # Helper to compute total contribution of either minima or maxima
        def contribution(is_min: bool) -> int:
            # prev index with strict < (for min) or > (for max)
            prev = [-1] * n
            # next index with non‑strict <= (for min) or >= (for max)
            nxt = [n] * n
            stack = []
            # Compute prev indices
            for i, val in enumerate(nums):
                while stack and ((nums[stack[-1]] > val) if is_min else (nums[stack[-1]] < val)):
                    stack.pop()
                prev[i] = stack[-1] if stack else -1
                stack.append(i)
            # Compute next indices
            stack.clear()
            for i in range(n - 1, -1, -1):
                val = nums[i]
                while stack and ((nums[stack[-1]] >= val) if is_min else (nums[stack[-1]] <= val)):
                    stack.pop()
                nxt[i] = stack[-1] if stack else n
                stack.append(i)

            total = 0
            for i in range(n):
                left = prev[i] + 1               # smallest allowed l
                right = nxt[i] - 1                # largest allowed r
                # l must also satisfy length constraint: i - l + 1 <= k => l >= i - k + 1
                start = max(left, i - k + 1)
                if start > i:
                    continue
                # The point where the right bound switches from l+k-1 to the absolute right
                # l >= right - k + 1  => right is limiting
                split = max(start, right - k + 1)
                # Region 1: l in [start, split-1] where max_r = l + k - 1
                if split > start:
                    len1 = split - start
                    end1 = split - 1
                    # sum of l over this range
                    sum_l = (start + end1) * len1 // 2
                    # each contributes (l + k - i)
                    total += nums[i] * (sum_l + len1 * (k - i))
                # Region 2: l in [split, i] where max_r = right
                if split <= i:
                    len2 = i - split + 1
                    total += nums[i] * len2 * (right - i + 1)
            return total

        sum_min = contribution(is_min=True)
        sum_max = contribution(is_min=False)
        return sum_min + sum_max
