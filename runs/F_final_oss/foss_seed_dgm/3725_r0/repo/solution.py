from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # Helper to count pairs (a,b) with 0<=a<=A, 0<=b<=B and a+b <= S
        def count_pairs_le(A: int, B: int, S: int) -> int:
            if S < 0:
                return 0
            # total possible pairs
            if S >= A + B:
                return (A + 1) * (B + 1)
            # Ensure A <= B for simpler handling (symmetry)
            if A > B:
                A, B = B, A
            if S <= A:
                # sum_{a=0}^{S} (S - a + 1)
                return (S + 1) * (S + 2) // 2
            # S > A
            # Find split point where S - a >= B  -> a <= S - B
            split = S - B
            if split < 0:
                split = 0
            cnt = 0
            # For a in [0, split-1], min(B, S-a) = B
            if split > 0:
                cnt += (B + 1) * split
            # For a in [split, A], min = S - a
            # number of terms
            nterms = A - split + 1
            first = S - split + 1  # when a = split
            last = S - A + 1       # when a = A
            cnt += nterms * (first + last) // 2
            return cnt

        # Compute bounds for maximum contributions
        prev_greater = [-1] * n
        next_greater_eq = [n] * n
        stack = []
        for i, val in enumerate(nums):
            while stack and nums[stack[-1]] <= val:
                stack.pop()
            prev_greater[i] = stack[-1] if stack else -1
            stack.append(i)
        stack.clear()
        for i in range(n - 1, -1, -1):
            val = nums[i]
            while stack and nums[stack[-1]] < val:
                stack.pop()
            next_greater_eq[i] = stack[-1] if stack else n
            stack.append(i)

        # Compute bounds for minimum contributions
        prev_smaller = [-1] * n
        next_smaller_eq = [n] * n
        stack.clear()
        for i, val in enumerate(nums):
            while stack and nums[stack[-1]] >= val:
                stack.pop()
            prev_smaller[i] = stack[-1] if stack else -1
            stack.append(i)
        stack.clear()
        for i in range(n - 1, -1, -1):
            val = nums[i]
            while stack and nums[stack[-1]] > val:
                stack.pop()
            next_smaller_eq[i] = stack[-1] if stack else n
            stack.append(i)

        total = 0
        for i in range(n):
            # Maximum contribution
            A = i - prev_greater[i] - 1  # max a distance
            B = next_greater_eq[i] - i - 1
            cnt_max = count_pairs_le(A, B, k - 1)
            total += nums[i] * cnt_max
            # Minimum contribution
            A = i - prev_smaller[i] - 1
            B = next_smaller_eq[i] - i - 1
            cnt_min = count_pairs_le(A, B, k - 1)
            total += nums[i] * cnt_min
        return total
