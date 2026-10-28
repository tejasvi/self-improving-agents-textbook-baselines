from typing import *

# Bit-set helpers over indices 0..127 (value v <-> bit v of an int).
_V = 128
_M0 = []  # _M0[b]: bitmask of indices v with bit b clear
_M1 = []  # _M1[b]: bitmask of indices v with bit b set
for _b in range(7):
    _m1 = 0
    for _v in range(_V):
        if (_v >> _b) & 1:
            _m1 |= 1 << _v
    _M1.append(_m1)
    _M0.append(((1 << _V) - 1) ^ _m1)


def _or_image(S: int, x: int) -> int:
    """{v | x : v in S}"""
    for b in range(7):
        if (x >> b) & 1:
            S = ((S & _M0[b]) << (1 << b)) | (S & _M1[b])
    return S


def _xor_image(S: int, a: int) -> int:
    """{v ^ a : v in S}"""
    for b in range(7):
        if (a >> b) & 1:
            S = ((S & _M0[b]) << (1 << b)) | ((S & _M1[b]) >> (1 << b))
    return S


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def sweep(seq):
            # res[i] = bitset of OR values of k-subsets of seq[:i]
            dp = [0] * (k + 1)
            dp[0] = 1  # OR value 0 with empty set
            res = [0] * (n + 1)
            for i, x in enumerate(seq):
                top = min(k, i + 1)
                for j in range(top, 0, -1):
                    if dp[j - 1]:
                        dp[j] |= _or_image(dp[j - 1], x)
                res[i + 1] = dp[k]
            return res

        pre = sweep(nums)
        suf = sweep(nums[::-1])  # suf[i] = k-subsets of last i elements
        best = -1
        for m in range(k, n - k + 1):
            A = pre[m]
            B = suf[n - m]
            if not A or not B:
                continue
            X = 0
            a = A
            while a:
                low = a & -a
                v = low.bit_length() - 1
                X |= _xor_image(B, v)
                a ^= low
            best = max(best, X.bit_length() - 1)
        return best
