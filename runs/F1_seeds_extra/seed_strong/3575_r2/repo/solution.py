from typing import *


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        FULL = (1 << 128) - 1
        # M[b]: bitset of values v in [0,128) having bit b set
        M = []
        for b in range(7):
            m = 0
            for v in range(128):
                if v >> b & 1:
                    m |= 1 << v
            M.append(m)
        N = [FULL ^ M[b] for b in range(7)]  # values with bit b clear

        def map_or(S, x):
            # returns {v | x : v in S}, S a bitset over values
            for b in range(7):
                if x >> b & 1:
                    S = ((S & N[b]) << (1 << b)) | (S & M[b])
            return S

        def xor_perm(B, a):
            # returns {v ^ a : v in B}
            for c in range(7):
                if a >> c & 1:
                    s = 1 << c
                    B = ((B & N[c]) << s) | ((B >> s) & N[c])
            return B

        # pre_k[m]: bitset of OR values of k-subsets of nums[:m]
        pre_k = [0] * (n + 1)
        pre = [0] * (k + 1)
        pre[0] = 1  # OR of empty set = 0
        for i in range(n):
            x = nums[i]
            for j in range(min(i + 1, k), 0, -1):
                if pre[j - 1]:
                    pre[j] |= map_or(pre[j - 1], x)
            pre_k[i + 1] = pre[k]

        # suf_k[m]: bitset of OR values of k-subsets of nums[m:]
        suf_k = [0] * (n + 1)
        suf = [0] * (k + 1)
        suf[0] = 1
        for i in range(n - 1, -1, -1):
            x = nums[i]
            for j in range(min(n - i, k), 0, -1):
                if suf[j - 1]:
                    suf[j] |= map_or(suf[j - 1], x)
            suf_k[i] = suf[k]

        best = 0
        R = 0
        for m in range(k, n - k + 1):
            A = pre_k[m]
            B = suf_k[m]
            if not A or not B:
                continue
            while A:
                low = A & -A
                a = low.bit_length() - 1
                A ^= low
                R |= xor_perm(B, a)
        return R.bit_length() - 1
