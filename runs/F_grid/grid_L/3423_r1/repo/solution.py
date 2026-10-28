from typing import List

NEG = -(1 << 60)


class Solution:
    def maximumSumSubsequence(self, nums: List[int], queries: List[List[int]]) -> int:
        MOD = 10 ** 9 + 7
        n = len(nums)
        size = 1
        while size < n:
            size <<= 1

        # Each node: tuple (b00, b01, b10, b11) where bLR is the best sum of the
        # segment with leftmost element selected = L and rightmost selected = R,
        # no two adjacent selected. Padding leaves have value 0 (harmless).
        def leaf(x):
            return (0, NEG, NEG, x)

        def merge(L, R):
            # res[a][b] = max over c,d not both 1 of L[a][c] + R[d][b]
            l00, l01, l10, l11 = L
            r00, r01, r10, r11 = R
            # Allowed (c,d) pairs: not both selected at the junction.
            # a=0,b=0
            r00_ = max(l00 + r00, l00 + r10, l01 + r00)
            # a=0,b=1: R[d][1]
            r01_ = max(l00 + r01, l00 + r11, l01 + r01)
            # a=1,b=0
            r10_ = max(l10 + r00, l10 + r10, l11 + r00)
            # a=1,b=1
            r11_ = max(l10 + r01, l10 + r11, l11 + r01)
            return (r00_, r01_, r10_, r11_)

        tree = [None] * (2 * size)
        for i in range(size):
            tree[size + i] = leaf(nums[i] if i < n else 0)
        for i in range(size - 1, 0, -1):
            tree[i] = merge(tree[2 * i], tree[2 * i + 1])

        total = 0
        for pos, x in queries:
            i = size + pos
            tree[i] = leaf(x)
            i >>= 1
            while i:
                tree[i] = merge(tree[2 * i], tree[2 * i + 1])
                i >>= 1
            root = tree[1]
            total += max(root)
        return total % MOD
