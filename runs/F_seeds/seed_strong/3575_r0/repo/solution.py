from typing import *


_V = 128
_BITS = 7
# HAS[b]: bitset of values v in [0,128) with bit b set; NOT[b]: without bit b
_HAS = [sum(1 << v for v in range(_V) if v >> b & 1) for b in range(_BITS)]
_NOT = [((1 << _V) - 1) ^ _HAS[b] for b in range(_BITS)]
# G[t][p]: bitset of values v with (v >> t) == p
_G = [[sum(1 << v for v in range(_V) if (v >> t) == p) for p in range(_V >> t)]
      for t in range(_BITS)]


def _or_shift(s: int, x: int) -> int:
    """Bitset {v | x : v in s}."""
    for b in range(_BITS):
        if x >> b & 1:
            s = (s & _HAS[b]) | ((s & _NOT[b]) << (1 << b))
    return s


def _prefix_sets(seq: List[int], k: int) -> List[int]:
    """res[i] = bitset of OR values achievable by choosing exactly k of seq[:i]."""
    dp = [0] * (k + 1)
    dp[0] = 1  # OR value 0 with zero elements
    res = [dp[k]]
    for x in seq:
        for j in range(k - 1, -1, -1):
            if dp[j]:
                dp[j + 1] |= _or_shift(dp[j], x)
        res.append(dp[k])
    return res


def _max_xor(a: int, S: int) -> int:
    """max over b in S (bitset) of a ^ b; S must be nonempty."""
    p = 0
    for t in range(_BITS - 1, -1, -1):
        d = 1 - ((a >> t) & 1)
        q = p * 2 + d
        if S & _G[t][q]:
            p = q
        else:
            p = q ^ 1
    return a ^ p


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        pre = _prefix_sets(nums, k)
        suf = _prefix_sets(nums[::-1], k)
        best = 0
        for m in range(k, n - k + 1):
            A = pre[m]
            B = suf[n - m]
            if not A or not B:
                continue
            a = A
            while a:
                low = a & -a
                v = low.bit_length() - 1
                a ^= low
                r = _max_xor(v, B)
                if r > best:
                    best = r
        return best
