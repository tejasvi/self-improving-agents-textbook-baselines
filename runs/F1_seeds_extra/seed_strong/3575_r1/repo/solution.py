from typing import *


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def build(seq):
            # res[m][j] = set of OR values from choosing j elements of seq[:m]
            res = []
            dp = [set() for _ in range(k + 1)]
            dp[0].add(0)
            res.append([frozenset(s) for s in dp])
            for x in seq:
                for j in range(k, 0, -1):
                    if dp[j - 1]:
                        dp[j].update({v | x for v in dp[j - 1]})
                res.append([frozenset(s) for s in dp])
            return res

        L = build(nums)
        R = build(nums[::-1])
        best = -1
        for m in range(k, n - k + 1):
            left = L[m][k]
            right = R[n - m][k]
            for a in left:
                for b in right:
                    if a ^ b > best:
                        best = a ^ b
        return best
