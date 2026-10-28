from typing import List

NEG = -(10 ** 18)


class Solution:
    def maximumSumSubsequence(self, nums: List[int], queries: List[List[int]]) -> int:
        MOD = 10 ** 9 + 7
        n = len(nums)
        size = 1
        while size < n:
            size <<= 1

        # node = (a00, a01, a10, a11): aXY = best sum where first elem taken iff X,
        # last elem taken iff Y, no two adjacent selected.
        def leaf(v):
            return (0, NEG, NEG, v)

        def combine(L, R):
            # result[x][y] = max over p,q not both 1 of L[x][p] + R[q][y]
            def best(x, y):
                lx0 = L[2 * x]      # L[x][0]
                lx1 = L[2 * x + 1]  # L[x][1]
                r0y = R[y]          # R[0][y]
                r1y = R[2 + y]      # R[1][y]
                return max(lx0 + max(r0y, r1y), lx1 + r0y)
            return (best(0, 0), best(0, 1), best(1, 0), best(1, 1))

        tree = [None] * (2 * size)
        for i in range(size):
            v = nums[i] if i < n else 0
            tree[size + i] = leaf(v)
        for i in range(size - 1, 0, -1):
            tree[i] = combine(tree[2 * i], tree[2 * i + 1])

        total = 0
        for pos, x in queries:
            i = size + pos
            tree[i] = leaf(x)
            i >>= 1
            while i >= 1:
                tree[i] = combine(tree[2 * i], tree[2 * i + 1])
                i >>= 1
            total += max(tree[1])
        return total % MOD
