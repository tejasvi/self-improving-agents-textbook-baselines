from typing import List


class Solution:
    def maximumSubarrayXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        # best[l][r] = max XOR score over subarrays of nums[l..r]
        # score[l][r] = score[l][r-1] ^ score[l+1][r]  (Pascal's rule mod 2)
        best = [None] * (n + 1)
        prev_score = None  # score row for l+1
        prev_best = None   # best row for l+1
        for l in range(n - 1, -1, -1):
            score = [0] * n
            brow = [0] * n
            score[l] = nums[l]
            brow[l] = nums[l]
            for r in range(l + 1, n):
                s = score[r - 1] ^ prev_score[r]
                score[r] = s
                b = s
                if brow[r - 1] > b:
                    b = brow[r - 1]
                if prev_best[r] > b:
                    b = prev_best[r]
                brow[r] = b
            best[l] = brow
            prev_score = score
            prev_best = brow
        return [best[l][r] for l, r in queries]
