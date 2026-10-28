from typing import List


def _tri(s: int) -> int:
    # number of (x, y) with x, y >= 0 and x + y <= s
    return (s + 1) * (s + 2) // 2 if s >= 0 else 0


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        m = k - 1

        def max_sum(arr):
            # left[i]: nearest index to the left with value >= arr[i] (or -1)
            # right[i]: nearest index to the right with value > arr[i] (or n)
            left = [-1] * n
            right = [n] * n
            st = []
            for i in range(n):
                while st and arr[st[-1]] < arr[i]:
                    right[st.pop()] = i
                left[i] = st[-1] if st else -1
                st.append(i)
            total = 0
            T = _tri
            for i in range(n):
                L = i - left[i] - 1
                R = right[i] - i - 1
                # pairs (x, y): 0<=x<=L, 0<=y<=R, x+y<=m
                cnt = T(m) - T(m - L - 1) - T(m - R - 1) + T(m - L - R - 2)
                total += arr[i] * cnt
            return total

        return max_sum(nums) - max_sum([-v for v in nums])
