from typing import List


class Solution:
    def maximumSubarrayXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        # Group queries by left endpoint.
        by_left = [[] for _ in range(n)]
        for i, (l, r) in enumerate(queries):
            by_left[l].append((r, i))

        ans = [0] * len(queries)
        # F[r] = XOR score of nums[l..r]; B[r] = max XOR score over subarrays of nums[l..r].
        # Recurrence: f[l][r] = f[l][r-1] ^ f[l+1][r], f[l][l] = nums[l].
        F_next = None
        B_next = None
        for l in range(n - 1, -1, -1):
            F = [0] * n
            B = [0] * n
            F[l] = nums[l]
            B[l] = nums[l]
            if F_next is not None:
                for r in range(l + 1, n):
                    f = F[r - 1] ^ F_next[r]
                    F[r] = f
                    b = B[r - 1]
                    if f > b:
                        b = f
                    bn = B_next[r]
                    if bn > b:
                        b = bn
                    B[r] = b
            for r, i in by_left[l]:
                ans[i] = B[r]
            F_next = F
            B_next = B
        return ans
